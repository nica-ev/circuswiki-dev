from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from translation.dynamic_link_labels import repair_dynamic_link_labels
from translation.link_repair import LinkRepairResult, repair_link_targets
from translation.markdown import join_markdown, split_markdown
from translation.metadata import read_scalar
from translation.workflow import DOCS, ROOT, rel


@dataclass(frozen=True)
class LinkRepairItem:
    path: str
    language: str
    translation_id: str
    status: str
    source: str
    source_exists: bool
    repair_count: int
    label_repair_count: int
    diagnostic_count: int
    safe_repair: bool
    reasons: list[str]


def scan_link_repairs(language: str = "") -> dict[str, Any]:
    items = link_repair_items(language)
    return {
        "ok": True,
        "total": len(items),
        "safe_count": sum(1 for item in items if item.safe_repair),
        "repair_count": sum(item.repair_count for item in items),
        "label_repair_count": sum(item.label_repair_count for item in items),
        "items": [asdict(item) for item in items],
    }


def preview_link_repair(path: str) -> dict[str, Any]:
    target = normalize_docs_markdown_path(path)
    source, document, result = repair_context(target)
    return {
        "ok": True,
        "path": rel(target),
        "source": rel(source),
        "safe_repair": is_safe_repair(result),
        "repair_count": result.repair_count,
        "label_repair_count": dynamic_label_repair_count(result),
        "diagnostics": [asdict(item) for item in result.diagnostics],
        "current_body": document.body,
        "repaired_body": result.body,
    }


def repair_link_files(paths: list[str]) -> dict[str, Any]:
    repaired: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for raw_path in paths:
        try:
            target = normalize_docs_markdown_path(raw_path)
            source, document, result = repair_context(target)
        except Exception as exc:
            skipped.append({"path": str(raw_path), "reason": str(exc)})
            continue

        if not is_safe_repair(result):
            skipped.append(
                {
                    "path": rel(target),
                    "reason": "not_safe_repair",
                    "repair_count": result.repair_count,
                    "diagnostics": [asdict(item) for item in result.diagnostics],
                }
            )
            continue

        target.write_text(join_markdown(document.frontmatter, result.body), encoding="utf-8", newline="\n")
        repaired.append(
            {
                "path": rel(target),
                "source": rel(source),
                "repair_count": result.repair_count,
                "label_repair_count": dynamic_label_repair_count(result),
            }
        )

    return {
        "ok": not skipped,
        "requested_count": len(paths),
        "repaired_count": len(repaired),
        "skipped_count": len(skipped),
        "repaired": repaired,
        "skipped": skipped,
    }


def repair_all_safe_link_files(language: str = "") -> dict[str, Any]:
    paths = [item.path for item in link_repair_items(language) if item.safe_repair]
    return repair_link_files(paths)


def link_repair_items(language: str = "") -> list[LinkRepairItem]:
    items: list[LinkRepairItem] = []
    if not DOCS.exists():
        return items

    roots = [DOCS / language] if language else [path for path in DOCS.iterdir() if path.is_dir()]
    for root in roots:
        if not root.exists() or root.name == "img":
            continue
        for path in sorted(root.rglob("*.md")):
            item = inspect_link_repair_file(path)
            if item:
                items.append(item)
    return items


def inspect_link_repair_file(path: Path) -> LinkRepairItem | None:
    if not safe_docs_markdown_path(path):
        return None

    document = split_markdown(path.read_text(encoding="utf-8"))
    if not document.has_frontmatter:
        return None

    status = read_scalar(document.frontmatter, "translation_status") or ""
    if status == "original":
        return None

    source = read_scalar(document.frontmatter, "translation_source") or ""
    if not source:
        return None

    language = path.relative_to(DOCS).parts[0]
    translation_id = read_scalar(document.frontmatter, "translation_id") or ""
    source_path = (ROOT / source).resolve()
    source_exists = source_path.is_file()
    if not source_exists:
        return LinkRepairItem(
            path=rel(path),
            language=language,
            translation_id=translation_id,
            status=status,
            source=source,
            source_exists=False,
            repair_count=0,
            label_repair_count=0,
            diagnostic_count=1,
            safe_repair=False,
            reasons=["missing_translation_source_file"],
        )

    if not safe_docs_markdown_path(source_path):
        return None

    source_document = split_markdown(source_path.read_text(encoding="utf-8"))
    result = combined_link_repair(path, document.frontmatter, source_document.body, document.body)
    reasons = sorted({item.kind for item in result.diagnostics})
    if not result.repair_count and not reasons:
        return None

    return LinkRepairItem(
        path=rel(path),
        language=language,
        translation_id=translation_id,
        status=status,
        source=source,
        source_exists=True,
        repair_count=result.repair_count,
        label_repair_count=dynamic_label_repair_count(result),
        diagnostic_count=len(result.diagnostics),
        safe_repair=is_safe_repair(result),
        reasons=reasons,
    )


def repair_context(path: Path) -> tuple[Path, Any, LinkRepairResult]:
    if not safe_docs_markdown_path(path):
        raise ValueError("Path is not a Markdown file under docs/<lang>/")

    document = split_markdown(path.read_text(encoding="utf-8"))
    if not document.has_frontmatter:
        raise ValueError("File has no frontmatter")
    if read_scalar(document.frontmatter, "translation_status") == "original":
        raise ValueError("Original files are not repaired by this tool")

    source = read_scalar(document.frontmatter, "translation_source") or ""
    if not source:
        raise ValueError("File has no translation_source")

    source_path = (ROOT / source).resolve()
    if not source_path.is_file():
        raise ValueError("translation_source points to a missing file")
    if not safe_docs_markdown_path(source_path):
        raise ValueError("translation_source is not under docs/<lang>/")

    source_document = split_markdown(source_path.read_text(encoding="utf-8"))
    return source_path, document, combined_link_repair(path, document.frontmatter, source_document.body, document.body)


def combined_link_repair(
    target_path: Path,
    target_frontmatter: str,
    source_body: str,
    target_body: str,
) -> LinkRepairResult:
    target_result = repair_link_targets(source_body, target_body)
    label_result = repair_dynamic_link_labels(
        page_path=target_path,
        frontmatter=target_frontmatter,
        body=target_result.body,
        docs_root=DOCS,
    )
    return label_result.to_result(target_result)


def dynamic_label_repair_count(result: LinkRepairResult) -> int:
    return sum(1 for item in result.diagnostics if item.kind == "dynamic_label_repaired")


def is_safe_repair(result: LinkRepairResult) -> bool:
    return result.repair_count > 0 and not any(item.kind == "link_count_mismatch" for item in result.diagnostics)


def normalize_docs_markdown_path(path: str) -> Path:
    target = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    if not safe_docs_markdown_path(target):
        raise ValueError("Path is not a Markdown file under docs/<lang>/")
    return target


def safe_docs_markdown_path(path: Path) -> bool:
    try:
        relative = path.resolve().relative_to(DOCS.resolve())
    except ValueError:
        return False
    return len(relative.parts) >= 2 and path.suffix.lower() == ".md"
