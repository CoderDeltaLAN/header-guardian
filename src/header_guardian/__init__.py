from __future__ import annotations

__all__: list[str] = ["ping", "__version__"]


def ping() -> str:
    return "pong"


__version__ = "0.1.0"
