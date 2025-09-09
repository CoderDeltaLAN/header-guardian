# Copyright 2025 CoderDeltaLAN
# SPDX-License-Identifier: MIT

import header_guardian as hg


def test_ping() -> None:
    assert hg.ping() == "pong"
