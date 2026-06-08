from __future__ import annotations

from translation.cleanup import (
    delete_all_deletable_orphan_translations,
    delete_orphan_translations,
    scan_orphan_translations,
)


def handle_get(handler, path: str, _query_string: str) -> bool:
    if path == "/api/cleanup/orphans":
        try:
            return handler.send_json(scan_orphan_translations())
        except Exception as exc:
            return handler.send_error_json(500, str(exc))
    return False


def handle_post(handler, path: str, payload: dict[str, object]) -> bool:
    if path == "/api/cleanup/delete-orphans":
        try:
            paths = payload.get("paths")
            if not isinstance(paths, list):
                return handler.send_error_json(400, "Missing paths list")
            return handler.send_json(delete_orphan_translations([str(path) for path in paths]))
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    if path == "/api/cleanup/delete-all-orphans":
        try:
            return handler.send_json(delete_all_deletable_orphan_translations())
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    return False
