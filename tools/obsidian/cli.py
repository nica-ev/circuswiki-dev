from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class CommandResult:
    ok: bool
    command: list[str]
    stdout: str
    stderr: str
    error: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "command": self.command,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "error": self.error,
        }


def obsidian_executable() -> str | None:
    return shutil.which("obsidian")


def status() -> dict[str, Any]:
    executable = obsidian_executable()
    command = [executable or "obsidian"]
    return {
        "ok": True,
        "available": executable is not None,
        "command": command,
        "stdout": executable or "",
        "stderr": "",
        "error": "" if executable else "Obsidian CLI executable was not found on PATH.",
    }


def run_obsidian(args: list[str], timeout_seconds: int = 10) -> CommandResult:
    executable = obsidian_executable()
    command = [executable or "obsidian", *args]
    if not executable:
        return CommandResult(
            ok=False,
            command=command,
            stdout="",
            stderr="",
            error="Obsidian CLI executable was not found on PATH.",
        )

    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            text=True,
            timeout=timeout_seconds,
        )
    except Exception as exc:
        return CommandResult(
            ok=False,
            command=command,
            stdout="",
            stderr="",
            error=str(exc),
        )

    return CommandResult(
        ok=completed.returncode == 0,
        command=command,
        stdout=completed.stdout,
        stderr=completed.stderr,
        error="" if completed.returncode == 0 else f"Command exited with {completed.returncode}.",
    )


def open_path(path: str, newtab: bool = False) -> dict[str, Any]:
    target = normalize_vault_path(path)
    args = ["open", f"path={target}"]
    if newtab:
        args.append("newtab")
    result = run_obsidian(args)
    payload = result.as_dict()
    payload["path"] = target
    return payload


def normalize_vault_path(path: str) -> str:
    if not path.strip():
        raise ValueError("Missing path")

    raw = Path(path)
    target = raw.resolve() if raw.is_absolute() else (ROOT / raw).resolve()
    try:
        relative = target.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError("Path is outside the vault root") from exc
    if not target.is_file():
        raise ValueError("Path does not exist")
    return relative.as_posix()
