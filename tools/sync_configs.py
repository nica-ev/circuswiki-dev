from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from core.languages import (
    DEFAULT_BASE_URL,
    native_language_name,
    normalize_base_path,
    normalize_base_url,
    site_subpath,
    site_url,
    validate_registry,
    zensical_configs,
    zensical_docs_dir,
    zensical_site_dir,
)

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SyncChange:
    path: str
    language: str
    field: str
    before: str
    after: str

    def as_dict(self) -> dict[str, str]:
        return {
            "path": self.path,
            "language": self.language,
            "field": self.field,
            "before": self.before,
            "after": self.after,
        }


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def alternate_block(base_path: str) -> str:
    lines = ["alternate = ["]
    for language in zensical_configs():
        lines.append(
            "  { name = "
            + toml_string(native_language_name(language))
            + ", link = "
            + toml_string(site_subpath(language, base_path))
            + ", lang = "
            + toml_string(language)
            + " },"
        )
    lines.append("]")
    return "\n".join(lines)


def replace_top_level_assignment(text: str, key: str, value: str) -> str:
    return re.sub(
        rf'(?m)^{re.escape(key)}\s*=\s*"[^"]*"',
        f"{key} = {toml_string(value)}",
        text,
        count=1,
    )


def replace_theme_language(text: str, value: str) -> str:
    pattern = re.compile(r'(?ms)(^\[project\.theme\]\s*.*?^language\s*=\s*)"[^"]*"')
    return pattern.sub(rf"\1{toml_string(value)}", text, count=1)


def replace_alternates(text: str, base_path: str) -> str:
    block = alternate_block(base_path)
    pattern = re.compile(r"(?ms)^alternate\s*=\s*\[.*?^\]")
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    marker = "[project.extra]\n"
    if marker in text:
        return text.replace(marker, marker + block + "\n", 1)
    return text.rstrip() + "\n\n[project.extra]\n" + block + "\n"


def sync_config_text(text: str, language: str, base_path: str, base_url: str) -> str:
    updated = replace_top_level_assignment(text, "site_url", site_url(language, base_url))
    updated = replace_top_level_assignment(updated, "docs_dir", zensical_docs_dir(language))
    updated = replace_top_level_assignment(updated, "site_dir", zensical_site_dir(language))
    updated = replace_theme_language(updated, language)
    updated = replace_alternates(updated, base_path)
    return updated


def describe_changes(path: Path, language: str, before: str, after: str) -> list[SyncChange]:
    changes: list[SyncChange] = []
    for field, pattern in {
        "site_url": r'(?m)^site_url\s*=\s*"([^"]*)"',
        "docs_dir": r'(?m)^docs_dir\s*=\s*"([^"]*)"',
        "site_dir": r'(?m)^site_dir\s*=\s*"([^"]*)"',
        "theme.language": r'(?ms)^\[project\.theme\]\s*.*?^language\s*=\s*"([^"]*)"',
    }.items():
        before_value = match_value(pattern, before)
        after_value = match_value(pattern, after)
        if before_value != after_value:
            changes.append(SyncChange(rel(path), language, field, before_value, after_value))

    if match_value(r"(?ms)^alternate\s*=\s*(\[.*?^\])", before) != match_value(
        r"(?ms)^alternate\s*=\s*(\[.*?^\])",
        after,
    ):
        changes.append(SyncChange(rel(path), language, "alternate", "changed", "synced"))
    return changes


def match_value(pattern: str, text: str) -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def sync_configs(write: bool = False, base_path: str | None = None, base_url: str | None = None) -> dict[str, object]:
    normalized_base_path = normalize_base_path(base_path)
    normalized_base_url = normalize_base_url(base_url)
    changes: list[SyncChange] = []
    changed_files: list[str] = []

    for language, path in zensical_configs().items():
        before = path.read_text(encoding="utf-8")
        after = sync_config_text(before, language, normalized_base_path, normalized_base_url)
        file_changes = describe_changes(path, language, before, after)
        if file_changes:
            changes.extend(file_changes)
            changed_files.append(rel(path))
            if write:
                path.write_text(after, encoding="utf-8", newline="\n")

    validation = validate_registry() if write else None
    return {
        "write": write,
        "base_path": normalized_base_path,
        "base_url": normalized_base_url,
        "changed_count": len(changes),
        "changed_files": changed_files,
        "changes": [change.as_dict() for change in changes],
        "validation": validation,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronize Zensical configs from tools/config/languages.json.")
    parser.add_argument("--write", action="store_true", help="Write changes. Default is dry-run only.")
    parser.add_argument("--base-path", default=os.getenv("CIRCUSWIKI_SITE_BASE_PATH"))
    parser.add_argument("--base-url", default=os.getenv("CIRCUSWIKI_SITE_URL") or DEFAULT_BASE_URL)
    args = parser.parse_args()

    result = sync_configs(write=args.write, base_path=args.base_path, base_url=args.base_url)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    validation = result.get("validation")
    if isinstance(validation, dict) and not validation.get("ok"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
