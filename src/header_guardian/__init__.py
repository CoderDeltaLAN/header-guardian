from __future__ import annotations

__all__: list[str] = ["ping", "__version__"]

__version__ = "0.1.1"


def ping() -> str:
    return "pong"
