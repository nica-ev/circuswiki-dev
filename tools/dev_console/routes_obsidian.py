from __future__ import annotations

from obsidian.cli import open_path, status


def handle_get(handler, path: str, _query_string: str) -> bool:
    if path == "/api/obsidian/status":
        return handler.send_json(status())
    return False


def handle_post(handler, path: str, payload: dict[str, object]) -> bool:
    if path == "/api/obsidian/open":
        try:
            item_path = str(payload.get("path") or "")
            newtab = bool(payload.get("newtab"))
            return handler.send_json(open_path(item_path, newtab=newtab))
        except Exception as exc:
            return handler.send_error_json(400, str(exc))
    return False
