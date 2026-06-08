from __future__ import annotations

import json
from typing import Any

from obsidian.cli import CommandResult, run_obsidian, status as obsidian_status


def status() -> dict[str, Any]:
    return obsidian_status()


def query_base(base_path: str, view: str, timeout_seconds: int = 60) -> dict[str, Any]:
    result = run_obsidian(
        [
            "base:query",
            f"path={base_path}",
            f"view={view}",
            "format=json",
        ],
        timeout_seconds=timeout_seconds,
    )
    parsed = parse_json_output(result)
    return {
        "ok": result.ok and parsed["ok"],
        "command": result.command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "error": result.error or parsed["error"],
        "data": parsed["data"],
    }


def parse_json_output(result: CommandResult) -> dict[str, Any]:
    if not result.ok:
        return {"ok": False, "data": None, "error": result.error or result.stderr}

    text = result.stdout.strip()
    if not text:
        return {"ok": False, "data": None, "error": "Obsidian returned empty output."}

    for start_char in ("[", "{"):
        start = text.find(start_char)
        if start == -1:
            continue
        candidate = text[start:]
        try:
            return {"ok": True, "data": json.loads(candidate), "error": ""}
        except json.JSONDecodeError:
            continue

    return {"ok": False, "data": None, "error": "Obsidian output was not valid JSON."}
