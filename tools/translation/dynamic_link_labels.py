from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from dynamic.blocks import parse_dynamic_blocks
from translation.link_repair import LinkRepairDiagnostic, LinkRepairResult, markdown_target_span, normalize_markdown_target
from translation.markdown import split_markdown
from translation.metadata import read_scalar


MARKDOWN_LINK_RE = re.compile(
    r"(?P<image>!?)"
    r"\[(?P<label>(?:\\.|[^\]\\])*)\]"
    r"\((?P<inner><[^>]+>|[^)]*)\)"
)


@dataclass(frozen=True)
class DynamicLabelRepair:
    body: str
    repair_count: int
    diagnostics: list[LinkRepairDiagnostic]

    def to_result(self, base_result: LinkRepairResult | None = None) -> LinkRepairResult:
        diagnostics = [*(base_result.diagnostics if base_result else []), *self.diagnostics]
        base_count = base_result.repair_count if base_result else 0
        base_body = base_result.body if base_result else self.body
        return LinkRepairResult(
            body=self.body,
            changed=self.body != base_body or bool(base_result and base_result.changed),
            repair_count=base_count + self.repair_count,
            diagnostics=diagnostics,
        )


def repair_dynamic_link_labels(
    page_path: Path,
    frontmatter: str,
    body: str,
    docs_root: Path,
) -> DynamicLabelRepair:
    if "dynamic" not in frontmatter_tags(frontmatter):
        return DynamicLabelRepair(body=body, repair_count=0, diagnostics=[])

    blocks = parse_dynamic_blocks(body)
    if not blocks:
        return DynamicLabelRepair(body=body, repair_count=0, diagnostics=[])

    language_root = page_language_root(page_path, docs_root)
    if language_root is None:
        return DynamicLabelRepair(body=body, repair_count=0, diagnostics=[])

    replacements: list[tuple[int, int, str, LinkRepairDiagnostic]] = []
    for block in blocks:
        content = body[block.content_start:block.content_end]
        for match in MARKDOWN_LINK_RE.finditer(content):
            if match.group("image"):
                continue
            parsed = markdown_target_span(match.group("inner"), block.content_start + match.start("inner"))
            if not parsed:
                continue
            raw_target = parsed[0]
            resolved = resolve_markdown_target(page_path, raw_target, docs_root)
            if not resolved or not same_language_path(resolved, language_root):
                continue
            title = page_title(resolved)
            if not title:
                continue
            label_start = block.content_start + match.start("label")
            label_end = block.content_start + match.end("label")
            current_label = match.group("label")
            replacement = escape_markdown_label(title)
            if current_label == replacement:
                continue
            replacements.append(
                (
                    label_start,
                    label_end,
                    replacement,
                    LinkRepairDiagnostic(
                        kind="dynamic_label_repaired",
                        link_type="markdown",
                        message="Dynamic generated link label was replaced with the linked page title.",
                        source_target=title,
                        translated_target=raw_target,
                    ),
                )
            )

    if not replacements:
        return DynamicLabelRepair(body=body, repair_count=0, diagnostics=[])

    output = body
    for start, end, replacement, _diagnostic in reversed(replacements):
        output = output[:start] + replacement + output[end:]
    return DynamicLabelRepair(
        body=output,
        repair_count=len(replacements),
        diagnostics=[diagnostic for *_span, diagnostic in replacements],
    )


def frontmatter_tags(frontmatter: str) -> list[str]:
    tags: list[str] = []
    lines = frontmatter.splitlines()
    in_tags = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("tags:"):
            in_tags = True
            value = stripped.split(":", 1)[1].strip()
            if value.startswith("[") and value.endswith("]"):
                tags.extend(clean_tag(part) for part in value[1:-1].split(","))
            elif value and value != "[]":
                tags.append(clean_tag(value))
            continue
        if in_tags and line.startswith((" ", "\t")) and stripped.startswith("-"):
            tags.append(clean_tag(stripped[1:]))
            continue
        if in_tags and stripped and not line.startswith((" ", "\t")):
            in_tags = False
    return sorted({tag for tag in tags if tag})


def clean_tag(value: str) -> str:
    return value.strip().strip('"\'').lstrip("#")


def page_language_root(page_path: Path, docs_root: Path) -> Path | None:
    try:
        relative = page_path.resolve().relative_to(docs_root.resolve())
    except ValueError:
        return None
    if len(relative.parts) < 2:
        return None
    return docs_root / relative.parts[0]


def same_language_path(path: Path, language_root: Path) -> bool:
    try:
        path.resolve().relative_to(language_root.resolve())
    except ValueError:
        return False
    return path.suffix.lower() == ".md"


def resolve_markdown_target(page_path: Path, raw_target: str, docs_root: Path) -> Path | None:
    target = normalize_markdown_target(raw_target)
    if "://" in target or target.startswith(("#", "/", "mailto:")):
        return None
    target = split_suffix(target)[0]
    target = unquote(target).replace("\\", "/")
    if target.startswith("./"):
        target = target[2:]
    candidate = (docs_root.parent / target).resolve() if target.startswith("docs/") else (page_path.parent / target).resolve()
    try:
        candidate.relative_to(docs_root.resolve())
    except ValueError:
        return None
    return candidate if candidate.is_file() and candidate.suffix.lower() == ".md" else None


def split_suffix(path: str) -> tuple[str, str]:
    indexes = [index for index in (path.find("#"), path.find("?")) if index != -1]
    if not indexes:
        return path, ""
    index = min(indexes)
    return path[:index], path[index:]


def page_title(path: Path) -> str:
    document = split_markdown(path.read_text(encoding="utf-8"))
    return read_scalar(document.frontmatter, "title") or ""


def escape_markdown_label(label: str) -> str:
    return label.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("|", "\\|").replace("\n", " ")
