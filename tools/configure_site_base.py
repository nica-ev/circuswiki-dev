from __future__ import annotations

import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIGS = {
    "de": ROOT / "zensical.toml",
    "en": ROOT / "zensical.en.toml",
    "pl": ROOT / "zensical.pl.toml",
    "hu": ROOT / "zensical.hu.toml",
    "it": ROOT / "zensical.it.toml",
    "nl": ROOT / "zensical.nl.toml",
    "el": ROOT / "zensical.el.toml",
    "es": ROOT / "zensical.es.toml",
    "uk": ROOT / "zensical.uk.toml",
}
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
    if language == "de":
        return base_path
    return f"{base_path}{language}/"


def language_url(base_url: str, language: str) -> str:
    if language == "de":
        return base_url
    return f"{base_url}{language}/"


def replace_project_site_url(text: str, site_url: str) -> str:
    return re.sub(
        r'(?m)^site_url\s*=\s*"[^"]*"',
        f'site_url = "{site_url}"',
        text,
        count=1,
    )


def replace_alternate_link(text: str, language: str, link: str) -> str:
    pattern = re.compile(
        r'(\{\s*name\s*=\s*"[^"]+"\s*,\s*link\s*=\s*")[^"]*("\s*,\s*lang\s*=\s*"'
        + re.escape(language)
        + r'"\s*\})'
    )
    return pattern.sub(rf"\1{link}\2", text, count=1)


def configure_file(path: Path, language: str, base_path: str, base_url: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_project_site_url(text, language_url(base_url, language))

    for alternate_language in CONFIGS:
        text = replace_alternate_link(
            text,
            alternate_language,
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
