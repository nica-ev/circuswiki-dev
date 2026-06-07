from __future__ import annotations

import json
import os
import re
import tomllib
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from core.languages import default_language, language_name as registry_language_name, zensical_configs
from translation.markdown import split_markdown
from translation.metadata import read_scalar
from translation.workflow import (
    DEFAULT_BASE_URL,
    default_model,
    list_languages,
    load_local_env,
)

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
MODEL_PATH = ROOT / "tools" / "navigation" / "nav.json"
DEFAULT_LANGUAGE = default_language()
CONFIGS = zensical_configs()
NAV_BLOCK_RE = re.compile(r"(?ms)^nav\s*=\s*\[.*?^\]")
ID_RE = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class PageInfo:
    language: str
    relative_path: str
    title: str
    translation_id: str
    path: str


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def language_name(language: str) -> str:
    return registry_language_name(language)


def read_config_nav(language: str) -> list[dict[str, Any]]:
    path = CONFIGS[language]
    if not path.exists():
        return []
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return data.get("project", {}).get("nav", []) or []


def flatten_config_nav(nav: list[dict[str, Any]], prefix: str = "") -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for entry in nav:
        for label, value in entry.items():
            label_path = f"{prefix} / {label}" if prefix else str(label)
            if isinstance(value, str):
                items.append({"label": str(label), "label_path": label_path, "page": value})
            elif isinstance(value, list):
                items.extend(flatten_config_nav(value, label_path))
    return items


def nav_fingerprint(nav: list[dict[str, Any]]) -> str:
    flattened = flatten_config_nav(nav)
    return json.dumps(
        [{"label": item["label_path"], "page": item["page"]} for item in flattened],
        ensure_ascii=False,
        sort_keys=True,
    )


def read_page_info(path: Path, language: str) -> PageInfo:
    document = split_markdown(path.read_text(encoding="utf-8"))
    relative_path = path.relative_to(DOCS / language).as_posix()
    return PageInfo(
        language=language,
        relative_path=relative_path,
        title=read_scalar(document.frontmatter, "title") or path.stem,
        translation_id=read_scalar(document.frontmatter, "translation_id") or Path(relative_path).with_suffix("").as_posix(),
        path=rel(path),
    )


def discover_pages() -> dict[str, dict[str, PageInfo]]:
    pages: dict[str, dict[str, PageInfo]] = {}
    for language in list_languages():
        root = DOCS / language
        if not root.exists():
            continue
        for markdown_file in root.rglob("*.md"):
            page = read_page_info(markdown_file, language)
            pages.setdefault(language, {})[page.relative_path] = page
    return pages


def nav_model_exists() -> bool:
    return MODEL_PATH.exists()


def default_empty_model() -> dict[str, Any]:
    return {
        "version": 1,
        "updated": datetime.now(UTC).isoformat(timespec="seconds"),
        "description": "Canonical CircusWiki navigation model. Edit items, then preview/apply from the dev console.",
        "items": [],
    }


def load_nav_model() -> dict[str, Any]:
    if not MODEL_PATH.exists():
        return default_empty_model()
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def save_nav_model(model: dict[str, Any]) -> dict[str, Any]:
    validate_model(model)
    model = normalized_model(model)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return model


def validate_model(model: dict[str, Any]) -> None:
    if not isinstance(model, dict):
        raise ValueError("Navigation model must be a JSON object")
    items = model.get("items")
    if not isinstance(items, list):
        raise ValueError("Navigation model requires an items array")
    validate_items(items)


def validate_items(items: list[Any]) -> None:
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Navigation item must be an object")
        if not item.get("id"):
            raise ValueError("Navigation item is missing id")
        if not item.get("page") and not item.get("children"):
            raise ValueError(f"Navigation item {item.get('id')} needs page or children")
        children = item.get("children", [])
        if children:
            if not isinstance(children, list):
                raise ValueError(f"Navigation item {item.get('id')} children must be an array")
            validate_items(children)


def normalized_model(model: dict[str, Any]) -> dict[str, Any]:
    result = dict(model)
    result["version"] = int(result.get("version") or 1)
    result["updated"] = datetime.now(UTC).isoformat(timespec="seconds")
    result["items"] = normalize_items(result.get("items") or [])
    return result


def normalize_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in items:
        entry: dict[str, Any] = {"id": str(item["id"])}
        if item.get("page"):
            entry["page"] = normalize_page(str(item["page"]))
        labels = item.get("labels") or {}
        if isinstance(labels, dict) and labels:
            entry["labels"] = {str(key): str(value) for key, value in labels.items() if value}
        elif item.get("label"):
            entry["labels"] = {DEFAULT_LANGUAGE: str(item["label"])}
        children = item.get("children") or []
        if children:
            entry["children"] = normalize_items(children)
        normalized.append(entry)
    return normalized


def normalize_page(page: str) -> str:
    page = page.replace("\\", "/").strip()
    for language in list_languages():
        prefix = f"docs/{language}/"
        if page.startswith(prefix):
            page = page[len(prefix) :]
            break
    return page


def slug(value: str) -> str:
    value = value.lower().strip()
    value = ID_RE.sub("-", value).strip("-")
    return value or "nav-item"


def model_from_current_nav(language: str = DEFAULT_LANGUAGE) -> dict[str, Any]:
    nav = read_config_nav(language)
    pages = discover_pages()
    model = default_empty_model()
    model["source"] = f"current zensical nav ({language})"
    model["items"] = items_from_config_nav(nav, language, pages)
    return normalized_model(model)


def items_from_config_nav(
    nav: list[dict[str, Any]],
    language: str,
    pages: dict[str, dict[str, PageInfo]],
) -> list[dict[str, Any]]:
    used: set[str] = set()

    def unique_id(label: str, page: str | None) -> str:
        base = slug(Path(page).with_suffix("").as_posix() if page else label)
        candidate = base
        index = 2
        while candidate in used:
            candidate = f"{base}-{index}"
            index += 1
        used.add(candidate)
        return candidate

    def convert(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for entry in entries:
            for label, value in entry.items():
                if isinstance(value, str):
                    page = normalize_page(value)
                    item: dict[str, Any] = {
                        "id": unique_id(str(label), page),
                        "page": page,
                        "labels": {language: str(label)},
                    }
                    page_info = pages.get(language, {}).get(page)
                    if page_info and page_info.title and page_info.title != label:
                        item["title"] = page_info.title
                    result.append(item)
                elif isinstance(value, list):
                    result.append(
                        {
                            "id": unique_id(str(label), None),
                            "labels": {language: str(label)},
                            "children": convert(value),
                        }
                    )
        return result

    return convert(nav)


def nav_label(item: dict[str, Any], language: str, pages: dict[str, dict[str, PageInfo]]) -> str:
    labels = item.get("labels") or {}
    if labels.get(language):
        return str(labels[language])
    page = item.get("page")
    if page:
        page_info = pages.get(language, {}).get(page)
        if page_info:
            return page_info.title
    if labels.get(DEFAULT_LANGUAGE):
        return str(labels[DEFAULT_LANGUAGE])
    if page:
        page_info = pages.get(DEFAULT_LANGUAGE, {}).get(page)
        if page_info:
            return page_info.title
        return Path(page).stem
    return str(item.get("id", "Navigation"))


def nav_for_language(items: list[dict[str, Any]], language: str, pages: dict[str, dict[str, PageInfo]]) -> list[dict[str, Any]]:
    nav: list[dict[str, Any]] = []
    for item in items:
        label = nav_label(item, language, pages)
        children = item.get("children") or []
        if children:
            nav.append({label: nav_for_language(children, language, pages)})
        elif item.get("page"):
            nav.append({label: item["page"]})
    return nav


def format_nav_block(nav: list[dict[str, Any]]) -> str:
    lines = ["nav = ["]
    lines.extend(format_nav_entries(nav, 2))
    lines.append("]")
    return "\n".join(lines)


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def format_nav_entries(entries: list[dict[str, Any]], indent: int) -> list[str]:
    lines: list[str] = []
    prefix = " " * indent
    for entry in entries:
        for label, value in entry.items():
            if isinstance(value, str):
                lines.append(f"{prefix}{{ {toml_string(label)} = {toml_string(value)} }},")
            elif isinstance(value, list):
                lines.append(f"{prefix}{{ {toml_string(label)} = [")
                lines.extend(format_nav_entries(value, indent + 2))
                lines.append(f"{prefix}] }},")
    return lines


def render_model_navs(model: dict[str, Any] | None = None) -> dict[str, str]:
    model = normalized_model(model or load_nav_model())
    pages = discover_pages()
    rendered: dict[str, str] = {}
    for language in configured_languages():
        rendered[language] = format_nav_block(nav_for_language(model["items"], language, pages))
    return rendered


def configured_languages() -> list[str]:
    return [language for language in list_languages() if language in CONFIGS and CONFIGS[language].exists()]


def replace_nav_block(text: str, nav_block: str) -> str:
    if not NAV_BLOCK_RE.search(text):
        raise ValueError("Could not find nav block in config")
    return NAV_BLOCK_RE.sub(nav_block, text, count=1)


def apply_nav_model(model: dict[str, Any] | None = None, save_model: bool = True) -> dict[str, Any]:
    model = normalized_model(model or load_nav_model())
    if save_model:
        save_nav_model(model)
    rendered = render_model_navs(model)
    changed: list[str] = []
    for language, nav_block in rendered.items():
        path = CONFIGS[language]
        text = path.read_text(encoding="utf-8")
        updated = replace_nav_block(text, nav_block)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed.append(rel(path))
    return {"changed": changed, "changed_count": len(changed), "model_path": rel(MODEL_PATH)}


def duplicate_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def model_page_set(items: list[dict[str, Any]]) -> set[str]:
    pages: set[str] = set()
    for item in items:
        if item.get("page"):
            pages.add(str(item["page"]))
        pages.update(model_page_set(item.get("children") or []))
    return pages


def model_missing_targets(model: dict[str, Any], pages: dict[str, dict[str, PageInfo]]) -> list[dict[str, str]]:
    missing: list[dict[str, str]] = []
    for page in sorted(model_page_set(model.get("items") or [])):
        for language in configured_languages():
            if page not in pages.get(language, {}):
                missing.append({"language": language, "page": page, "status": "will_use_fallback_if_source_exists"})
    return missing


def nav_scan() -> dict[str, Any]:
    languages = configured_languages()
    pages = discover_pages()
    config_navs: dict[str, Any] = {}
    fingerprints: dict[str, list[str]] = {}

    for language in languages:
        nav = read_config_nav(language)
        flattened = flatten_config_nav(nav)
        fingerprint = nav_fingerprint(nav)
        fingerprints.setdefault(fingerprint, []).append(language)
        config_navs[language] = {
            "config": rel(CONFIGS[language]),
            "count": len(flattened),
            "items": flattened,
            "duplicate_pages": duplicate_values([item["page"] for item in flattened]),
            "duplicate_labels": duplicate_values([item["label_path"] for item in flattened]),
            "missing_files": [
                item for item in flattened if normalize_page(item["page"]) not in pages.get(language, {})
            ],
        }

    model = load_nav_model()
    model_pages = model_page_set(model.get("items") or [])
    default_pages = pages.get(DEFAULT_LANGUAGE, {})
    orphan_candidates = [
        {
            "page": page.relative_path,
            "title": page.title,
            "translation_id": page.translation_id,
        }
        for page in sorted(default_pages.values(), key=lambda item: item.relative_path.lower())
        if page.relative_path not in model_pages and not is_low_value_nav_candidate(page.relative_path)
    ]

    return {
        "languages": languages,
        "language_names": {language: language_name(language) for language in languages},
        "model_exists": nav_model_exists(),
        "model_path": rel(MODEL_PATH),
        "model": model,
        "configs": config_navs,
        "nav_variants": [
            {"languages": langs, "count": len(langs)} for langs in fingerprints.values()
        ],
        "has_multiple_navs": len(fingerprints) > 1,
        "model_missing_targets": model_missing_targets(model, pages),
        "orphan_candidate_count": len(orphan_candidates),
        "orphan_candidates": orphan_candidates[:80],
        "page_count_by_language": {language: len(pages.get(language, {})) for language in languages},
    }


def is_low_value_nav_candidate(relative_path: str) -> bool:
    path = relative_path.lower()
    return (
        path == "sitemap.md"
        or path == "tags.md"
        or path.startswith("blog/posts/")
        or path in {"test.md", "release notes.md"}
    )


def navigation_preview(model: dict[str, Any] | None = None) -> dict[str, Any]:
    model = normalized_model(model or load_nav_model())
    rendered = render_model_navs(model)
    current: dict[str, str] = {}
    changed: dict[str, bool] = {}
    for language, path in CONFIGS.items():
        if not path.exists() or language not in rendered:
            continue
        match = NAV_BLOCK_RE.search(path.read_text(encoding="utf-8"))
        current[language] = match.group(0) if match else ""
        changed[language] = current[language] != rendered[language]
    return {
        "model": model,
        "rendered": rendered,
        "changed": changed,
        "changed_count": sum(1 for value in changed.values() if value),
    }


def flattened_model_labels(
    items: list[dict[str, Any]],
    source_lang: str,
    pages: dict[str, dict[str, PageInfo]],
) -> list[dict[str, str]]:
    labels: list[dict[str, str]] = []
    for item in items:
        labels.append(
            {
                "id": str(item["id"]),
                "source_label": nav_label(item, source_lang, pages),
                "page": str(item.get("page") or ""),
            }
        )
        labels.extend(flattened_model_labels(item.get("children") or [], source_lang, pages))
    return labels


def set_model_label(items: list[dict[str, Any]], item_id: str, language: str, label: str) -> bool:
    for item in items:
        if item.get("id") == item_id:
            labels = item.setdefault("labels", {})
            if not isinstance(labels, dict):
                labels = {}
                item["labels"] = labels
            labels[language] = label
            return True
        if set_model_label(item.get("children") or [], item_id, language, label):
            return True
    return False


def translate_nav_labels(
    target_lang: str,
    model: dict[str, Any] | None = None,
    source_lang: str = DEFAULT_LANGUAGE,
    model_name: str | None = None,
) -> dict[str, Any]:
    if target_lang == source_lang:
        raise ValueError("Target language must differ from source language")
    if target_lang not in configured_languages():
        raise ValueError(f"Unknown target language: {target_lang}")

    model = normalized_model(model or load_nav_model())
    pages = discover_pages()
    label_items = flattened_model_labels(model["items"], source_lang, pages)
    prompt = {
        "task": "Translate website navigation labels only.",
        "source_language": language_name(source_lang),
        "target_language": language_name(target_lang),
        "rules": [
            "Return JSON only.",
            "Return exactly this schema: {\"translations\":{\"item-id\":\"translated label\"}}.",
            "Do not add, remove, reorder, rename, or restructure navigation items.",
            "Do not translate file paths, IDs, or page values.",
            "Translate labels naturally and concisely for website navigation.",
            "Preserve proper names and project names unless there is an established localized form.",
        ],
        "labels": label_items,
    }
    content = call_navigation_model(json.dumps(prompt, ensure_ascii=False), model_name or default_model())
    parsed = parse_json_response(content)
    translations = parsed.get("translations")
    if not isinstance(translations, dict):
        raise ValueError("LLM response must contain a translations object")

    applied: list[dict[str, str]] = []
    for item_id, label in translations.items():
        if not isinstance(label, str) or not label.strip():
            continue
        if set_model_label(model["items"], str(item_id), target_lang, label.strip()):
            applied.append({"id": str(item_id), "label": label.strip()})

    model["source"] = f"label translation {source_lang}->{target_lang} ({model_name or default_model()})"
    model = normalized_model(model)
    return {
        "model": model,
        "target_lang": target_lang,
        "target_language": language_name(target_lang),
        "translated_count": len(applied),
        "translations": applied,
        "raw": content,
        "preview": navigation_preview(model),
    }


def translate_all_nav_labels(
    model: dict[str, Any] | None = None,
    source_lang: str = DEFAULT_LANGUAGE,
    target_langs: list[str] | None = None,
    model_name: str | None = None,
) -> dict[str, Any]:
    languages = configured_languages()
    if source_lang not in languages:
        raise ValueError(f"Unknown source language: {source_lang}")

    targets = target_langs or [language for language in languages if language != source_lang]
    targets = [language for language in targets if language != source_lang]
    unknown = [language for language in targets if language not in languages]
    if unknown:
        raise ValueError(f"Unknown target languages: {', '.join(unknown)}")

    current_model = normalized_model(model or load_nav_model())
    results: list[dict[str, Any]] = []
    for target_lang in targets:
        result = translate_nav_labels(
            target_lang=target_lang,
            model=current_model,
            source_lang=source_lang,
            model_name=model_name,
        )
        current_model = result["model"]
        results.append(
            {
                "target_lang": target_lang,
                "target_language": result["target_language"],
                "translated_count": result["translated_count"],
                "translations": result["translations"],
                "raw": result["raw"],
            }
        )

    current_model["source"] = f"label translation from {source_lang} to {len(results)} languages ({model_name or default_model()})"
    current_model = normalized_model(current_model)
    return {
        "model": current_model,
        "source_lang": source_lang,
        "source_language": language_name(source_lang),
        "target_count": len(results),
        "results": results,
        "preview": navigation_preview(current_model),
    }


def call_navigation_model(prompt: str, model: str) -> str:
    load_local_env()
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY or OPENAI_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL") or os.getenv("OPENAI_BASE_URL") or DEFAULT_BASE_URL
    url = chat_completions_url(base_url)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an information architect for a multilingual Markdown knowledge commons. Return strict JSON only.",
            },
            {"role": "user", "content": prompt},
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
            "X-Title": "CircusWiki Navigation Console",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Navigation API request failed with HTTP {exc.code}: {details}") from exc
    return data["choices"][0]["message"]["content"]


def chat_completions_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/chat/completions"):
        return normalized
    return normalized + "/chat/completions"


def parse_json_response(content: str) -> dict[str, Any]:
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
        if text.startswith("json"):
            text = text[4:].strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("LLM response did not contain a JSON object")
    return json.loads(text[start : end + 1])
