from __future__ import annotations

import argparse
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[2]
STATIC = Path(__file__).resolve().parent / "static"
sys.path.insert(0, str(ROOT / "tools"))

from translation.workflow import (  # noqa: E402
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


class DevConsoleHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/api/config":
            return self.send_json(
                {
                    "default_model": default_model(),
                    "default_source_lang": "de",
                    "default_target_lang": "en",
                    "default_prompt": default_prompt_template(),
                    "default_rendered_prompt": default_prompt("de", "en"),
                }
            )

        if parsed.path == "/api/pages":
            return self.send_json({"pages": list_sources()})

        if parsed.path == "/api/health":
            return self.send_json(health_summary())

        if parsed.path == "/api/vault-health":
            return self.send_json(vault_health_matrix())

        if parsed.path == "/api/page":
            query = parse_qs(parsed.query)
            path = query.get("path", [""])[0]
            if not path:
                return self.send_error_json(400, "Missing path")
            try:
                return self.send_json(inspect_page(path).__dict__)
            except Exception as exc:
                return self.send_error_json(500, str(exc))

        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/api/translate":
            payload = self.read_json()
            if payload is None:
                return self.send_error_json(400, "Invalid JSON")

            path = payload.get("path")
            if not path:
                return self.send_error_json(400, "Missing path")

            try:
                result = translate_page(
                    source_path=path,
                    model=payload.get("model") or None,
                    prompt=payload.get("prompt") or None,
                    dry_run=bool(payload.get("dry_run")),
                )
                return self.send_json(result)
            except Exception as exc:
                return self.send_error_json(500, str(exc))

        if parsed.path == "/api/repair-metadata":
            payload = self.read_json()
            if payload is None:
                return self.send_error_json(400, "Invalid JSON")

            path = payload.get("path")
            if not path:
                return self.send_error_json(400, "Missing path")

            try:
                return self.send_json(repair_vault_metadata(str(path)))
            except Exception as exc:
                return self.send_error_json(500, str(exc))

        if parsed.path == "/api/batch-plan":
            payload = self.read_json()
            if payload is None:
                return self.send_error_json(400, "Invalid JSON")

            try:
                target_lang = str(payload.get("target_lang") or "")
                max_files = int(payload.get("max_files") or 0)
                return self.send_json(batch_translation_plan(target_lang, max_files))
            except Exception as exc:
                return self.send_error_json(500, str(exc))

        if parsed.path == "/api/batch-translate-file":
            payload = self.read_json()
            if payload is None:
                return self.send_error_json(400, "Invalid JSON")

            try:
                result = translate_batch_item(
                    source_path=str(payload.get("source_path") or ""),
                    source_lang=str(payload.get("source_lang") or ""),
                    target_lang=str(payload.get("target_lang") or ""),
                    model=payload.get("model") or None,
                    prompt=payload.get("prompt") or None,
                )
                return self.send_json(result)
            except Exception as exc:
                return self.send_error_json(500, str(exc))

        return self.send_error_json(404, "Unknown endpoint")

    def read_json(self) -> dict[str, object] | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw)
        except Exception:
            return None

    def send_json(self, payload: object, status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_error_json(self, status: int, message: str) -> None:
        self.send_json({"error": message}, status=status)


def main() -> None:
    parser = argparse.ArgumentParser(description="CircusWiki local dev console")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), DevConsoleHandler)
    print(f"Dev console: http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
