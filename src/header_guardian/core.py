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


_COMMENT_MAP: dict[str, str] = {
    ".py": "# ",
    ".sh": "# ",
    ".ts": "// ",
    ".js": "// ",
    ".c": "// ",
    ".h": "// ",
    ".cpp": "// ",
    ".hpp": "// ",
    ".java": "// ",
    ".go": "// ",
    ".rs": "// ",
}


def _comment_prefix(ext: str) -> str:
    return _COMMENT_MAP.get(ext.lower(), "# ")


def _normalize(s: str) -> str:
    return "\n".join(line.strip() for line in s.strip().splitlines())


def default_header_text(license_id: str = "MIT", ext: str = ".py") -> str:
    # Cabecera mínima (puede expandirse con Copyright si se desea)
    return f"{_comment_prefix(ext)}SPDX-License-Identifier: {license_id}\n"


def header_for_path(path: Path, license_id: str = "MIT") -> str:
    return default_header_text(license_id=license_id, ext=path.suffix)


def has_header(path: Path, header: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    head = "\n".join(text.splitlines()[:50])
    return _normalize(header) in _normalize(head)


# Compat: acepta Path o str (contenido). Si str y header no dado, busca cadena SPDX.
def has_spdx_header(obj: Path | str, header: str | None = None, *, license_id: str = "MIT") -> bool:
    if isinstance(obj, Path):
        h = header or header_for_path(obj, license_id=license_id)
        return has_header(obj, h)
    text = obj
    if header is not None:
        return _normalize(header) in _normalize("\n".join(text.splitlines()[:50]))
    return "SPDX-License-Identifier:" in text.splitlines()[0:50].__str__()


def ensure_header(path: Path, header: str, *, autofix: bool = False) -> bool:
    # Semántica "ensure": True si el archivo TERMINA con header (lo tuviera o lo agreguemos)
    if has_header(path, header):
        return True
    if not autofix:
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    # Evita duplicados si corre en paralelo
    if not has_header(path, header):
        path.write_text(f"{header}{'' if header.endswith('\n') else '\n'}{text}", encoding="utf-8")
    return True


def check_headers(root: Path, exts: Sequence[str], license_id: str) -> list[Path]:
    missing: list[Path] = []
    for fp in _iter_files(root, exts):
        hdr = header_for_path(fp, license_id=license_id)
        if not has_header(fp, hdr):
            missing.append(fp)
    return missing


def fix_headers(root: Path, exts: Sequence[str], license_id: str) -> list[Path]:
    fixed: list[Path] = []
    for fp in _iter_files(root, exts):
        hdr = header_for_path(fp, license_id=license_id)
        if ensure_header(fp, hdr, autofix=True):
            fixed.append(fp)
    return fixed


__all__ = [
    "DEFAULT_IGNORES",
    "default_header_text",
    "header_for_path",
    "has_header",
    "has_spdx_header",
    "ensure_header",
    "check_headers",
    "fix_headers",
]
