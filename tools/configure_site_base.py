from __future__ import annotations

import json
import os
import re
from pathlib import Path

from core.languages import (
    default_language,
    native_language_name,
    site_subpath,
    site_url,
    zensical_configs,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIGS = zensical_configs()
DEFAULT_LANGUAGE = default_language()
DEFAULT_BASE_URL = "https://nica-ev.github.io/circuswiki/"


def normalize_base_path(value: str) -> str:
    value = value.strip() or "/circuswiki/"
    if not value.startswith("/"):
        value = "/" + value
    if not value.endswith("/"):
        value += "/"
    return value


def normalize_base_url(value: str) -> str:
    value = value.strip() or DEFAULT_BASE_URL
    if not value.endswith("/"):
        value += "/"
    return value


def language_path(base_path: str, language: str) -> str:
    return site_subpath(language, base_path)


def language_url(base_url: str, language: str) -> str:
    return site_url(language, base_url)


def replace_project_site_url(text: str, site_url: str) -> str:
    return re.sub(
        r'(?m)^site_url\s*=\s*"[^"]*"',
        f'site_url = "{site_url}"',
        text,
        count=1,
    )


def replace_alternate(text: str, language: str, name: str, link: str) -> str:
    pattern = re.compile(
        r'(\{\s*name\s*=\s*)"[^"]+"(\s*,\s*link\s*=\s*)"[^"]+"(\s*,\s*lang\s*=\s*"'
        + re.escape(language)
        + r'"\s*\})'
    )
    name_value = json.dumps(name, ensure_ascii=False)
    link_value = json.dumps(link, ensure_ascii=False)
    return pattern.sub(rf"\1{name_value}\2{link_value}\3", text, count=1)


def configure_file(path: Path, language: str, base_path: str, base_url: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_project_site_url(text, language_url(base_url, language))

    for alternate_language in CONFIGS:
        text = replace_alternate(
            text,
            alternate_language,
            native_language_name(alternate_language),
            language_path(base_path, alternate_language),
        )

    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    base_path = normalize_base_path(os.getenv("CIRCUSWIKI_SITE_BASE_PATH", "/circuswiki/"))
    base_url = normalize_base_url(os.getenv("CIRCUSWIKI_SITE_URL", DEFAULT_BASE_URL))

    for language, path in CONFIGS.items():
        configure_file(path, language, base_path, base_url)

    print(f"Configured site base path: {base_path}")
    print(f"Configured site URL: {base_url}")


if __name__ == "__main__":
    main()
