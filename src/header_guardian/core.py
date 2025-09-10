from __future__ import annotations

from collections.abc import Iterator, Sequence
from pathlib import Path

DEFAULT_IGNORES: tuple[str, ...] = (
    ".git",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
)


def _iter_files(root: Path, exts: Sequence[str]) -> Iterator[Path]:
    exts_l = {e.lower() for e in exts}
    for path in root.rglob("*"):
        if any(part in DEFAULT_IGNORES for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in exts_l:
            yield path


def has_spdx_header(text: str) -> bool:
    head = "\n".join(text.splitlines()[:20]).lower()
    return "spdx-license-identifier:" in head


def _comment_prefix(ext: str) -> str:
    # Futuro: detectar por tipo de archivo; hoy, # para .py y default.
    return "# "


def insert_spdx_header(text: str, license_id: str, ext: str) -> str:
    if has_spdx_header(text):
        return text
    return f"{_comment_prefix(ext)}SPDX-License-Identifier: {license_id}\n" + text


# --- API compatible con tests antiguos ---
def has_header(path: Path) -> bool:
    txt = path.read_text(encoding="utf-8", errors="ignore")
    return has_spdx_header(txt)


def ensure_header(path: Path, license_id: str) -> bool:
    """Inserta header SPDX si falta. Devuelve True si modificó el archivo."""
    txt = path.read_text(encoding="utf-8", errors="ignore")
    if has_spdx_header(txt):
        return False
    new = insert_spdx_header(txt, license_id, path.suffix)
    path.write_text(new, encoding="utf-8")
    return True


# --- API por lotes para el CLI ---
def check_headers(root: Path, exts: Sequence[str], license_id: str) -> list[Path]:
    missing: list[Path] = []
    for fp in _iter_files(root, exts):
        if not has_header(fp):
            missing.append(fp)
    return missing


def fix_headers(root: Path, exts: Sequence[str], license_id: str) -> list[Path]:
    fixed: list[Path] = []
    for fp in _iter_files(root, exts):
        if ensure_header(fp, license_id):
            fixed.append(fp)
    return fixed
