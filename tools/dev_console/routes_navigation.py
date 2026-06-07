from __future__ import annotations

from navigation.workflow import (
    apply_nav_model,
    model_from_current_nav,
    nav_scan,
    navigation_preview,
    save_nav_model,
    translate_all_nav_labels,
    translate_nav_labels,
)


def handle_get(handler, path: str, _query_string: str) -> bool:
    if path == "/api/navigation/scan":
        try:
            return handler.send_json(nav_scan())
        except Exception as exc:
            return handler.send_error_json(500, str(exc))
    return False


def handle_post(handler, path: str, payload: dict[str, object]) -> bool:
    if path == "/api/navigation/init":
        try:
            language = str(payload.get("language") or "")
            if not language:
                return handler.send_error_json(400, "Missing language")
            model = save_nav_model(model_from_current_nav(language))
            return handler.send_json({"model": model, "preview": navigation_preview(model)})
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    if path == "/api/navigation/preview":
        model = payload.get("model")
        if not isinstance(model, dict):
            return handler.send_error_json(400, "Missing model object")
        try:
            return handler.send_json(navigation_preview(model))
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    if path == "/api/navigation/apply":
        model = payload.get("model")
        if not isinstance(model, dict):
            return handler.send_error_json(400, "Missing model object")
        try:
            return handler.send_json(apply_nav_model(model, save_model=True))
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    if path == "/api/navigation/translate-labels":
        model = payload.get("model")
        if not isinstance(model, dict):
            return handler.send_error_json(400, "Missing model object")
        try:
            target_lang = str(payload.get("target_lang") or "")
            source_lang = str(payload.get("source_lang") or "")
            if not source_lang:
                return handler.send_error_json(400, "Missing source_lang")
            if not target_lang:
                return handler.send_error_json(400, "Missing target_lang")
            llm_model = payload.get("llm_model") or None
            result = translate_nav_labels(
                target_lang=target_lang,
                model=model,
                source_lang=source_lang,
                model_name=str(llm_model) if llm_model else None,
            )
            return handler.send_json(result)
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    if path == "/api/navigation/translate-all-labels":
        model = payload.get("model")
        if not isinstance(model, dict):
            return handler.send_error_json(400, "Missing model object")
        try:
            source_lang = str(payload.get("source_lang") or "")
            if not source_lang:
                return handler.send_error_json(400, "Missing source_lang")
            llm_model = payload.get("llm_model") or None
            result = translate_all_nav_labels(
                model=model,
                source_lang=source_lang,
                model_name=str(llm_model) if llm_model else None,
            )
            return handler.send_json(result)
        except Exception as exc:
            return handler.send_error_json(500, str(exc))

    return False
