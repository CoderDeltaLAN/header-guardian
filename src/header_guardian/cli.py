# Copyright 2025 CoderDeltaLAN
# SPDX-License-Identifier: MIT

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path

import click

from .core import ensure_header
from .headers import header_for_path

IGNORED_DIRS: set[str] = {
    ".git",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    "node_modules",
    "vendor",
}


def iter_files(root: Path, exts: Sequence[str]) -> Iterable[Path]:
    exts_norm = {e if e.startswith(".") else f".{e}" for e in exts}
    for p in root.rglob("*"):
        if p.is_file():
            if any(parent.name in IGNORED_DIRS for parent in p.parents):
                continue
            if not exts_norm or p.suffix in exts_norm:
                yield p


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--path", "path_str", default=".", show_default=True, help="Raíz a escanear.")
@click.option(
    "--ext",
    "exts",
    multiple=True,
    default=[".py"],
    show_default=True,
    help="Extensiones a procesar (repetible).",
)
@click.option(
    "--mode",
    type=click.Choice(["check", "fix"], case_sensitive=False),
    default="check",
    show_default=True,
    help="Modo de operación: validar o insertar encabezado.",
)
@click.option(
    "--header-file",
    "header_file",
    type=click.Path(dir_okay=False, exists=True, readable=True, path_type=Path),
    default=None,
    help="Archivo de texto con el header exacto a usar (si se provee, no se adapta por extensión).",
)
def main(path_str: str, exts: Sequence[str], mode: str, header_file: Path | None) -> None:
    root = Path(path_str).resolve()
    custom_header = header_file.read_text(encoding="utf-8") if header_file else None
    missing = 0

    for file in iter_files(root, exts):
        header = custom_header if custom_header is not None else header_for_path(file)
        ok = ensure_header(file, header, autofix=(mode.lower() == "fix"))
        if not ok:
            missing += 1

    if mode.lower() == "check":
        if missing > 0:
            click.echo(f"Missing header in {missing} file(s).", err=True)
            raise SystemExit(1)
        click.echo("All files have the required header.")
        return

    if missing > 0:
        click.echo(f"Some files were not fixed: {missing}", err=True)
        raise SystemExit(1)
    click.echo("Headers ensured.")
