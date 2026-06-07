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
    batch_translation_plan,
    find_group_source_language,
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
