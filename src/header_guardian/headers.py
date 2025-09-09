# Copyright 2025 CoderDeltaLAN
# SPDX-License-Identifier: MIT

from __future__ import annotations

from datetime import datetime
from pathlib import Path

_BASE_LINES = [
    "Copyright {year} CoderDeltaLAN",
    "SPDX-License-Identifier: MIT",
]

_LINE_PREFIX_BY_EXT = {
    ".py": "# ",
    ".sh": "# ",
    ".yaml": "# ",
    ".yml": "# ",
    ".toml": "# ",
    ".ini": "; ",
    ".js": "// ",
    ".jsx": "// ",
    ".ts": "// ",
    ".tsx": "// ",
    ".go": "// ",
    ".rs": "// ",
    ".c": "// ",
    ".h": "// ",
    ".cpp": "// ",
    ".hpp": "// ",
}


def _render_with_prefix(prefix: str) -> str:
    year = datetime.now().year
    lines = [line.format(year=year) for line in _BASE_LINES]
    return "".join(f"{prefix}{line}\n" for line in lines) + "\n"


def header_for_extension(ext: str) -> str:
    prefix = _LINE_PREFIX_BY_EXT.get(ext.lower(), "# ")
    return _render_with_prefix(prefix)


def header_for_path(path: Path) -> str:
    return header_for_extension(path.suffix)


def default_header_text() -> str:
    # compat: por defecto estilo Python/hash
    return _render_with_prefix("# ")
