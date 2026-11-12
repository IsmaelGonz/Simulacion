"""Repositorio de resultados del modelo.

Encapsula la lectura y escritura de los archivos CSV utilizados por el
experimento Monte Carlo y por la comparacion entre lenguajes.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from model.splitmix64 import double_bits_hex

RESULT_COLUMNS = {
    "experimento",
    "n",
    "n_c",
    "pi_estimado",
    "error_absoluto",
    "tiempo_mediana_ms",
}
VERIFICATION_COLUMNS = {"indice", "x_bits_hex", "y_bits_hex", "sha256_2000_uniformes"}


def write_results(rows: list[dict], path: Path) -> None:
    """Escribe las filas de resultados de una implementacion."""
    pd.DataFrame(rows).to_csv(path, index=False, float_format="%.12f")


def write_verification(
    first_pairs: list[tuple[int, float, float]],
    sha256: str,
    path: Path,
) -> None:
    """Escribe los primeros pares y la huella de la secuencia verificada."""
    rows = [
        {
            "indice": index,
            "x_bits_hex": double_bits_hex(x),
            "y_bits_hex": double_bits_hex(y),
            "sha256_2000_uniformes": sha256,
        }
        for index, x, y in first_pairs
    ]
    pd.DataFrame(rows).to_csv(path, index=False)


def read_results(path: Path, language: str) -> pd.DataFrame:
    """Lee y valida el CSV de resultados de un lenguaje."""
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontro {path.name}. Ejecute primero la implementacion {language}."
        )
    frame = pd.read_csv(path)
    missing = RESULT_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"{path.name} no contiene las columnas: {sorted(missing)}")
    return frame.sort_values("n").reset_index(drop=True)


def read_verification(path: Path, language: str) -> pd.DataFrame:
    """Lee y valida el CSV de verificacion de un lenguaje."""
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontro {path.name}. Ejecute primero la implementacion {language}."
        )
    frame = pd.read_csv(path)
    missing = VERIFICATION_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"{path.name} no contiene las columnas: {sorted(missing)}")
    return frame


def write_combined(frame: pd.DataFrame, path: Path) -> None:
    """Escribe la tabla comparativa combinada."""
    frame.to_csv(path, index=False, float_format="%.12f")
