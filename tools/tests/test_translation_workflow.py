from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from translation.markdown import join_markdown, split_markdown  # noqa: E402
from translation.metadata import ensure_scalars, read_scalar  # noqa: E402
from translation.workflow import (  # noqa: E402
    VaultPage,
    apply_translated_metadata,
    batch_translation_plan,
    find_group_source_language,
    merge_source_metadata,
    restore_markdown_link_targets,
    restore_wikilink_targets,
    source_body_hash,
    source_metadata_hash,
)


class TranslationWorkflowTests(unittest.TestCase):
    def test_batch_plan_all_targets(self) -> None:
        plan = batch_translation_plan("all", 1)
        self.assertEqual(plan["target_lang"], "all")
        self.assertGreaterEqual(plan["planned_count"], 0)
        self.assertIn("target_langs", plan)
        self.assertIn("de", plan["target_langs"])

    def test_batch_plan_reason_filter(self) -> None:
        plan = batch_translation_plan("all", 5, reason="missing_file")
        self.assertTrue(
            all(item["reason"] == "missing_file" for item in plan["candidates"]),
            plan["candidates"],
        )
        self.assertEqual(plan["filters"]["reason"], "missing_file")

    def test_batch_plan_source_filter(self) -> None:
        plan = batch_translation_plan("all", 5, source_lang="de")
        self.assertTrue(
            all(item["source_lang"] == "de" for item in plan["candidates"]),
            plan["candidates"],
        )
        self.assertEqual(plan["filters"]["source_lang"], "de")

    def test_batch_plan_max_source_chars_filter(self) -> None:
        plan = batch_translation_plan("all", 5, max_source_chars=1)
        self.assertEqual(plan["total_candidates"], 0)
        self.assertEqual(plan["filters"]["max_source_chars"], 1)

    def test_source_language_uses_original_status(self) -> None:
        pages = {
            "en": [self.page("en", "machine-translated")],
            "pl": [self.page("pl", "original")],
            "de": [self.page("de", "")],
        }
        self.assertEqual(find_group_source_language(pages), "pl")

    def test_frontmatter_unknown_fields_are_preserved(self) -> None:
        source = "---\ntitle: Test\ncustom_field: keep me\n---\nBody\n"
        document = split_markdown(source)
        updated = ensure_scalars(document.frontmatter, {"lang": "en"})
        output = join_markdown(updated, document.body)
        result = split_markdown(output)
        self.assertEqual(read_scalar(result.frontmatter, "custom_field"), "keep me")
        self.assertEqual(read_scalar(result.frontmatter, "lang"), "en")

    def test_body_hash_ignores_metadata_changes(self) -> None:
        self.assertEqual(source_body_hash("Body\n"), source_body_hash("Body\n"))
        self.assertNotEqual(source_body_hash("Body\n"), source_body_hash("Changed\n"))

    def test_metadata_hash_tracks_title_and_description(self) -> None:
        first = "title: Test\ndescription: One\ncustom: ignored\n"
        second = "title: Test\ndescription: Two\ncustom: ignored\n"
        third = "title: Test\ndescription: One\ncustom: changed\n"
        self.assertNotEqual(source_metadata_hash(first), source_metadata_hash(second))
        self.assertEqual(source_metadata_hash(first), source_metadata_hash(third))

    def test_metadata_merge_preserves_target_translated_fields(self) -> None:
        source = "title: Quelle\ndescription: Deutsch\ntags:\n  - spiel\nauthors:\n  - Marc\n"
        target = "title: Existing English\ndescription: Existing description\nlocal_note: keep\n"
        merged = merge_source_metadata(target, source)
        translated = apply_translated_metadata(
            merged,
            {"title": "Source", "description": "English description"},
        )
        self.assertEqual(read_scalar(translated, "title"), "Source")
        self.assertEqual(read_scalar(translated, "description"), "English description")
        self.assertEqual(read_scalar(translated, "local_note"), "keep")
        self.assertIn("tags:\n  - spiel", translated)
        self.assertIn("authors:\n  - Marc", translated)

    def test_markdown_link_targets_are_restored_without_touching_external_links(self) -> None:
        source = "See [Spiel](spiele/original.md#regeln) and [Site](https://example.org).\n"
        translated = "See [Game](games/translated.md#rules) and [Site](https://example.org).\n"
        result = restore_markdown_link_targets(source, translated)
        self.assertIn("[Game](spiele/original.md#regeln)", result)
        self.assertIn("[Site](https://example.org)", result)

    def test_wikilink_targets_are_restored_but_aliases_stay_translated(self) -> None:
        source = "Siehe [[Spiele/Fangen|Fangen]] und ![[img/original.png]].\n"
        translated = "See [[Games/Tag|Tag]] and ![[img/translated.png]].\n"
        result = restore_wikilink_targets(source, translated)
        self.assertIn("[[Spiele/Fangen|Tag]]", result)
        self.assertIn("![[img/original.png]]", result)

    def page(self, language: str, status: str) -> VaultPage:
        return VaultPage(
            path=ROOT / "docs" / language / "example.md",
            rel_path=f"docs/{language}/example.md",
            language=language,
            relative_path="example.md",
            frontmatter=f"lang: {language}\ntranslation_status: {status}\n",
            body="Body",
            has_frontmatter=True,
            translation_id="example",
            translation_status=status,
            translation_source_lang="",
            translation_source="",
            translation_source_hash="",
            title="Example",
        )


if __name__ == "__main__":
    unittest.main()
