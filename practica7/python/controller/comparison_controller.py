"""Controlador de comparacion entre Python y Java."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from model.monte_carlo import VERIFICATION_PAIRS
from model.results_repository import (
    read_results,
    read_verification,
    write_combined,
)
from view.console_view import print_comparison, print_error
from view.plots import generate_plots
from view.report_view import write_verification_report

PYTHON_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = PYTHON_DIR.parent
RESULTS_DIR = PROJECT_ROOT / "resultados"
PYTHON_CSV = RESULTS_DIR / "resultados_python.csv"
JAVA_CSV = RESULTS_DIR / "resultados_java.csv"
COMBINED_CSV = RESULTS_DIR / "resultados.csv"
VERIFICATION_PYTHON_CSV = RESULTS_DIR / "verificacion_python.csv"
VERIFICATION_JAVA_CSV = RESULTS_DIR / "verificacion_java.csv"
VERIFICATION_REPORT = RESULTS_DIR / "verificacion.txt"


def _build_combined(python_frame: pd.DataFrame, java_frame: pd.DataFrame) -> pd.DataFrame:
    if len(python_frame) != len(java_frame):
        raise ValueError("Python y Java no tienen el mismo numero de experimentos.")

    combined = pd.DataFrame(
        {
            "experimento": python_frame["experimento"].astype(int),
            "n": python_frame["n"].astype(int),
            "n_c": python_frame["n_c"].astype(int),
            "pi_estimado": python_frame["pi_estimado"].astype(float),
            "error_absoluto": python_frame["error_absoluto"].astype(float),
            "pi_python": python_frame["pi_estimado"].astype(float),
            "error_python": python_frame["error_absoluto"].astype(float),
            "tiempo_python_ms": python_frame["tiempo_mediana_ms"].astype(float),
            "pi_java": java_frame["pi_estimado"].astype(float),
            "error_java": java_frame["error_absoluto"].astype(float),
            "tiempo_java_ms": java_frame["tiempo_mediana_ms"].astype(float),
        }
    )

    pi_python = combined["pi_python"].to_numpy(dtype=float)
    pi_java = combined["pi_java"].to_numpy(dtype=float)
    nc_python = python_frame["n_c"].to_numpy()
    nc_java = java_frame["n_c"].to_numpy()

    combined["diferencia_pi"] = np.abs(pi_python - pi_java)
    combined["coincide_nc"] = np.equal(nc_python, nc_java)
    combined["coincide_pi"] = np.logical_and(
        np.isclose(pi_python, pi_java, rtol=0.0, atol=1e-12),
        combined["coincide_nc"].to_numpy(),
    )
    return combined


def _verify_sequences(
    verification_python: pd.DataFrame,
    verification_java: pd.DataFrame,
    combined: pd.DataFrame,
) -> dict:
    hash_python = str(verification_python["sha256_2000_uniformes"].iloc[0])
    hash_java = str(verification_java["sha256_2000_uniformes"].iloc[0])
    same_hash = hash_python == hash_java

    columns = ["indice", "x_bits_hex", "y_bits_hex"]
    same_first_pairs = verification_python[columns].equals(
        verification_java[columns]
    )
    same_nc = bool(combined["coincide_nc"].all())
    same_pi = bool(combined["coincide_pi"].all())

    return {
        "hash_python": hash_python,
        "hash_java": hash_java,
        "same_hash": same_hash,
        "same_first_pairs": same_first_pairs,
        "same_nc": same_nc,
        "same_pi": same_pi,
        "pairs": VERIFICATION_PAIRS,
        "shown_pairs": int(verification_python["indice"].max()),
    }


def run_comparison() -> int:
    try:
        python_frame = read_results(PYTHON_CSV, "Python")
        java_frame = read_results(JAVA_CSV, "Java")
        verification_python = read_verification(
            VERIFICATION_PYTHON_CSV, "Python"
        )
        verification_java = read_verification(VERIFICATION_JAVA_CSV, "Java")
    except (FileNotFoundError, ValueError) as error:
        print_error(f"Error: {error}")
        return 1

    try:
        combined = _build_combined(python_frame, java_frame)
    except ValueError as error:
        print_error(f"Error: {error}")
        return 1

    verification = _verify_sequences(
        verification_python, verification_java, combined
    )

    write_combined(combined, COMBINED_CSV)
    write_verification_report(verification, VERIFICATION_REPORT)
    generate_plots(combined, RESULTS_DIR)
    print_comparison(
        combined,
        verification,
        COMBINED_CSV,
        VERIFICATION_REPORT,
        RESULTS_DIR,
    )

    if not (
        verification["same_hash"]
        and verification["same_first_pairs"]
        and verification["same_nc"]
        and verification["same_pi"]
    ):
        print_error(
            "Advertencia: las implementaciones no produjeron exactamente los "
            "mismos resultados."
        )
        return 2

    return 0
