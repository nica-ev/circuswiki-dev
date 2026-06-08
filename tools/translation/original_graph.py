from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from core.languages import language_name
from translation.workflow import (
    DOCS,
    ROOT,
    WIKILINK_RE,
    VaultPage,
    discover_vault_pages,
    find_group_source_language,
    primary_page,
    rel,
    wikilink_target,
)


FENCE_RE = re.compile(r"^\s*(```|~~~)")
MARKDOWN_LINK_RE = re.compile(
    r"(!?\[[^\]]*\]\()(?P<target><[^>]+>|[^)\s]+(?:\s+\"[^\"]*\")?)(\))"
)
DEFAULT_EXCLUDED_RELATIVE_PATHS = {"sitemap.md"}


def original_graph(exclude_sitemap: bool = True) -> dict[str, object]:
    languages, groups = discover_vault_pages()
    excluded = DEFAULT_EXCLUDED_RELATIVE_PATHS if exclude_sitemap else set()
    return build_original_graph(languages, groups, excluded_relative_paths=excluded)


def build_original_graph(
    languages: list[str],
    groups: dict[str, dict[str, list[VaultPage]]],
    excluded_relative_paths: set[str] | None = None,
) -> dict[str, object]:
    excluded_relative_paths = excluded_relative_paths or set()
    originals, diagnostics = canonical_originals(groups)
    if excluded_relative_paths:
        originals = {
            translation_id: page
            for translation_id, page in originals.items()
            if page.relative_path not in excluded_relative_paths
        }
    page_to_group = page_group_index(groups)
    resolver = LinkResolver(groups)
    edge_map: dict[tuple[str, str], dict[str, object]] = {}

    for source_id, source_page in originals.items():
        for link in extract_explicit_links(source_page.body):
            target_page = resolver.resolve(source_page, link["target"])
            if not target_page:
                diagnostics.append(
                    diagnostic(
                        "unresolved_link",
                        source_page,
                        f"Could not resolve link target: {link['target']}",
                        {"target": link["target"], "link_type": link["type"]},
                    )
                )
                continue

            target_id = page_to_group.get(target_page.rel_path)
            if not target_id:
                diagnostics.append(
                    diagnostic(
                        "target_without_group",
                        source_page,
                        f"Resolved target has no translation group: {target_page.rel_path}",
                        {"target": link["target"], "resolved_path": target_page.rel_path},
                    )
                )
                continue
            if target_id not in originals and target_page.relative_path in excluded_relative_paths:
                continue
            if target_id not in originals:
                diagnostics.append(
                    diagnostic(
                        "target_without_original",
                        source_page,
                        f"Target group has no canonical original: {target_id}",
                        {"target": link["target"], "target_id": target_id},
                    )
                )
                continue
            if source_id == target_id:
                continue

            key = (source_id, target_id)
            edge = edge_map.setdefault(
                key,
                {
                    "source": source_id,
                    "target": target_id,
                    "value": 0,
                    "links": [],
                },
            )
            edge["value"] = int(edge["value"]) + 1
            edge["links"].append(
                {
                    "type": link["type"],
                    "target": link["target"],
                    "resolved_path": target_page.rel_path,
                    "resolved_lang": target_page.language,
                }
            )

    nodes = [
        graph_node(translation_id, page, edge_map)
        for translation_id, page in sorted(originals.items())
    ]
    edges = sorted(edge_map.values(), key=lambda item: (str(item["source"]), str(item["target"])))
    language_counts: dict[str, int] = {}
    for page in originals.values():
        language_counts[page.language] = language_counts.get(page.language, 0) + 1

    return {
        "nodes": nodes,
        "edges": edges,
        "categories": [
            {"name": language, "label": language_name(language)}
            for language in languages
            if language_counts.get(language)
        ],
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "diagnostic_count": len(diagnostics),
            "language_counts": language_counts,
            "excluded_relative_paths": sorted(excluded_relative_paths),
        },
        "diagnostics": diagnostics,
    }


def canonical_originals(
    groups: dict[str, dict[str, list[VaultPage]]],
) -> tuple[dict[str, VaultPage], list[dict[str, object]]]:
    originals: dict[str, VaultPage] = {}
    diagnostics: list[dict[str, object]] = []

    for translation_id, pages_by_language in sorted(groups.items()):
        explicit_originals = [
            page
            for pages in pages_by_language.values()
            for page in pages
            if page.translation_status == "original"
        ]
        if len(explicit_originals) > 1:
            diagnostics.append(
                {
                    "type": "multiple_originals",
                    "translation_id": translation_id,
                    "message": f"Multiple original pages for translation group: {translation_id}",
                    "paths": [page.rel_path for page in explicit_originals],
                }
            )

        source_lang = find_group_source_language(pages_by_language)
        source_pages = pages_by_language.get(source_lang) or []
        if source_pages:
            originals[translation_id] = primary_page(source_pages)
            continue

        fallback_pages = next(iter(pages_by_language.values()), [])
        if fallback_pages:
            originals[translation_id] = primary_page(fallback_pages)
            diagnostics.append(
                diagnostic(
                    "missing_canonical_source",
                    originals[translation_id],
                    f"Used fallback page as graph original for: {translation_id}",
                )
            )

    return originals, diagnostics


def graph_node(
    translation_id: str,
    page: VaultPage,
    edge_map: dict[tuple[str, str], dict[str, object]],
) -> dict[str, object]:
    in_degree = sum(1 for (_source, target) in edge_map if target == translation_id)
    out_degree = sum(1 for (source, _target) in edge_map if source == translation_id)
    return {
        "id": translation_id,
        "name": translation_id,
        "title": page.title,
        "lang": page.language,
        "language": language_name(page.language),
        "path": page.rel_path,
        "relative_path": page.relative_path,
        "category": page.language,
        "symbolSize": min(48, 16 + (in_degree + out_degree) * 3),
        "value": in_degree + out_degree,
        "in_degree": in_degree,
        "out_degree": out_degree,
    }


def page_group_index(groups: dict[str, dict[str, list[VaultPage]]]) -> dict[str, str]:
    index: dict[str, str] = {}
    for translation_id, pages_by_language in groups.items():
        for pages in pages_by_language.values():
            for page in pages:
                index[page.rel_path] = translation_id
    return index


def extract_explicit_links(body: str) -> list[dict[str, str]]:
    text = without_fenced_code(body)
    links: list[dict[str, str]] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        if match.group(1).startswith("!"):
            continue
        links.append({"type": "markdown", "target": clean_markdown_target(match.group("target"))})
    for match in WIKILINK_RE.finditer(text):
        if match.group(1).startswith("!"):
            continue
        target = wikilink_target(match.group("body"))
        if target:
            links.append({"type": "wikilink", "target": target})
    return links


def without_fenced_code(body: str) -> str:
    output: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            output.append("")
            continue
        output.append("" if in_fence else line)
    return "\n".join(output)


def clean_markdown_target(target: str) -> str:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        return target[1:-1].strip()
    if " " in target:
        path, maybe_title = target.split(" ", 1)
        if maybe_title.strip().startswith('"'):
            return path
    return target


class LinkResolver:
    def __init__(self, groups: dict[str, dict[str, list[VaultPage]]]) -> None:
        self.pages = [
            page
            for pages_by_language in groups.values()
            for pages in pages_by_language.values()
            for page in pages
        ]
        self.by_abs = {page.path.resolve(): page for page in self.pages}
        self.by_rel = {page.rel_path.lower(): page for page in self.pages}
        self.by_wikilink: dict[str, list[VaultPage]] = {}
        for page in self.pages:
            keys = {
                Path(page.relative_path).with_suffix("").as_posix().lower(),
                Path(page.relative_path).stem.lower(),
                page.title.lower(),
            }
            for key in keys:
                self.by_wikilink.setdefault(key, []).append(page)

    def resolve(self, source: VaultPage, raw_target: str) -> VaultPage | None:
        target = normalize_link_target(raw_target)
        if not target or is_non_content_target(target):
            return None
        if target.lower().endswith(".md") or target.startswith("docs/") or "/" in target:
            return self.resolve_path(source, target)
        return self.resolve_wikilink(source, target)

    def resolve_path(self, source: VaultPage, target: str) -> VaultPage | None:
        path_part = strip_anchor_query(target)
        path_part = unquote(path_part).replace("\\", "/")

        candidates: list[Path] = []
        if path_part.startswith("docs/"):
            candidates.append(ROOT / path_part)
        else:
            candidates.append(source.path.parent / path_part)
            candidates.append(DOCS / source.language / path_part)
            candidates.append(ROOT / path_part)

        for candidate in candidates:
            page = self.by_abs.get(candidate.resolve())
            if page:
                return page
        return self.resolve_wikilink(source, Path(path_part).with_suffix("").as_posix())

    def resolve_wikilink(self, source: VaultPage, target: str) -> VaultPage | None:
        key = strip_anchor_query(target).replace("\\", "/").strip().lower()
        key = Path(key).with_suffix("").as_posix().lower()
        matches = self.by_wikilink.get(key, [])
        if not matches:
            return None

        same_language = [page for page in matches if page.language == source.language]
        if same_language:
            return sorted(same_language, key=lambda page: page.rel_path)[0]
        return sorted(matches, key=lambda page: page.rel_path)[0]


def normalize_link_target(target: str) -> str:
    return strip_anchor_query(target.strip())


def strip_anchor_query(target: str) -> str:
    return target.split("#", 1)[0].split("?", 1)[0].strip()


def is_non_content_target(target: str) -> bool:
    lowered = target.lower()
    return (
        not target
        or lowered.startswith(("http:", "https:", "mailto:", "#", "/"))
        or lowered.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf"))
    )


def diagnostic(
    kind: str,
    source_page: VaultPage,
    message: str,
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "type": kind,
        "translation_id": source_page.translation_id,
        "source_path": source_page.rel_path,
        "source_lang": source_page.language,
        "message": message,
    }
    if extra:
        payload.update(extra)
    return payload
