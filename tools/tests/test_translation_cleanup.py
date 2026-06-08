from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from translation import cleanup  # noqa: E402


def note(frontmatter: str, body: str = "Body\n") -> str:
    return f"---\n{textwrap.dedent(frontmatter).strip()}\n---\n{body}"


class TranslationCleanupTests(unittest.TestCase):
    def run_with_vault(self, callback) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            docs = root / "docs"
            docs.mkdir()

            def local_rel(path: Path) -> str:
                return Path(path).resolve().relative_to(root).as_posix()

            with (
                patch.object(cleanup, "ROOT", root),
                patch.object(cleanup, "DOCS", docs),
                patch.object(cleanup, "rel", local_rel),
            ):
                callback(root, docs)

    def test_scan_marks_missing_machine_translation_source_as_deletable(self) -> None:
        def scenario(_root: Path, docs: Path) -> None:
            target = docs / "en" / "Old.md"
            target.parent.mkdir()
            target.write_text(
                note(
                    """
                    lang: en
                    translation_id: game-old
                    translation_status: machine-translated
                    translation_source: docs/de/Old.md
                    translation_source_lang: de
                    """
                ),
                encoding="utf-8",
            )

            result = cleanup.scan_orphan_translations()

            self.assertEqual(result["total"], 1)
            self.assertEqual(result["deletable_count"], 1)
            item = result["items"][0]
            self.assertEqual(item["path"], "docs/en/Old.md")
            self.assertEqual(item["reason"], "missing_translation_source_file")
            self.assertTrue(item["deletable"])

        self.run_with_vault(scenario)

    def test_scan_ignores_original_files_without_translation_source(self) -> None:
        def scenario(_root: Path, docs: Path) -> None:
            source = docs / "de" / "Original.md"
            source.parent.mkdir()
            source.write_text(
                note(
                    """
                    lang: de
                    translation_id: game-original
                    translation_status: original
                    """
                ),
                encoding="utf-8",
            )

            result = cleanup.scan_orphan_translations()

            self.assertEqual(result["total"], 0)

        self.run_with_vault(scenario)

    def test_scan_reports_translation_id_mismatch_without_deletion(self) -> None:
        def scenario(_root: Path, docs: Path) -> None:
            source = docs / "de" / "Renamed.md"
            target = docs / "en" / "Old.md"
            source.parent.mkdir()
            target.parent.mkdir()
            source.write_text(
                note(
                    """
                    lang: de
                    translation_id: game-renamed
                    translation_status: original
                    """
                ),
                encoding="utf-8",
            )
            target.write_text(
                note(
                    """
                    lang: en
                    translation_id: game-old
                    translation_status: machine-translated
                    translation_source: docs/de/Renamed.md
                    translation_source_lang: de
                    """
                ),
                encoding="utf-8",
            )

            result = cleanup.scan_orphan_translations()

            self.assertEqual(result["total"], 1)
            item = result["items"][0]
            self.assertEqual(item["reason"], "source_translation_id_mismatch")
            self.assertFalse(item["deletable"])
            self.assertTrue(target.exists())

        self.run_with_vault(scenario)

    def test_delete_orphan_translations_deletes_only_current_deletable_items(self) -> None:
        def scenario(_root: Path, docs: Path) -> None:
            orphan = docs / "en" / "Old.md"
            mismatch_source = docs / "de" / "Renamed.md"
            mismatch = docs / "en" / "Mismatch.md"
            orphan.parent.mkdir()
            mismatch_source.parent.mkdir()
            orphan.write_text(
                note(
                    """
                    lang: en
                    translation_id: game-old
                    translation_status: machine-translated
                    translation_source: docs/de/Old.md
                    translation_source_lang: de
                    """
                ),
                encoding="utf-8",
            )
            mismatch_source.write_text(
                note(
                    """
                    lang: de
                    translation_id: different
                    translation_status: original
                    """
                ),
                encoding="utf-8",
            )
            mismatch.write_text(
                note(
                    """
                    lang: en
                    translation_id: game-mismatch
                    translation_status: machine-translated
                    translation_source: docs/de/Renamed.md
                    translation_source_lang: de
                    """
                ),
                encoding="utf-8",
            )

            result = cleanup.delete_orphan_translations(
                ["docs/en/Old.md", "docs/en/Mismatch.md", "../outside.md"]
            )

            self.assertEqual(result["deleted_count"], 1)
            self.assertEqual(result["skipped_count"], 2)
            self.assertFalse(orphan.exists())
            self.assertTrue(mismatch.exists())
            self.assertIn("not_deletable", {item["reason"] for item in result["skipped"]})
            self.assertIn("invalid_path", {item["reason"] for item in result["skipped"]})

        self.run_with_vault(scenario)


if __name__ == "__main__":
    unittest.main()
