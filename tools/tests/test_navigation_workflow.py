from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from navigation.workflow import format_nav_block, replace_nav_block  # noqa: E402


class NavigationWorkflowTests(unittest.TestCase):
    def test_format_nav_block_renders_nested_toml_nav(self) -> None:
        nav = [
            {"Start": "index.md"},
            {"Games": [{"Tag": "spiele/fangen.md"}]},
        ]
        result = format_nav_block(nav)
        self.assertIn('nav = [', result)
        self.assertIn('{ "Start" = "index.md" },', result)
        self.assertIn('{ "Games" = [', result)
        self.assertIn('{ "Tag" = "spiele/fangen.md" },', result)

    def test_replace_nav_block_changes_only_first_nav_block(self) -> None:
        text = '[project]\nname = "Test"\nnav = [\n  { "Old" = "old.md" },\n]\n'
        result = replace_nav_block(text, 'nav = [\n  { "New" = "new.md" },\n]')
        self.assertIn('{ "New" = "new.md" }', result)
        self.assertNotIn('{ "Old" = "old.md" }', result)
        self.assertIn('name = "Test"', result)


if __name__ == "__main__":
    unittest.main()
