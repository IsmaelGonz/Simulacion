"""Vista de consola del experimento Monte Carlo."""

from __future__ import annotations

import platform
from pathlib import Path

from model.monte_carlo import (
    DEFAULT_SEED,
    REAL_PI,
    REPETITIONS,
    SAMPLE_SIZES,
    VERIFICATION_PAIRS,
    WARMUP_RUNS,
)


def print_experiment_results(
    rows: list[dict],
    verification: dict,
    python_csv: Path,
    verification_csv: Path,
    global_warmup_runs: int,
) -> None:
    print("=" * 92)
    print("APE 007 - ESTIMACION DE pi MEDIANTE MONTE CARLO - PYTHON")
    print("=" * 92)
    print(f"Python: {platform.python_version()} | Sistema: {platform.platform()}")
    print(f"Generador: SplitMix64 | Semilla: {DEFAULT_SEED}")
    print(
        f"Repeticiones cronometradas: {REPETITIONS} | "
        f"Calentamiento por tamano: {WARMUP_RUNS}"
    )
    print(
        f"Calentamiento global adicional: {global_warmup_runs} x "
        f"{max(SAMPLE_SIZES):,} puntos"
    )
    print(
        f"{'Exp.':<5}{'N':>12}{'Nc':>12}{'pi estimado':>16}"
        f"{'Error absoluto':>18}{'Mediana (ms)':>16}"
    )
    print("-" * 92)
    for row in rows:
        print(
            f"{row['experimento']:<5}{row['n']:>12,}{row['n_c']:>12,}"
            f"{row['pi_estimado']:>16.10f}{row['error_absoluto']:>18.10f}"
            f"{row['tiempo_mediana_ms']:>16.6f}"
        )
    print("-" * 92)
    print(f"Valor real de pi (math.pi): {REAL_PI:.15f}")
    print(
        "Verificacion de secuencia: "
        f"{verification['pares']} pares, SHA-256 = {verification['sha256']}"
    )
    print(f"Resultados Python: {python_csv}")
    print(f"Verificacion Python: {verification_csv}")


def print_comparison(
    combined,
    verification: dict,
    combined_csv: Path,
    verification_report: Path,
    plots_dir: Path,
) -> None:
    print("=" * 100)
    print("APE 007 - COMPARACION PYTHON vs JAVA")
    print("=" * 100)
    print(
        f"{'N':>12}{'Nc':>12}{'pi estimado':>16}{'Error abs.':>16}"
        f"{'T. Python (ms)':>18}{'T. Java (ms)':>16}{'Coincide':>12}"
    )
    print("-" * 100)
    for _, row in combined.iterrows():
        print(
            f"{int(row['n']):>12,}{int(row['n_c']):>12,}"
            f"{row['pi_estimado']:>16.10f}{row['error_absoluto']:>16.10f}"
            f"{row['tiempo_python_ms']:>18.6f}{row['tiempo_java_ms']:>16.6f}"
            f"{('SI' if row['coincide_pi'] else 'NO'):>12}"
        )
    print("-" * 100)
    print(f"Hash Python: {verification['hash_python']}")
    print(f"Hash Java:   {verification['hash_java']}")
    print(f"Hashes iguales: {'SI' if verification['same_hash'] else 'NO'}")
    print(
        "Primeros 10 pares identicos: "
        f"{'SI' if verification['same_first_pairs'] else 'NO'}"
    )
    print(
        f"Nc y pi coinciden en todos los experimentos: "
        f"{'SI' if verification['same_nc'] and verification['same_pi'] else 'NO'}"
    )
    print(f"Tabla combinada: {combined_csv}")
    print(f"Verificacion: {verification_report}")
    print(f"Graficos: {plots_dir}")


def print_error(message: str) -> None:
    import sys

    print(message, file=sys.stderr)
