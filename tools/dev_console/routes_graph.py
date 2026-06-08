from __future__ import annotations

from urllib.parse import parse_qs

from translation.original_graph import original_graph


def handle_get(handler, path: str, query_string: str) -> bool:
    if path == "/api/original-graph":
        try:
            query = parse_qs(query_string)
            exclude_sitemap = (query.get("exclude_sitemap", ["true"])[0] or "true").lower()
            return handler.send_json(original_graph(exclude_sitemap=exclude_sitemap != "false"))
        except Exception as exc:
            return handler.send_error_json(500, str(exc))
    return False


def handle_post(_handler, _path: str, _payload: dict[str, object]) -> bool:
    return False
