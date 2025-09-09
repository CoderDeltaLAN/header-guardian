# Copyright 2025 CoderDeltaLAN
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

from header_guardian.core import ensure_header, has_header
from header_guardian.headers import header_for_path


def test_ts_header(tmp_path: Path) -> None:
    f = tmp_path / "sample.ts"
    f.write_text("console.log('hi');\n", encoding="utf-8")
    header = header_for_path(f)
    assert not has_header(f, header)
    assert ensure_header(f, header, autofix=True)
    assert has_header(f, header)
    text = f.read_text(encoding="utf-8")
    assert text.startswith("// ")
