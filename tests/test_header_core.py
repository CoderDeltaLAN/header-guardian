# Copyright 2025 CoderDeltaLAN
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

from header_guardian.core import ensure_header, has_header
from header_guardian.headers import default_header_text


def test_ensure_and_check(tmp_path: Path) -> None:
    test_file = tmp_path / "sample.py"
    test_file.write_text("print('hi')\n", encoding="utf-8")

    header = default_header_text()

    assert not has_header(test_file, header)
    assert ensure_header(test_file, header, autofix=True) is True
    assert has_header(test_file, header)
    # idempotente
    assert ensure_header(test_file, header, autofix=True) is True
