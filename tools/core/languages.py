"""Shared language and site registry helpers for CircusWiki tooling."""
from __future__ import annotations

import json
import os
import sys
import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
REGISTRY_PATH = ROOT / "tools" / "config" / "languages.json"
DEFAULT_BASE_PATH = "/circuswiki/"
DEFAULT_BASE_URL = "https://nica-ev.github.io/circuswiki/"


@lru_cache(maxsize=1)
def registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8-sig"))


def language_entries() -> list[dict[str, Any]]:
    return list(registry().get("languages", []))


def language_codes() -> tuple[str, ...]:
    return tuple(str(item["code"]) for item in language_entries())


def language_codes_re() -> str:
    return "|".join(language_codes())


def default_language() -> str:
    return str(registry().get("default_language") or "de")


def common_fallback_language() -> str:
    return str(registry().get("common_fallback_language") or "en")


def language_entry(code: str) -> dict[str, Any] | None:
    return next((item for item in language_entries() if item.get("code") == code), None)


def language_name(code: str) -> str:
    entry = language_entry(code)
    return str(entry.get("name") if entry else code)


def native_language_name(code: str) -> str:
    entry = language_entry(code)
    return str(entry.get("nativeName") if entry else language_name(code))


def zensical_config_path(code: str) -> Path:
    entry = language_entry(code)
    if not entry:
        raise KeyError(f"Unknown language: {code}")
    return ROOT / str(entry["zensical"])


def zensical_configs() -> dict[str, Path]:
    return {code: zensical_config_path(code) for code in language_codes()}


def docs_path(code: str) -> Path:
    return DOCS / code


def site_subpath(code: str, base_path: str) -> str:
    if code == default_language():
        return base_path
    return f"{base_path}{code}/"


def site_url(code: str, base_url: str) -> str:
    if code == default_language():
        return base_url
    return f"{base_url}{code}/"


def normalize_base_path(value: str | None = None) -> str:
    base_path = (value or os.getenv("CIRCUSWIKI_SITE_BASE_PATH") or DEFAULT_BASE_PATH).strip()
    if not base_path.startswith("/"):
        base_path = "/" + base_path
    if not base_path.endswith("/"):
        base_path += "/"
    return base_path


def normalize_base_url(value: str | None = None) -> str:
    base_url = (value or os.getenv("CIRCUSWIKI_SITE_URL") or DEFAULT_BASE_URL).strip()
    if not base_url.endswith("/"):
        base_url += "/"
    return base_url


def zensical_docs_dir(code: str) -> str:
    return f".build/{code}"


def zensical_site_dir(code: str) -> str:
    if code == default_language():
        return "site"
    return f"site/{code}"


def configured_language_codes(require_docs: bool = False, require_config: bool = False) -> list[str]:
    codes = list(language_codes())
    if require_docs:
        codes = [code for code in codes if docs_path(code).exists()]
    if require_config:
        codes = [code for code in codes if zensical_config_path(code).exists()]
    return codes


def extra_docs_language_codes() -> list[str]:
    known = set(language_codes())
    if not DOCS.exists():
        return []
    return sorted(
        path.name
        for path in DOCS.iterdir()
        if path.is_dir() and path.name != "img" and path.name not in known
    )


def validate_registry() -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in language_entries():
        code = str(entry.get("code") or "")
        if not code:
            issues.append({"language": "", "issue": "missing_code"})
            continue
        if code in seen:
            issues.append({"language": code, "issue": "duplicate_code"})
        seen.add(code)
        for key in ("name", "nativeName", "zensical"):
            if not entry.get(key):
                issues.append({"language": code, "issue": f"missing_{key}"})
        if not docs_path(code).exists():
            issues.append({"language": code, "issue": "missing_docs_dir"})
        if not zensical_config_path(code).exists():
            issues.append({"language": code, "issue": "missing_zensical_config"})
    for code in extra_docs_language_codes():
        issues.append({"language": code, "issue": "docs_dir_not_in_registry"})
    issues.extend(validate_zensical_configs())
    return {"ok": not issues, "languages": list(language_codes()), "issues": issues}


def validate_zensical_configs(
    base_path: str | None = None,
    base_url: str | None = None,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    expected_codes = list(language_codes())
    expected_links = {
        code: site_subpath(code, normalize_base_path(base_path)) for code in expected_codes
    }
    expected_names = {code: native_language_name(code) for code in expected_codes}
    expected_base_url = normalize_base_url(base_url)

    for config_language, config_path in zensical_configs().items():
        if not config_path.exists():
            continue
        try:
            data = tomllib.loads(config_path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            issues.append(
                {
                    "language": config_language,
                    "config": rel(config_path),
                    "issue": "invalid_toml",
                    "detail": str(exc),
                }
            )
            continue

        project = data.get("project", {})
        expected_site_url = site_url(config_language, expected_base_url)
        if str(project.get("site_url") or "") != expected_site_url:
            issues.append(
                {
                    "language": config_language,
                    "config": rel(config_path),
                    "issue": "site_url_mismatch",
                    "expected": expected_site_url,
                    "actual": str(project.get("site_url") or ""),
                }
            )

        expected_docs_dir = zensical_docs_dir(config_language)
        if str(project.get("docs_dir") or "") != expected_docs_dir:
            issues.append(
                {
                    "language": config_language,
                    "config": rel(config_path),
                    "issue": "docs_dir_mismatch",
                    "expected": expected_docs_dir,
                    "actual": str(project.get("docs_dir") or ""),
                }
            )

        expected_site_dir = zensical_site_dir(config_language)
        if str(project.get("site_dir") or "") != expected_site_dir:
            issues.append(
                {
                    "language": config_language,
                    "config": rel(config_path),
                    "issue": "site_dir_mismatch",
                    "expected": expected_site_dir,
                    "actual": str(project.get("site_dir") or ""),
                }
            )

        theme_language = str(project.get("theme", {}).get("language") or "")
        if theme_language != config_language:
            issues.append(
                {
                    "language": config_language,
                    "config": rel(config_path),
                    "issue": "theme_language_mismatch",
                    "expected": config_language,
                    "actual": theme_language,
                }
            )

        alternates = project.get("extra", {}).get("alternate") or []
        by_language = {
            str(item.get("lang")): item
            for item in alternates
            if isinstance(item, dict) and item.get("lang")
        }

        for code in expected_codes:
            alternate = by_language.get(code)
            if not alternate:
                issues.append(
                    {
                        "language": config_language,
                        "config": rel(config_path),
                        "alternate": code,
                        "issue": "missing_alternate",
                    }
                )
                continue
            actual_name = str(alternate.get("name") or "")
            actual_link = str(alternate.get("link") or "")
            if actual_name != expected_names[code]:
                issues.append(
                    {
                        "language": config_language,
                        "config": rel(config_path),
                        "alternate": code,
                        "issue": "alternate_name_mismatch",
                        "expected": expected_names[code],
                        "actual": actual_name,
                    }
                )
            if actual_link != expected_links[code]:
                issues.append(
                    {
                        "language": config_language,
                        "config": rel(config_path),
                        "alternate": code,
                        "issue": "alternate_link_mismatch",
                        "expected": expected_links[code],
                        "actual": actual_link,
                    }
                )

        extra = sorted(set(by_language) - set(expected_codes))
        for code in extra:
            issues.append(
                {
                    "language": config_language,
                    "config": rel(config_path),
                    "alternate": code,
                    "issue": "alternate_not_in_registry",
                }
            )

    return issues


def validate_zensical_alternates(base_path: str | None = None) -> list[dict[str, str]]:
    return [
        issue
        for issue in validate_zensical_configs(base_path=base_path)
        if issue["issue"].startswith("alternate_") or issue["issue"] == "missing_alternate"
    ]


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def main() -> None:
    result = validate_registry()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
