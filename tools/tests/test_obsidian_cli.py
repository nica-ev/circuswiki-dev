from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from obsidian.cli import status  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
