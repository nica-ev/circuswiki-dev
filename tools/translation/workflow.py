from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .markdown import join_markdown, split_markdown
from .metadata import ensure_scalars, missing_scalars, read_scalar, set_scalar


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
DEFAULT_MODEL = "google/gemini-2.0-flash-001"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
LANGUAGES = ("de", "en", "pl", "hu", "it", "nl", "el", "es", "uk")
DEFAULT_CONTEXT_DESCRIPTION = (
    "CircusWiki pages about circus pedagogy, movement games, inclusive practice, "
    "organizational documentation, and related educational material."
)
LANGUAGE_NAMES = {
    "de": "German",
    "en": "English",
    "pl": "Polish",
    "hu": "Hungarian",
    "it": "Italian",
    "nl": "Dutch",
    "el": "Greek",
    "es": "Spanish",
    "uk": "Ukrainian",
}
BATCH_TRANSLATION_EXCLUDED_RELATIVE_PATHS = {
    "sitemap.md",
}
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()(?P<target>[^)\s]+(?:\s+\"[^\"]*\")?)(\))")
WIKILINK_RE = re.compile(r"(!?\[\[)(?P<body>[^\]]+)(\]\])")
LOCAL_LINK_RE = re.compile(r"^(?![a-z][a-z0-9+.-]*:|#|/|mailto:)(?P<path>[^#?]+?\.md)(?P<suffix>[#?].*)?$", re.IGNORECASE)


def language_name(language: str) -> str:
    return LANGUAGE_NAMES.get(language, language)


@dataclass(frozen=True)
class PageStatus:
    source: str
    target: str
    translation_id: str
    source_hash: str
    target_exists: bool
    needs_translation: bool
    issues: list[str]


@dataclass(frozen=True)
class VaultPage:
    path: Path
    rel_path: str
    language: str
    relative_path: str
    frontmatter: str
    body: str
    has_frontmatter: bool
    translation_id: str
    translation_status: str
    translation_source_lang: str
    translation_source: str
    translation_source_hash: str
    title: str


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def language_path(path: str | Path, source_lang: str, target_lang: str) -> Path:
    source = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path)
    source_root = (DOCS / source_lang).resolve()
    target_root = (DOCS / target_lang).resolve()
    relative = source.resolve().relative_to(source_root)
    return target_root / relative


def list_languages() -> list[str]:
    configured = [language for language in LANGUAGES if (DOCS / language).exists()]
    extra = sorted(
        path.name
        for path in DOCS.iterdir()
        if path.is_dir() and path.name != "img" and path.name not in configured
    )
    return configured + extra


def list_sources(source_lang: str = "de") -> list[str]:
    source_root = DOCS / source_lang
    return sorted(
        rel(path)
        for path in source_root.rglob("*.md")
        if path.is_file()
    )


def source_hash(frontmatter: str, body: str) -> str:
    translation_id = read_scalar(frontmatter, "translation_id") or ""
    payload = f"translation_id={translation_id}\n\n{body}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def derive_translation_id(path: Path) -> str:
    stem = path.stem.lower()
    return (
        stem.replace(" ", "-")
        .replace("_", "-")
        .replace(".", "-")
        .strip("-")
    )


def derive_translation_id_from_relative(relative_path: str) -> str:
    return Path(relative_path).with_suffix("").as_posix()


def read_vault_page(path: Path, language: str) -> VaultPage:
    document = split_markdown(path.read_text(encoding="utf-8"))
    relative_path = path.relative_to(DOCS / language).as_posix()
    translation_id = read_scalar(document.frontmatter, "translation_id")
    return VaultPage(
        path=path,
        rel_path=rel(path),
        language=language,
        relative_path=relative_path,
        frontmatter=document.frontmatter,
        body=document.body,
        has_frontmatter=document.has_frontmatter,
        translation_id=translation_id or derive_translation_id_from_relative(relative_path),
        translation_status=read_scalar(document.frontmatter, "translation_status") or "",
        translation_source_lang=read_scalar(document.frontmatter, "translation_source_lang") or "",
        translation_source=read_scalar(document.frontmatter, "translation_source") or "",
        translation_source_hash=read_scalar(document.frontmatter, "translation_source_hash") or "",
        title=read_scalar(document.frontmatter, "title") or path.stem,
    )


def discover_vault_pages() -> tuple[list[str], dict[str, dict[str, list[VaultPage]]]]:
    languages = list_languages()
    groups: dict[str, dict[str, list[VaultPage]]] = {}

    for language in languages:
        language_root = DOCS / language
        for markdown_file in language_root.rglob("*.md"):
            page = read_vault_page(markdown_file, language)
            groups.setdefault(page.translation_id, {}).setdefault(language, []).append(page)

    return languages, groups


def find_group_source_language(pages_by_language: dict[str, list[VaultPage]]) -> str:
    for language, pages in pages_by_language.items():
        if any(page.translation_status == "original" for page in pages):
            return language

    for pages in pages_by_language.values():
        for page in pages:
            if page.translation_source_lang and page.translation_source_lang in pages_by_language:
                return page.translation_source_lang

    for pages in pages_by_language.values():
        for page in pages:
            source = page.translation_source
            if source.startswith("docs/"):
                parts = source.split("/")
                if len(parts) > 2 and parts[1] in pages_by_language:
                    return parts[1]

    if "de" in pages_by_language:
        return "de"
    if "en" in pages_by_language:
        return "en"
    return next(iter(pages_by_language))


def primary_page(pages: list[VaultPage]) -> VaultPage:
    originals = [page for page in pages if page.translation_status == "original"]
    if originals:
        return originals[0]
    return pages[0]


def vault_health_matrix() -> dict[str, object]:
    languages, groups = discover_vault_pages()
    rows: list[dict[str, object]] = []
    totals = {"green": 0, "yellow": 0, "red": 0}

    for translation_id in sorted(groups):
        pages_by_language = groups[translation_id]
        source_lang = find_group_source_language(pages_by_language)
        source_pages = pages_by_language.get(source_lang) or []
        source_page = primary_page(source_pages) if source_pages else None
        source_hash_value = (
            source_hash(source_page.frontmatter, source_page.body)
            if source_page
            else ""
        )

        title = (
            source_page.title
            if source_page
            else primary_page(next(iter(pages_by_language.values()))).title
        )
        relative_path = (
            source_page.relative_path
            if source_page
            else primary_page(next(iter(pages_by_language.values()))).relative_path
        )
        cells: dict[str, dict[str, object]] = {}

        for language in languages:
            pages = pages_by_language.get(language, [])
            issues: list[str] = []
            page = primary_page(pages) if pages else None

            if not page:
                cells[language] = {
                    "status": "red",
                    "exists": False,
                    "path": "",
                    "relative_path": relative_path,
                    "issues": ["missing_file"],
                }
                totals["red"] += 1
                continue

            if len(pages) > 1:
                issues.append("duplicate_translation_id_in_language")
            if not page.has_frontmatter:
                issues.append("missing_frontmatter")
            if not read_scalar(page.frontmatter, "translation_id"):
                issues.append("missing_translation_id")
            if page.language != read_scalar(page.frontmatter, "lang"):
                issues.append("lang_mismatch")
            if page.relative_path != relative_path:
                issues.append("relative_path_mismatch")

            if language == source_lang:
                if page.translation_status != "original":
                    issues.append("source_status_not_original")
                if page.translation_source_lang and page.translation_source_lang != source_lang:
                    issues.append("source_lang_mismatch")
                if not page.translation_source_lang:
                    issues.append("source_missing_translation_source_lang")
            else:
                required = [
                    "translation_source",
                    "translation_source_lang",
                    "translation_source_hash",
                    "translation_model",
                    "translation_status",
                    "translation_updated",
                ]
                for key in missing_scalars(page.frontmatter, required):
                    issues.append(f"missing_{key}")
                if page.translation_source_lang and page.translation_source_lang != source_lang:
                    issues.append("translation_source_lang_mismatch")
                if page.translation_source_hash and page.translation_source_hash != source_hash_value:
                    issues.append("source_hash_mismatch")
                if page.translation_status == "missing-translation":
                    issues.append("fallback_page")

            status = "green" if not issues else "yellow"
            totals[status] += 1
            cells[language] = {
                "status": status,
                "exists": True,
                "path": page.rel_path,
                "relative_path": page.relative_path,
                "issues": issues,
            }

        row_issues = sum(len(cell["issues"]) for cell in cells.values())
        missing = sum(1 for cell in cells.values() if cell["status"] == "red")
        rows.append(
            {
                "translation_id": translation_id,
                "title": title,
                "relative_path": relative_path,
                "source_lang": source_lang,
                "issues": row_issues,
                "missing": missing,
                "cells": cells,
            }
        )

    return {
        "languages": languages,
        "language_names": {language: language_name(language) for language in languages},
        "total_notes": len(rows),
        "totals": totals,
        "rows": rows,
    }


def repair_vault_metadata(path: str | Path) -> dict[str, object]:
    target = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    target.relative_to(ROOT)
    if not target.is_file() or target.suffix.lower() != ".md":
        raise FileNotFoundError(f"Not a Markdown file: {path}")

    language = target.relative_to(DOCS).parts[0]
    page = read_vault_page(target, language)
    _languages, groups = discover_vault_pages()
    pages_by_language = groups.get(page.translation_id)
    if not pages_by_language:
        return {"path": rel(target), "changed": False, "changes": [], "remaining": ["group_not_found"]}

    source_lang = find_group_source_language(pages_by_language)
    source_pages = pages_by_language.get(source_lang) or []
    source_page = primary_page(source_pages) if source_pages else None
    changes: list[str] = []
    skipped: list[str] = []
    frontmatter = page.frontmatter

    def assign(key: str, value: str, reason: str) -> None:
        nonlocal frontmatter
        if read_scalar(frontmatter, key) != value:
            frontmatter = set_scalar(frontmatter, key, value)
            changes.append(reason)

    assign("lang", language, "set_lang_from_folder")
    assign("translation_id", page.translation_id, "set_translation_id")

    if language == source_lang:
        assign("translation_status", "original", "set_source_status_original")
        assign("translation_source_lang", source_lang, "set_source_language")
    else:
        assign("translation_source_lang", source_lang, "set_translation_source_language")
        if source_page:
            assign("translation_source", source_page.rel_path, "set_translation_source")
        if not read_scalar(frontmatter, "translation_status"):
            assign("translation_status", "needs-review", "set_missing_translation_status")

        # Do not fabricate quality-sensitive provenance. A missing or mismatched
        # source hash/model/timestamp should stay visible until translation is rerun
        # or manually reviewed.
        for key in ("translation_source_hash", "translation_model", "translation_updated"):
            if not read_scalar(frontmatter, key):
                skipped.append(f"missing_{key}")

    if frontmatter != page.frontmatter:
        output = join_markdown(frontmatter, page.body)
        target.write_text(output, encoding="utf-8", newline="\n")

    updated = read_vault_page(target, language)
    remaining = deterministic_repair_remaining_issues(updated, source_lang, source_page)
    return {
        "path": rel(target),
        "changed": bool(changes),
        "changes": changes,
        "skipped": skipped,
        "remaining": remaining,
    }


def deterministic_repair_remaining_issues(
    page: VaultPage,
    source_lang: str,
    source_page: VaultPage | None,
) -> list[str]:
    issues: list[str] = []
    if read_scalar(page.frontmatter, "lang") != page.language:
        issues.append("lang_mismatch")
    if not read_scalar(page.frontmatter, "translation_id"):
        issues.append("missing_translation_id")

    if page.language == source_lang:
        if read_scalar(page.frontmatter, "translation_status") != "original":
            issues.append("source_status_not_original")
        if read_scalar(page.frontmatter, "translation_source_lang") != source_lang:
            issues.append("source_lang_mismatch")
        return issues

    if read_scalar(page.frontmatter, "translation_source_lang") != source_lang:
        issues.append("translation_source_lang_mismatch")
    if source_page and read_scalar(page.frontmatter, "translation_source") != source_page.rel_path:
        issues.append("translation_source_mismatch")
    for key in ("translation_source_hash", "translation_model", "translation_updated"):
        if not read_scalar(page.frontmatter, key):
            issues.append(f"missing_{key}")
    return issues


def batch_translation_plan(
    target_lang: str,
    max_files: int,
) -> dict[str, object]:
    if max_files < 1:
        raise ValueError("max_files must be at least 1")

    languages, groups = discover_vault_pages()
    if target_lang not in languages:
        raise ValueError(f"Unknown target language: {target_lang}")

    candidates: list[dict[str, object]] = []
    skipped: list[dict[str, str]] = []

    for translation_id in sorted(groups):
        pages_by_language = groups[translation_id]
        source_lang = find_group_source_language(pages_by_language)
        if source_lang == target_lang:
            skipped.append({"translation_id": translation_id, "reason": "target_is_source"})
            continue

        source_pages = pages_by_language.get(source_lang) or []
        if not source_pages:
            skipped.append({"translation_id": translation_id, "reason": "missing_source"})
            continue

        source_page = primary_page(source_pages)
        excluded_reason = batch_translation_exclusion_reason(source_page)
        if excluded_reason:
            skipped.append({"translation_id": translation_id, "reason": excluded_reason})
            continue

        target_pages = pages_by_language.get(target_lang) or []
        target_page = primary_page(target_pages) if target_pages else None
        reason = translation_candidate_reason(source_page, target_page, source_lang)
        if not reason:
            skipped.append({"translation_id": translation_id, "reason": "not_translation_candidate"})
            continue

        candidates.append(
            {
                "translation_id": translation_id,
                "title": source_page.title,
                "source_lang": source_lang,
                "source_language": language_name(source_lang),
                "target_lang": target_lang,
                "target_language": language_name(target_lang),
                "source_path": source_page.rel_path,
                "target_path": rel(language_path(source_page.path, source_lang, target_lang)),
                "source_chars": len(source_page.body),
                "reason": reason,
            }
        )

    limited = candidates[:max_files]
    return {
        "target_lang": target_lang,
        "target_language": language_name(target_lang),
        "max_files": max_files,
        "total_candidates": len(candidates),
        "planned_count": len(limited),
        "total_source_chars": sum(int(item["source_chars"]) for item in limited),
        "candidates": limited,
        "skipped_count": len(skipped),
    }


def batch_translation_exclusion_reason(source_page: VaultPage) -> str | None:
    if source_page.relative_path in BATCH_TRANSLATION_EXCLUDED_RELATIVE_PATHS:
        return "excluded_generated_index_page"
    return None


def translation_candidate_reason(
    source_page: VaultPage,
    target_page: VaultPage | None,
    source_lang: str,
) -> str | None:
    if target_page is None:
        return "missing_file"

    if target_page.translation_status == "missing-translation":
        return "fallback_page"

    current_hash = source_hash(source_page.frontmatter, source_page.body)
    if target_page.translation_source_hash and target_page.translation_source_hash != current_hash:
        return "source_hash_mismatch"

    if not target_page.translation_source_hash:
        return "missing_source_hash"

    if target_page.translation_source_lang and target_page.translation_source_lang != source_lang:
        return "translation_source_lang_mismatch"

    return None


def translate_batch_item(
    source_path: str,
    source_lang: str,
    target_lang: str,
    model: str | None = None,
    prompt: str | None = None,
) -> dict[str, object]:
    return translate_page(
        source_path=source_path,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        prompt=prompt,
        dry_run=False,
    )


def inspect_page(
    source_path: str | Path,
    source_lang: str = "de",
    target_lang: str = "en",
) -> PageStatus:
    source = (ROOT / source_path).resolve()
    target = language_path(source, source_lang, target_lang)
    source_doc = split_markdown(source.read_text(encoding="utf-8"))
    issues: list[str] = []

    if not source_doc.has_frontmatter:
        issues.append("source_missing_frontmatter")

    translation_id = read_scalar(source_doc.frontmatter, "translation_id")
    if not translation_id:
        translation_id = derive_translation_id(source)
        issues.append("source_missing_translation_id")

    if read_scalar(source_doc.frontmatter, "lang") != source_lang:
        issues.append("source_lang_mismatch")

    current_hash = source_hash(source_doc.frontmatter, source_doc.body)
    target_exists = target.exists()
    needs_translation = not target_exists

    if target_exists:
        target_doc = split_markdown(target.read_text(encoding="utf-8"))
        if not target_doc.has_frontmatter:
            issues.append("target_missing_frontmatter")
            needs_translation = True
        else:
            if read_scalar(target_doc.frontmatter, "lang") != target_lang:
                issues.append("target_lang_mismatch")
            if read_scalar(target_doc.frontmatter, "translation_id") != translation_id:
                issues.append("translation_id_mismatch")
            if read_scalar(target_doc.frontmatter, "translation_source_hash") != current_hash:
                issues.append("target_outdated")
                needs_translation = True
            missing = missing_scalars(
                target_doc.frontmatter,
                [
                    "translation_source",
                    "translation_source_lang",
                    "translation_source_hash",
                    "translation_model",
                    "translation_status",
                    "translation_updated",
                ],
            )
            for key in missing:
                issues.append(f"target_missing_{key}")

    return PageStatus(
        source=rel(source),
        target=rel(target),
        translation_id=translation_id,
        source_hash=current_hash,
        target_exists=target_exists,
        needs_translation=needs_translation,
        issues=issues,
    )


def health_summary(source_lang: str = "de", target_lang: str = "en") -> dict[str, object]:
    pages = [inspect_page(path, source_lang, target_lang) for path in list_sources(source_lang)]
    return {
        "source_lang": source_lang,
        "target_lang": target_lang,
        "total": len(pages),
        "translated": sum(1 for page in pages if page.target_exists),
        "needs_translation": sum(1 for page in pages if page.needs_translation),
        "with_issues": sum(1 for page in pages if page.issues),
        "pages": [page.__dict__ for page in pages],
    }


def translate_page(
    source_path: str | Path,
    source_lang: str = "de",
    target_lang: str = "en",
    model: str | None = None,
    prompt: str | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
    model = model or default_model()
    source = (ROOT / source_path).resolve()
    target = language_path(source, source_lang, target_lang)
    source_doc = split_markdown(source.read_text(encoding="utf-8"))
    translation_id = read_scalar(source_doc.frontmatter, "translation_id") or derive_translation_id(source)
    current_hash = source_hash(source_doc.frontmatter, source_doc.body)

    translated_body = call_translation_model(
        body=source_doc.body,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        prompt=prompt,
    )
    translated_body = restore_internal_link_targets(source_doc.body, translated_body)

    target_frontmatter = source_doc.frontmatter
    target_frontmatter = ensure_scalars(
        target_frontmatter,
        {
            "lang": target_lang,
            "translation_id": translation_id,
            "translation_source": rel(source),
            "translation_source_lang": source_lang,
            "translation_source_hash": current_hash,
            "translation_model": model,
            "translation_status": "machine-translated",
            "translation_updated": datetime.now(UTC).isoformat(timespec="seconds"),
        },
    )

    output = join_markdown(target_frontmatter, translated_body)
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8", newline="\n")

    return {
        "source": rel(source),
        "target": rel(target),
        "model": model,
        "dry_run": dry_run,
        "source_hash": current_hash,
        "translated_chars": len(translated_body),
    }


def restore_internal_link_targets(source_body: str, translated_body: str) -> str:
    translated_body = restore_markdown_link_targets(source_body, translated_body)
    translated_body = restore_wikilink_targets(source_body, translated_body)
    return translated_body


def restore_markdown_link_targets(source_body: str, translated_body: str) -> str:
    source_targets = [
        match.group("target")
        for match in MARKDOWN_LINK_RE.finditer(source_body)
        if is_local_markdown_target(match.group("target"))
    ]
    if not source_targets:
        return translated_body

    index = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal index
        current = match.group("target")
        if not is_local_markdown_target(current):
            return match.group(0)
        if index >= len(source_targets):
            return match.group(0)
        target = source_targets[index]
        index += 1
        return f"{match.group(1)}{target}{match.group(3)}"

    return MARKDOWN_LINK_RE.sub(replace, translated_body)


def restore_wikilink_targets(source_body: str, translated_body: str) -> str:
    source_targets = [
        wikilink_target(match.group("body"))
        for match in WIKILINK_RE.finditer(source_body)
        if wikilink_target(match.group("body"))
    ]
    if not source_targets:
        return translated_body

    index = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal index
        if index >= len(source_targets):
            return match.group(0)
        source_target = source_targets[index]
        index += 1
        body = match.group("body")
        alias = wikilink_alias(body)
        return f"{match.group(1)}{source_target}{alias}{match.group(3)}"

    return WIKILINK_RE.sub(replace, translated_body)


def is_local_markdown_target(target: str) -> bool:
    return bool(LOCAL_LINK_RE.match(target.split(None, 1)[0]))


def wikilink_target(body: str) -> str:
    target = body.split("|", 1)[0].strip()
    return target


def wikilink_alias(body: str) -> str:
    if "|" not in body:
        return ""
    return "|" + body.split("|", 1)[1]


def call_translation_model(
    body: str,
    source_lang: str,
    target_lang: str,
    model: str,
    prompt: str | None = None,
) -> str:
    load_local_env()
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY or OPENAI_API_KEY")

    base_url = os.getenv("OPENROUTER_BASE_URL") or os.getenv("OPENAI_BASE_URL") or DEFAULT_BASE_URL
    url = chat_completions_url(base_url)
    system_prompt = render_prompt(prompt, source_lang, target_lang)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": body},
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/nica-ev/circuswiki",
            "X-Title": "CircusWiki Translation Console",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Translation API request failed with HTTP {exc.code} for {url}: {details}"
        ) from exc

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected translation response: {data}") from exc

    return strip_code_fences(content).strip() + "\n"


def chat_completions_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/chat/completions"):
        return normalized
    return normalized + "/chat/completions"


def load_local_env() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def default_model() -> str:
    load_local_env()
    return os.getenv("OPENROUTER_MODEL") or DEFAULT_MODEL


def default_prompt(source_lang: str, target_lang: str) -> str:
    return render_prompt(None, source_lang, target_lang)


def default_prompt_template() -> str:
    return """You are an expert {source_language}-to-{target_language} translator and localization specialist. Your mission is to translate {source_language} text into {target_language} that is not just grammatically correct, but also completely natural, idiomatic, and clear, as if it were originally written by a native {target_language} speaker for a {target_language} audience.

Guiding Principles:
1. **Clarity is paramount.** The reader must understand the text's meaning and intent without any confusion.
2. **Natural flow over literal accuracy.** You must restructure sentences and choose different words to make the text sound natural in {target_language}.
3. **Context is key.** You must understand the purpose of the text (e.g., game rules, marketing copy, technical description) and adapt your translation accordingly. The context for this text is: {context_description}

Strict Translation Rules:
1. **AVOID "SOURCE-ISMS":** You must actively identify and eliminate calques (word-for-word translations of {source_language} structures). Do not mirror {source_language} sentence structure, word order, or unique grammatical features. Rephrase the entire idea using natural {target_language} syntax.
2. **LOGICAL INFERENCE FOR INSTRUCTIONS:** When translating instructions, rules, or procedures, you must validate their logic. If a literal translation results in a nonsensical or illogical instruction in {target_language}, you are required to infer the true, logical intent and translate that intent instead.
3. **USE ACTIVE & IDIOMATIC VERBS:** Prefer natural {target_language} verbal constructions over awkward noun phrases common in literal translations. For example, a direct translation might produce a clunky noun phrase, but the goal is to find the fluid, verb-centric equivalent in {target_language}.
4. **ADAPT IDIOMS:** Never translate {source_language} idioms or colloquialisms literally. Find the closest functional equivalent in {target_language} or rephrase the meaning plainly if no direct equivalent exists.

Markdown and Structure Rules:
1. Return only translated Markdown body content.
2. Preserve Markdown structure, headings, tables, admonitions, comments, code blocks, links, image links, and Obsidian wikilinks.
3. Translate natural language text only.
4. Do not translate file names, URLs, anchors, image paths, YAML, HTML attributes, IDs, placeholders, or code.
5. Keep formatting intact.

Output Format Constraint:
Your response MUST contain ONLY the final, translated {target_language} text. Do not include any titles, headers, notes, explanations, or any other text before or after the translation. Your entire output is the translation itself."""


def render_prompt(prompt: str | None, source_lang: str, target_lang: str) -> str:
    template = prompt or default_prompt_template()
    source_language = LANGUAGE_NAMES.get(source_lang, source_lang)
    target_language = LANGUAGE_NAMES.get(target_lang, target_lang)
    replacements = {
        "{source_lang}": source_lang,
        "{target_lang}": target_lang,
        "{source_language}": source_language,
        "{target_language}": target_language,
        "{SOURCE_LANGUAGE}": source_language,
        "{TARGET_LANGUAGE}": target_language,
        "{{SOURCE_LANGUAGE}}": source_language,
        "{{TARGET_LANGUAGE}}": target_language,
        "{context_description}": DEFAULT_CONTEXT_DESCRIPTION,
        "{CONTEXT_DESCRIPTION}": DEFAULT_CONTEXT_DESCRIPTION,
        "{{CONTEXT_DESCRIPTION}}": DEFAULT_CONTEXT_DESCRIPTION,
    }
    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        lines = stripped.splitlines()
        return "\n".join(lines[1:-1])
    return text
