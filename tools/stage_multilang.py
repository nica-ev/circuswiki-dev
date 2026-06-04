from __future__ import annotations

import re
import shutil
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BUILD = ROOT / ".build"
SITE_ASSETS = ROOT / "site-assets"
LANGUAGES = ("de", "en")


IMAGE_LINK_RE = re.compile(
    r"(?P<prefix>(?:\(|\[|=|:\s*|src=[\"']|href=[\"']))"
    r"(?P<path>(?:(?:\.\./)+)?img/)"
)


def copy_language(language: str) -> Path:
    source = DOCS / language
    target = BUILD / language

    if not source.exists():
        raise FileNotFoundError(f"Missing language source directory: {source}")

    shutil.copytree(source, target)

    shared_img = DOCS / "img"
    if shared_img.exists():
        shutil.copytree(shared_img, target / "img")

    if SITE_ASSETS.exists():
        for item in SITE_ASSETS.iterdir():
            destination = target / item.name
            if item.is_dir():
                shutil.copytree(item, destination)
            else:
                shutil.copy2(item, destination)

    return target


def normalize_image_links(language_root: Path) -> None:
    for markdown_file in language_root.rglob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        replacement_path = os.path.relpath(
            language_root / "img", markdown_file.parent
        ).replace("\\", "/").rstrip("/") + "/"

        def replace(match: re.Match[str]) -> str:
            return f"{match.group('prefix')}{replacement_path}"

        updated = IMAGE_LINK_RE.sub(replace, text)
        if updated != text:
            markdown_file.write_text(updated, encoding="utf-8", newline="")


def main() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)

    for language in LANGUAGES:
        language_root = copy_language(language)
        normalize_image_links(language_root)


if __name__ == "__main__":
    main()
