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
    return f"{_comment_prefix(ext)}SPDX-License-Identifier: {license_id}"


def header_for_path(path: Path, license_id: str = "MIT") -> str:
    return default_header_text(license_id=license_id, ext=path.suffix)


def has_header(path: Path, header: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    head_lines = text.splitlines()[:30]
    head = "\n".join(head_lines)
    return _normalize(header) in _normalize(head)


def ensure_header(path: Path, header: str, *, autofix: bool = False) -> bool:
    if has_header(path, header):
        return False
    if not autofix:
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    new = f"{header}\n{text}"
    path.write_text(new, encoding="utf-8")
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
    "ensure_header",
    "check_headers",
    "fix_headers",
]
