"""Punto de entrada Python - APE 007 - Monte Carlo para estimar pi.

Uso:
    py python\\main.py              # ejecuta los cuatro experimentos en Python
    py python\\main.py --comparar   # compara con Java y genera CSV y graficos

El programa no ejecuta Java automaticamente. Ejecute primero ambas
implementaciones y despues la comparacion.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from controller.comparison_controller import run_comparison
from controller.experiment_controller import run_experiments

PYTHON_DIR = Path(__file__).resolve().parent


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="APE 007 - Monte Carlo para estimar pi (Python)"
    )
    parser.add_argument(
        "--comparar",
        action="store_true",
        help="comparar los resultados de Python y Java, y generar graficos",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    if args.comparar:
        return run_comparison()
    return run_experiments()


if __name__ == "__main__":
    raise SystemExit(main())
