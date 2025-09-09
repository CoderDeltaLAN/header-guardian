# Copyright 2025 CoderDeltaLAN
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path


def ping() -> str:
    return "pong"


def _normalize(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def has_header(path: Path, header_text: str) -> bool:
    data = path.read_text(encoding="utf-8", errors="strict")
    return _normalize(data).startswith(_normalize(header_text))


def ensure_header(path: Path, header_text: str, autofix: bool = False) -> bool:
    if has_header(path, header_text):
        return True
    if not autofix:
        return False
    original = path.read_text(encoding="utf-8", errors="strict")
    path.write_text(_normalize(header_text) + original, encoding="utf-8")
    return True
