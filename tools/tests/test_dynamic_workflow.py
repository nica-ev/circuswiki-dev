from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from dynamic.blocks import parse_dynamic_blocks, replace_block_contents  # noqa: E402
from dynamic.render import markdown_href, render_dynamic, render_table  # noqa: E402
from dynamic.workflow import frontmatter_tags  # noqa: E402


class DynamicWorkflowTests(unittest.TestCase):
    def test_parse_and_replace_dynamic_block_content_only(self) -> None:
        body = """Intro
<!-- dynamic:start
engine: obsidian-base
base: _bases/games.base
view: Fangspiele
-->
<!-- dynamic:content -->
old table
<!-- dynamic:end -->
Outro
"""
        blocks = parse_dynamic_blocks(body)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].config["engine"], "obsidian-base")
        self.assertEqual(blocks[0].config["base"], "_bases/games.base")
        self.assertEqual(blocks[0].config["view"], "Fangspiele")

        replaced = replace_block_contents(body, {0: "new table"})
        self.assertIn("Intro", replaced)
        self.assertIn("new table", replaced)
        self.assertNotIn("old table", replaced)
        self.assertIn("Outro", replaced)

    def test_frontmatter_tags_support_yaml_list_and_inline_list(self) -> None:
        self.assertIn("dynamic", frontmatter_tags("tags:\n  - spiele\n  - dynamic\n"))
        self.assertIn("dynamic", frontmatter_tags("tags: [spiele, #dynamic]\n"))

    def test_render_table_does_not_filter_language_by_default(self) -> None:
        page_path = ROOT / "docs" / "de" / "Fangspiele.md"
        markdown, warnings = render_table(
            [
                {"file": "docs/de/Alaska Baseball.md", "group-min": 30},
                {"file": "docs/en/Alaska Baseball.md", "group-min": 30},
            ],
            page_path,
            {},
        )
        self.assertIn("[Alaska Baseball](<Alaska%20Baseball.md>)", markdown)
        self.assertIn("[Alaska Baseball](<../en/Alaska%20Baseball.md>)", markdown)
        self.assertEqual(warnings, [])

    def test_render_table_filters_current_language_when_explicit(self) -> None:
        page_path = ROOT / "docs" / "de" / "Fangspiele.md"
        markdown, warnings = render_table(
            [
                {"file": "docs/de/Alaska Baseball.md", "group-min": 30},
                {"file": "docs/en/Alaska Baseball.md", "group-min": 30},
            ],
            page_path,
            {"language": "current"},
        )
        self.assertIn("[Alaska Baseball](<Alaska%20Baseball.md>)", markdown)
        self.assertNotIn("../en", markdown)
        self.assertEqual(warnings, ["language filter kept 1/2 rows for de"])

    def test_markdown_href_is_relative_to_current_page(self) -> None:
        page_path = ROOT / "docs" / "de" / "spiele" / "Index.md"
        href = markdown_href("docs/de/Alaska Baseball.md", page_path)
        self.assertEqual(href, "../Alaska%20Baseball.md")

    def test_markdown_href_does_not_start_with_percent_encoded_character(self) -> None:
        page_path = ROOT / "docs" / "de" / "Liste aller Spiele.md"
        href = markdown_href("docs/de/Ägyptisches Wurfspiel.md", page_path)
        self.assertEqual(href, "./%C3%84gyptisches%20Wurfspiel.md")

    def test_render_dynamic_supports_list_format(self) -> None:
        page_path = ROOT / "docs" / "de" / "Kaskade Workspace.md"
        markdown, warnings = render_dynamic(
            [
                {"file": "docs/de/Kaskade 001.md", "title": "Kaskade 001"},
                {"file": "docs/de/Kaskade 002.md", "title": "Kaskade 002"},
            ],
            page_path,
            {"format": "list"},
        )
        self.assertIn("edit the dynamic block config, not this list", markdown)
        self.assertIn("- [Kaskade 001](<Kaskade%20001.md>)", markdown)
        self.assertIn("- [Kaskade 002](<Kaskade%20002.md>)", markdown)
        self.assertEqual(warnings, [])

    def test_render_dynamic_warns_and_falls_back_to_table_for_unknown_format(self) -> None:
        page_path = ROOT / "docs" / "de" / "Fangspiele.md"
        markdown, warnings = render_dynamic(
            [{"file": "docs/de/Alaska Baseball.md", "group-min": 30}],
            page_path,
            {"format": "cards"},
        )
        self.assertIn("| file", markdown)
        self.assertIn("group-min |", markdown)
        self.assertEqual(warnings, ["unsupported format cards; rendered table"])

    def test_render_dynamic_pads_table_rows_consistently(self) -> None:
        page_path = ROOT / "docs" / "de" / "Fangspiele.md"
        markdown, _warnings = render_dynamic(
            [
                {"file": "docs/de/A.md", "Material": "x"},
                {"file": "docs/de/Long File Name.md", "Material": "longer value"},
            ],
            page_path,
            {"format": "table", "columns": "file, Material"},
        )
        lines = [line for line in markdown.splitlines() if line.startswith("|")]
        self.assertEqual(len(lines), 4)
        self.assertTrue(all(len(line) == len(lines[0]) for line in lines), lines)


if __name__ == "__main__":
    unittest.main()
