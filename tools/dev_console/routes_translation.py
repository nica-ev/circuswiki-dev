from __future__ import annotations

from urllib.parse import parse_qs

from core.languages import common_fallback_language, default_language, language_entries
from translation.workflow import (
    batch_translation_plan,
    default_model,
    default_prompt,
    default_prompt_template,
    health_summary,
    inspect_page,
    list_sources,
    repair_vault_metadata,
    translate_batch_item,
    translate_page,
    vault_health_matrix,
)


def query_value(query: dict[str, list[str]], key: str, default: str = "") -> str:
    return query.get(key, [default])[0] or default


def required_query_value(handler, query: dict[str, list[str]], key: str) -> str | None:
    value = query_value(query, key)
    if not value:
        handler.send_error_json(400, f"Missing {key}")
        return None
    return value


def required_payload_value(handler, payload: dict[str, object], key: str) -> str | None:
    value = str(payload.get(key) or "")
    if not value:
        handler.send_error_json(400, f"Missing {key}")
        return None
    return value


def handle_get(handler, path: str, query_string: str) -> bool:
    query = parse_qs(query_string)

    if path == "/api/config":
        source_lang = default_language()
        target_lang = common_fallback_language()
        return handler.send_json(
            {
                "default_model": default_model(),
                "default_source_lang": source_lang,
                "default_target_lang": target_lang,
                "languages": language_entries(),
                "default_prompt": default_prompt_template(),
                "default_rendered_prompt": default_prompt(source_lang, target_lang),
            }
        )

    if path == "/api/pages":
        source_lang = required_query_value(handler, query, "source_lang")
        if not source_lang:
            return True
        return handler.send_json({"pages": list_sources(source_lang)})

    if path == "/api/health":
        source_lang = required_query_value(handler, query, "source_lang")
        target_lang = required_query_value(handler, query, "target_lang")
        if not source_lang or not target_lang:
            return True
        return handler.send_json(health_summary(source_lang, target_lang))

    if path == "/api/vault-health":
        return handler.send_json(vault_health_matrix())

    if path == "/api/page":
        source_path = query_value(query, "path")
        if not source_path:
            return handler.send_error_json(400, "Missing path")
        source_lang = required_query_value(handler, query, "source_lang")
        target_lang = required_query_value(handler, query, "target_lang")
        if not source_lang or not target_lang:
            return True
        try:
            return handler.send_json(inspect_page(source_path, source_lang, target_lang).__dict__)
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    return False


def handle_post(handler, path: str, payload: dict[str, object]) -> bool:
    if path == "/api/translate":
        source_path = payload.get("path")
        if not source_path:
            return handler.send_error_json(400, "Missing path")
        source_lang = required_payload_value(handler, payload, "source_lang")
        target_lang = required_payload_value(handler, payload, "target_lang")
        if not source_lang or not target_lang:
            return True
        try:
            result = translate_page(
                source_path=str(source_path),
                source_lang=source_lang,
                target_lang=target_lang,
                model=payload.get("model") or None,
                prompt=payload.get("prompt") or None,
                dry_run=bool(payload.get("dry_run")),
            )
            return handler.send_json(result)
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    if path == "/api/repair-metadata":
        source_path = payload.get("path")
        if not source_path:
            return handler.send_error_json(400, "Missing path")
        try:
            return handler.send_json(repair_vault_metadata(str(source_path)))
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    if path == "/api/batch-plan":
        try:
            target_lang = str(payload.get("target_lang") or "")
            max_files = int(payload.get("max_files") or 0)
            raw_max_source_chars = payload.get("max_source_chars")
            max_source_chars = (
                int(raw_max_source_chars)
                if raw_max_source_chars not in (None, "", 0, "0")
                else None
            )
            return handler.send_json(
                batch_translation_plan(
                    target_lang=target_lang,
                    max_files=max_files,
                    source_lang=str(payload.get("source_lang") or "all"),
                    reason=str(payload.get("reason") or "all"),
                    max_source_chars=max_source_chars,
                    path_filter=str(payload.get("path_filter") or ""),
                )
            )
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    if path == "/api/batch-translate-file":
        try:
            result = translate_batch_item(
                source_path=str(payload.get("source_path") or ""),
                source_lang=str(payload.get("source_lang") or ""),
                target_lang=str(payload.get("target_lang") or ""),
                model=payload.get("model") or None,
                prompt=payload.get("prompt") or None,
            )
            return handler.send_json(result)
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    return False
