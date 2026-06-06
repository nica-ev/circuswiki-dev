from __future__ import annotations

import re
from collections.abc import Iterable


SCALAR_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?P<value>.*)$")


def read_scalar(frontmatter: str, key: str) -> str | None:
    for line in frontmatter.splitlines():
        match = SCALAR_RE.match(line)
        if match and match.group("key") == key:
            return match.group("value").strip().strip('"')
    return None


def set_scalar(frontmatter: str, key: str, value: str) -> str:
    lines = frontmatter.splitlines()
    replacement = f"{key}: {format_scalar(value)}"

    for index, line in enumerate(lines):
        match = SCALAR_RE.match(line)
        if match and match.group("key") == key:
            lines[index] = replacement
            return "\n".join(lines) + "\n"

    if lines and lines[-1].strip():
        lines.append(replacement)
    else:
        lines[-1:] = [replacement]
    return "\n".join(lines) + "\n"


def ensure_scalars(frontmatter: str, values: dict[str, str]) -> str:
    updated = frontmatter
    for key, value in values.items():
        updated = set_scalar(updated, key, value)
    return updated


def missing_scalars(frontmatter: str, keys: Iterable[str]) -> list[str]:
    return [key for key in keys if read_scalar(frontmatter, key) in (None, "")]


def format_scalar(value: str) -> str:
    if value == "":
        return ""
    if any(char in value for char in ['"', "\n"]):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if value.lower() in {"true", "false", "null", "none"}:
        return f'"{value}"'
    if value.startswith((" ", "-", "@", "#")) or value.endswith(" "):
        return f'"{value}"'
    return value
