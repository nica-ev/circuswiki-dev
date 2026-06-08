from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from obsidian.cli import normalize_vault_path, open_path, run_obsidian, status  # noqa: E402


class ObsidianCliTests(unittest.TestCase):
    def test_status_reports_missing_cli_without_failing(self) -> None:
        with patch("obsidian.cli.shutil.which", return_value=None):
            result = status()
        self.assertTrue(result["ok"])
        self.assertFalse(result["available"])
        self.assertEqual(result["command"], ["obsidian"])
        self.assertIn("not found", result["error"])

    def test_status_reports_available_cli_path(self) -> None:
        with patch("obsidian.cli.shutil.which", return_value="/usr/bin/obsidian"):
            result = status()
        self.assertTrue(result["ok"])
        self.assertTrue(result["available"])
        self.assertEqual(result["command"], ["/usr/bin/obsidian"])
        self.assertEqual(result["stdout"], "/usr/bin/obsidian")

    def test_run_obsidian_decodes_cli_output_as_utf8(self) -> None:
        completed = Mock(returncode=0, stdout='{"title":"Aufwärmspiele"}', stderr="")
        with patch("obsidian.cli.shutil.which", return_value="/usr/bin/obsidian"):
            with patch("obsidian.cli.subprocess.run", return_value=completed) as run:
                result = run_obsidian(["base:query"])

        self.assertTrue(result.ok)
        self.assertIn("Aufwärmspiele", result.stdout)
        self.assertEqual(run.call_args.kwargs["encoding"], "utf-8")
        self.assertEqual(run.call_args.kwargs["errors"], "replace")

    def test_normalize_vault_path_accepts_existing_relative_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            note = root / "docs" / "de" / "Test.md"
            note.parent.mkdir(parents=True)
            note.write_text("test", encoding="utf-8")

            with patch("obsidian.cli.ROOT", root):
                self.assertEqual(normalize_vault_path("docs/de/Test.md"), "docs/de/Test.md")

    def test_normalize_vault_path_rejects_outside_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            outside = root.parent / "outside.md"
            outside.write_text("test", encoding="utf-8")
            try:
                with patch("obsidian.cli.ROOT", root):
                    with self.assertRaises(ValueError):
                        normalize_vault_path(str(outside))
            finally:
                outside.unlink(missing_ok=True)

    def test_open_path_uses_obsidian_open_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            note = root / "docs" / "de" / "Test.md"
            note.parent.mkdir(parents=True)
            note.write_text("test", encoding="utf-8")

            completed = Mock(returncode=0, stdout="", stderr="")
            with patch("obsidian.cli.ROOT", root):
                with patch("obsidian.cli.shutil.which", return_value="/usr/bin/obsidian"):
                    with patch("obsidian.cli.subprocess.run", return_value=completed) as run:
                        result = open_path("docs/de/Test.md", newtab=True)

            self.assertTrue(result["ok"])
            self.assertEqual(result["path"], "docs/de/Test.md")
            self.assertEqual(
                run.call_args.args[0],
                ["/usr/bin/obsidian", "open", "path=docs/de/Test.md", "newtab"],
            )


if __name__ == "__main__":
    unittest.main()
