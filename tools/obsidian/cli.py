from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from typing import Any


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
