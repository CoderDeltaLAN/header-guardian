from __future__ import annotations
import sys
from pathlib import Path
import click
from .core import check_headers, fix_headers

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--path", "path", type=click.Path(file_okay=False, path_type=Path), default=Path("."), show_default=True, help="Raíz a escanear.")
@click.option("--ext", "exts", type=str, multiple=True, default=[".py"], show_default=True, help="Extensiones a validar (repetible).")
@click.option("--mode", type=click.Choice(["check", "fix"]), default="check", show_default=True, help="Solo validar o corregir.")
@click.option("--license-id", type=str, default="MIT", show_default=True, help="SPDX License Identifier a exigir.")
def main(path: Path, exts: tuple[str, ...], mode: str, license_id: str) -> None:
    if mode == "check":
        missing = check_headers(path, list(exts), license_id)
        if missing:
            click.echo("Archivos sin header SPDX:", err=True)
            for m in missing:
                click.echo(f"- {m}", err=True)
            sys.exit(1)
        click.echo("OK: todos los archivos tienen header SPDX.")
        return
    # fix
    fixed = fix_headers(path, list(exts), license_id)
    if fixed:
        click.echo("Añadidos headers SPDX a:")
        for f in fixed:
            click.echo(f"- {f}")
    else:
        click.echo("Nada que corregir; todo en orden.")

if __name__ == "__main__":
    main()
