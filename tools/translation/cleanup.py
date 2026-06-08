from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from translation.markdown import split_markdown
from translation.metadata import read_scalar
from translation.workflow import DOCS, ROOT, rel

DELETABLE_STATUSES = {"machine-translated", "missing-translation"}


@dataclass(frozen=True)
class OrphanTranslationItem:
    path: str
    language: str
    translation_id: str
    status: str
    source: str
    source_exists: bool
    reason: str
    deletable: bool
    detail: str


def scan_orphan_translations() -> dict[str, Any]:
    items = orphan_translation_items()
    counts: dict[str, int] = {}
    for item in items:
        counts[item.reason] = counts.get(item.reason, 0) + 1
    return {
        "ok": True,
        "total": len(items),
        "deletable_count": sum(1 for item in items if item.deletable),
        "counts": counts,
        "items": [asdict(item) for item in items],
    }


def delete_orphan_translations(paths: list[str]) -> dict[str, Any]:
    requested: set[str] = set()
    skipped: list[dict[str, Any]] = []
    for raw_path in paths:
        if not str(raw_path).strip():
            continue
        try:
            requested.add(normalize_rel_path(raw_path))
        except ValueError:
            skipped.append({"path": str(raw_path), "reason": "invalid_path"})

    current = {item.path: item for item in orphan_translation_items()}
    deleted: list[dict[str, Any]] = []

    for path in sorted(requested):
        item = current.get(path)
        if not item:
            skipped.append({"path": path, "reason": "not_current_orphan"})
            continue
        if not item.deletable:
            skipped.append({"path": path, "reason": "not_deletable", "item": asdict(item)})
            continue

        target = (ROOT / path).resolve()
        if not safe_docs_markdown_path(target):
            skipped.append({"path": path, "reason": "unsafe_path"})
            continue

        target.unlink()
        deleted.append(asdict(item))

    return {
        "ok": not skipped,
        "requested_count": len(requested),
        "deleted_count": len(deleted),
        "skipped_count": len(skipped),
        "deleted": deleted,
        "skipped": skipped,
    }


def delete_all_deletable_orphan_translations() -> dict[str, Any]:
    paths = [item.path for item in orphan_translation_items() if item.deletable]
    return delete_orphan_translations(paths)


def orphan_translation_items() -> list[OrphanTranslationItem]:
    items: list[OrphanTranslationItem] = []
    if not DOCS.exists():
        return items

    for path in sorted(DOCS.rglob("*.md")):
        try:
            item = inspect_translation_file(path)
        except Exception:
            continue
        if item:
            items.append(item)
    return items


def inspect_translation_file(path: Path) -> OrphanTranslationItem | None:
    if not safe_docs_markdown_path(path):
        return None

    language = path.relative_to(DOCS).parts[0]
    document = split_markdown(path.read_text(encoding="utf-8"))
    if not document.has_frontmatter:
        return None

    status = read_scalar(document.frontmatter, "translation_status") or ""
    if status == "original":
        return None

    translation_id = read_scalar(document.frontmatter, "translation_id") or ""
    source = read_scalar(document.frontmatter, "translation_source") or ""
    source_lang = read_scalar(document.frontmatter, "translation_source_lang") or ""

    if not status and not source:
        return None

    if not source:
        return orphan_item(
            path,
            language,
            translation_id,
            status,
            source,
            False,
            "missing_translation_source",
            status in DELETABLE_STATUSES,
            "Translated file has no translation_source metadata.",
        )

    source_path = (ROOT / source).resolve()
    source_exists = source_path.is_file()
    if not source_exists:
        return orphan_item(
            path,
            language,
            translation_id,
            status,
            source,
            False,
            "missing_translation_source_file",
            status in DELETABLE_STATUSES,
            "translation_source points to a missing file.",
        )

    if not safe_docs_markdown_path(source_path):
        return orphan_item(
            path,
            language,
            translation_id,
            status,
            source,
            True,
            "invalid_translation_source_path",
            False,
            "translation_source exists but is not a Markdown file under docs/<lang>/.",
        )

    source_doc = split_markdown(source_path.read_text(encoding="utf-8"))
    source_translation_id = read_scalar(source_doc.frontmatter, "translation_id") or ""
    if translation_id and source_translation_id and source_translation_id != translation_id:
        return orphan_item(
            path,
            language,
            translation_id,
            status,
            source,
            True,
            "source_translation_id_mismatch",
            False,
            f"Source translation_id is {source_translation_id!r}.",
        )

    actual_source_lang = source_path.relative_to(DOCS).parts[0]
    if source_lang and source_lang != actual_source_lang:
        return orphan_item(
            path,
            language,
            translation_id,
            status,
            source,
            True,
            "source_language_mismatch",
            False,
            f"Source path is under {actual_source_lang!r}.",
        )

    return None


def orphan_item(
    path: Path,
    language: str,
    translation_id: str,
    status: str,
    source: str,
    source_exists: bool,
    reason: str,
    deletable: bool,
    detail: str,
) -> OrphanTranslationItem:
    return OrphanTranslationItem(
        path=rel(path),
        language=language,
        translation_id=translation_id,
        status=status,
        source=source,
        source_exists=source_exists,
        reason=reason,
        deletable=deletable,
        detail=detail,
    )


def normalize_rel_path(path: str) -> str:
    target = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"Path is outside repository: {path}") from exc
    return rel(target)


def safe_docs_markdown_path(path: Path) -> bool:
    try:
        relative = path.resolve().relative_to(DOCS.resolve())
    except ValueError:
        return False
    return len(relative.parts) >= 2 and path.suffix.lower() == ".md"
