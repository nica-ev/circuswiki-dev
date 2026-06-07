from __future__ import annotations

from obsidian.cli import status


def handle_get(handler, path: str, _query_string: str) -> bool:
    if path == "/api/obsidian/status":
        return handler.send_json(status())
    return False


def handle_post(_handler, _path: str, _payload: dict[str, object]) -> bool:
    return False
