from __future__ import annotations

from pathlib import Path

from header_guardian.core import check_headers, fix_headers, has_spdx_header


def test_adds_and_detects_header(tmp_path: Path) -> None:
    f = tmp_path / "a.py"
    f.write_text("print('x')\n", encoding="utf-8")
    missing = check_headers(tmp_path, [".py"], "MIT")
    assert f in missing
    fixed = fix_headers(tmp_path, [".py"], "MIT")
    assert f in fixed
    txt = f.read_text(encoding="utf-8")
    assert has_spdx_header(txt)
