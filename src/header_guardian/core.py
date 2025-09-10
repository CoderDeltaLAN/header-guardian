from __future__ import annotations
from pathlib import Path
from typing import Iterable, Iterator, Sequence

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
    # Busca 'SPDX-License-Identifier:' en las primeras ~20 líneas
    head = "\n".join(text.splitlines()[:20]).lower()
    return "spdx-license-identifier:" in head

def insert_spdx_header(text: str, license_id: str, ext: str) -> str:
    comment_prefix = "# " if ext.lower() == ".py" else "# "
    header = f"{comment_prefix}SPDX-License-Identifier: {license_id}\n"
    # Evita duplicados
    if has_spdx_header(text):
        return text
    return header + text

def check_headers(root: Path, exts: Sequence[str], license_id: str) -> list[Path]:
    missing: list[Path] = []
    for fp in _iter_files(root, exts):
        txt = fp.read_text(encoding="utf-8", errors="ignore")
        if not has_spdx_header(txt):
            missing.append(fp)
    return missing

def fix_headers(root: Path, exts: Sequence[str], license_id: str) -> list[Path]:
    fixed: list[Path] = []
    for fp in _iter_files(root, exts):
        txt = fp.read_text(encoding="utf-8", errors="ignore")
        if not has_spdx_header(txt):
            new = insert_spdx_header(txt, license_id, fp.suffix)
            fp.write_text(new, encoding="utf-8")
            fixed.append(fp)
    return fixed
