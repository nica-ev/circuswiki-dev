from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from translation.original_graph import build_original_graph, extract_explicit_links  # noqa: E402
from translation.workflow import VaultPage  # noqa: E402


class OriginalGraphTests(unittest.TestCase):
    def test_graph_normalizes_links_through_translations_to_originals(self) -> None:
        groups = {
            "a": {
                "pl": [
                    self.page(
                        "pl",
                        "a.md",
                        "A",
                        "a",
                        "original",
                        "[German B](../de/b.md)\n",
                    )
                ]
            },
            "b": {
                "it": [self.page("it", "b.md", "B Original", "b", "original", "")],
                "de": [self.page("de", "b.md", "B German", "b", "machine-translated", "")],
            },
        }
        graph = build_original_graph(["pl", "it", "de"], groups)

        self.assertEqual({node["id"] for node in graph["nodes"]}, {"a", "b"})
        self.assertEqual(
            [(edge["source"], edge["target"]) for edge in graph["edges"]],
            [("a", "b")],
        )
        self.assertEqual(graph["edges"][0]["links"][0]["resolved_path"], "docs/de/b.md")

    def test_graph_resolves_wikilinks_to_same_language_translation_then_original_group(self) -> None:
        groups = {
            "a": {
                "pl": [self.page("pl", "a.md", "A", "a", "original", "[[B Polish|B]]\n")]
            },
            "b": {
                "it": [self.page("it", "b.md", "B Original", "b", "original", "")],
                "pl": [self.page("pl", "b.md", "B Polish", "b", "machine-translated", "")],
            },
        }
        graph = build_original_graph(["pl", "it"], groups)

        self.assertEqual(
            [(edge["source"], edge["target"]) for edge in graph["edges"]],
            [("a", "b")],
        )
        self.assertEqual(graph["edges"][0]["links"][0]["resolved_path"], "docs/pl/b.md")

    def test_extract_explicit_links_ignores_images_and_code_fences(self) -> None:
        body = (
            "[Content](target.md)\n"
            "![Image](image.png)\n"
            "[[Target Page]]\n"
            "![[image.png]]\n"
            "```\n"
            "[Ignored](ignored.md)\n"
            "```\n"
        )
        links = extract_explicit_links(body)

        self.assertEqual(
            [(link["type"], link["target"]) for link in links],
            [("markdown", "target.md"), ("wikilink", "Target Page")],
        )

    def test_extract_explicit_links_handles_table_angle_targets(self) -> None:
        body = (
            "| file |\n"
            "| --- |\n"
            "| [Alaska Baseball](<Alaska%20Baseball.md>) |\n"
            "| [Ägyptisches Wurfspiel](<./%C3%84gyptisches%20Wurfspiel.md>) |\n"
            "| [Raw Space](<Raw Space.md>) |\n"
        )
        links = extract_explicit_links(body)

        self.assertEqual(
            [link["target"] for link in links],
            [
                "Alaska%20Baseball.md",
                "./%C3%84gyptisches%20Wurfspiel.md",
                "Raw Space.md",
            ],
        )

    def test_graph_resolves_markdown_links_inside_tables(self) -> None:
        groups = {
            "index": {
                "de": [
                    self.page(
                        "de",
                        "index.md",
                        "Index",
                        "index",
                        "original",
                        "| file |\n| --- |\n| [Target](<Target%20Page.md>) |\n",
                    )
                ]
            },
            "target": {
                "de": [self.page("de", "Target Page.md", "Target", "target", "original", "")]
            },
        }
        graph = build_original_graph(["de"], groups)

        self.assertEqual(
            [(edge["source"], edge["target"]) for edge in graph["edges"]],
            [("index", "target")],
        )
        self.assertEqual(graph["edges"][0]["links"][0]["resolved_path"], "docs/de/Target Page.md")

    def test_graph_can_exclude_sitemap_nodes_and_edges(self) -> None:
        groups = {
            "a": {
                "de": [self.page("de", "a.md", "A", "a", "original", "[Sitemap](sitemap.md)\n")]
            },
            "sitemap": {
                "de": [self.page("de", "sitemap.md", "Sitemap", "sitemap", "original", "[A](a.md)\n")]
            },
        }
        graph = build_original_graph(["de"], groups, excluded_relative_paths={"sitemap.md"})

        self.assertEqual([node["id"] for node in graph["nodes"]], ["a"])
        self.assertEqual(graph["edges"], [])
        self.assertEqual(graph["summary"]["excluded_relative_paths"], ["sitemap.md"])

    def page(
        self,
        language: str,
        relative_path: str,
        title: str,
        translation_id: str,
        status: str,
        body: str,
    ) -> VaultPage:
        path = ROOT / "docs" / language / relative_path
        return VaultPage(
            path=path,
            rel_path=f"docs/{language}/{relative_path}",
            language=language,
            relative_path=relative_path,
            frontmatter=f"lang: {language}\ntitle: {title}\ntranslation_id: {translation_id}\ntranslation_status: {status}\n",
            body=body,
            has_frontmatter=True,
            translation_id=translation_id,
            translation_status=status,
            translation_source_lang=language if status == "original" else "",
            translation_source="",
            translation_source_hash="",
            title=title,
        )


if __name__ == "__main__":
    unittest.main()
