"""Controlador del experimento Monte Carlo en Python."""

from __future__ import annotations

import statistics
import time
from pathlib import Path

from model.monte_carlo import (
    ExperimentResult,
    REAL_PI,
    REPETITIONS,
    SAMPLE_SIZES,
    VERIFICATION_PAIRS,
    WARMUP_RUNS,
    estimate_pi,
)
from model.results_repository import write_results, write_verification
from model.splitmix64 import DEFAULT_SEED, verify_sequence
from view.console_view import print_experiment_results

PYTHON_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = PYTHON_DIR.parent
RESULTS_DIR = PROJECT_ROOT / "resultados"
PYTHON_CSV = RESULTS_DIR / "resultados_python.csv"
VERIFICATION_PYTHON_CSV = RESULTS_DIR / "verificacion_python.csv"
GLOBAL_WARMUP_RUNS = 2


def ensure_results_dir() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def run_experiment(n: int) -> tuple[ExperimentResult, list[float]]:
    """Ejecuta un experimento con calentamiento y repeticiones cronometradas."""
    warmup = estimate_pi(n, DEFAULT_SEED)

    times_ms: list[float] = []
    last_result = warmup
    for _ in range(REPETITIONS):
        start_ns = time.perf_counter_ns()
        last_result = estimate_pi(n, DEFAULT_SEED)
        elapsed_ns = time.perf_counter_ns() - start_ns
        times_ms.append(elapsed_ns / 1_000_000.0)

    if last_result.n_c != warmup.n_c:
        raise RuntimeError(
            "El generador no es determinista: Nc cambio entre repeticiones."
        )

    return last_result, times_ms


def build_rows() -> list[dict]:
    rows: list[dict] = []
    for experiment, n in enumerate(SAMPLE_SIZES, start=1):
        result, times = run_experiment(n)
        row = {
            "experimento": experiment,
            "n": result.n,
            "n_c": result.n_c,
            "pi_estimado": result.pi_estimate,
            "error_absoluto": result.absolute_error,
            "pi_real": REAL_PI,
            "semilla": result.seed,
            "repeticiones": REPETITIONS,
            "tiempo_rep1_ms": times[0] if len(times) > 0 else 0.0,
            "tiempo_rep2_ms": times[1] if len(times) > 1 else 0.0,
            "tiempo_rep3_ms": times[2] if len(times) > 2 else 0.0,
            "tiempo_mediana_ms": statistics.median(times),
            "tiempo_promedio_ms": statistics.mean(times),
            "tiempo_minimo_ms": min(times),
            "tiempo_desv_std_ms": statistics.stdev(times) if len(times) > 1 else 0.0,
        }
        rows.append(row)
    return rows


def run_experiments() -> int:
    ensure_results_dir()
    for _ in range(GLOBAL_WARMUP_RUNS):
        estimate_pi(max(SAMPLE_SIZES), DEFAULT_SEED)

    rows = build_rows()
    verification = verify_sequence(VERIFICATION_PAIRS, DEFAULT_SEED)

    write_results(rows, PYTHON_CSV)
    write_verification(
        verification["primeros_pares"], verification["sha256"], VERIFICATION_PYTHON_CSV
    )
    print_experiment_results(
        rows,
        verification,
        PYTHON_CSV,
        VERIFICATION_PYTHON_CSV,
        GLOBAL_WARMUP_RUNS,
    )
    return 0
