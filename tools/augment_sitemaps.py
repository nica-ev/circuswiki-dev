from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
LANGUAGES = ("de", "en", "pl", "hu", "it", "nl", "el", "es", "uk")
DEFAULT_LANGUAGE = "de"
DEFAULT_BASE_URL = "https://nica-ev.github.io/circuswiki/"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def normalize_base_url(value: str) -> str:
    value = value.strip() or DEFAULT_BASE_URL
    if not value.endswith("/"):
        value += "/"
    return value


def language_base_url(base_url: str, language: str) -> str:
    if language == DEFAULT_LANGUAGE:
        return base_url
    return f"{base_url}{language}/"


def site_root(language: str) -> Path:
    if language == DEFAULT_LANGUAGE:
        return SITE
    return SITE / language


def page_paths(site_root: Path, language: str) -> list[str]:
    paths: list[str] = []
    for index in site_root.rglob("index.html"):
        parts = index.relative_to(site_root).parts
        if any(part.startswith(".") for part in parts):
            continue
        relative = index.parent.relative_to(site_root)
        if not relative.parts:
            paths.append("")
        elif relative.parts[0] not in {"assets", "javascripts", *LANGUAGES}:
            paths.append(relative.as_posix() + "/")
    return sorted(set(paths))


def page_url(base_url: str, relative_path: str) -> str:
    return base_url + quote(relative_path, safe="/")


def write_sitemap(language: str, site_root: Path, base_url: str) -> None:
    if not site_root.exists():
        return

    urlset = ElementTree.Element("urlset", xmlns=SITEMAP_NS)
    for relative_path in page_paths(site_root, language):
        url = ElementTree.SubElement(urlset, "url")
        loc = ElementTree.SubElement(url, "loc")
        loc.text = page_url(language_base_url(base_url, language), relative_path)

    tree = ElementTree.ElementTree(urlset)
    ElementTree.indent(tree, space="  ")
    tree.write(site_root / "sitemap.xml", encoding="utf-8", xml_declaration=True)


def main() -> None:
    base_url = normalize_base_url(os.getenv("CIRCUSWIKI_SITE_URL", DEFAULT_BASE_URL))
    for language in LANGUAGES:
        write_sitemap(language, site_root(language), base_url)


if __name__ == "__main__":
    main()
