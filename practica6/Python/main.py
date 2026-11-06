"""Programa principal de la practica APE 006 - implementacion Python.

Uso:
    py Python/main.py                 # menu interactivo
    py Python/main.py --all           # genera todos los resultados Python
    py Python/main.py --generate 10000
    py Python/main.py --chi
    py Python/main.py --ks
    py Python/main.py --compare
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import pandas as pd

from chi_square import chi_square_rows, format_chi_square_report, run_chi_square
from kolmogorov_smirnov import format_ks_report, run_ks
from lcg import Lcg, LcgParameters, sample_text
from plots import plot_chi_square, plot_histogram, plot_ks

PYTHON_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PYTHON_DIR.parent
RESULTS_DIR = PYTHON_DIR / "resultados"
DATA_DIR = RESULTS_DIR / "datos"
PLOTS_DIR = RESULTS_DIR / "graficas"

DEFAULT_N = 10_000


def ensure_directories() -> None:
    for directory in (DATA_DIR, PLOTS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def hash_states(states: Sequence[int]) -> str:
    digest = hashlib.sha256()
    for state in states:
        digest.update(int(state).to_bytes(4, "little"))
    return digest.hexdigest()


def generate_sequence(n: int = DEFAULT_N, save: bool = True) -> Dict:
    ensure_directories()
    lcg = Lcg(LcgParameters())
    states = lcg.generate_states(n)
    values = [state / lcg.parameters.m for state in states]

    if save:
        frame = pd.DataFrame(
            {
                "indice": range(1, n + 1),
                "estado": states,
                "u": values,
            }
        )
        filename = "python_secuencia_10000.csv" if n == DEFAULT_N else f"python_secuencia_{n}.csv"
        frame.to_csv(DATA_DIR / filename, index=False)

    return {
        "n": n,
        "states": states,
        "values": values,
        "sha256": hash_states(states),
        "parametros": lcg.parameters.as_dict(),
    }


def save_json(path: Path, data: Dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def build_results_document(
    sequence: Dict,
    chi_result: Dict,
    ks_result: Dict,
) -> Dict:
    return {
        "lenguaje": "Python",
        "parametros": sequence["parametros"],
        "secuencia": {
            "n": sequence["n"],
            "sha256_estados": sequence["sha256"],
            "primeros_estados": sequence["states"][:10],
            "primeros_valores": sequence["values"][:10],
            "minimo": min(sequence["values"]),
            "maximo": max(sequence["values"]),
            "archivo": "Python/resultados/datos/python_secuencia_10000.csv",
        },
        "chi_cuadrado": chi_result,
        "kolmogorov_smirnov": ks_result,
        "entorno": {
            "python": platform.python_version(),
            "plataforma": platform.platform(),
            "numpy": _module_version("numpy"),
            "pandas": _module_version("pandas"),
            "matplotlib": _module_version("matplotlib"),
        },
    }


def _module_version(name: str) -> str:
    try:
        module = __import__(name)
        return getattr(module, "__version__", "desconocida")
    except Exception:
        return "no disponible"


def run_all(verbose: bool = True) -> Dict:
    ensure_directories()
    sequence = generate_sequence(DEFAULT_N, save=True)
    values = sequence["values"]

    chi_result = run_chi_square(values, bins=10, alpha=0.05)
    ks_result = run_ks(values, alpha=0.05)

    pd.DataFrame(chi_square_rows(chi_result)).to_csv(
        DATA_DIR / "python_chi_cuadrado.csv", index=False
    )

    document = build_results_document(sequence, chi_result, ks_result)
    save_json(DATA_DIR / "python_resultados.json", document)

    (DATA_DIR / "muestra_python.txt").write_text(
        sample_text(values, 10) + "\n", encoding="utf-8"
    )

    plot_histogram(values, PLOTS_DIR / "python_histograma.png")
    plot_chi_square(chi_result, PLOTS_DIR / "python_chi_cuadrado.png")
    plot_ks(values, ks_result, PLOTS_DIR / "python_kolmogorov_smirnov.png")

    if verbose:
        print("=" * 70)
        print("APE 006 - VALIDACION ESTADISTICA - PYTHON")
        print("=" * 70)
        print("Parametros LCG:", sequence["parametros"])
        print(f"Secuencia generada: {sequence['n']} numeros")
        print(f"SHA-256 de estados: {sequence['sha256']}")
        print("Muestra inicial:")
        print(sample_text(values, 10))
        print()
        print(format_chi_square_report(chi_result))
        print()
        print(format_ks_report(ks_result))
        print()
        print("Archivos generados en:", RESULTS_DIR)

    return {
        "sequence": sequence,
        "chi": chi_result,
        "ks": ks_result,
        "document": document,
    }


def run_comparison_script(reuse: bool = False, skip_python: bool = False) -> int:
    script = PROJECT_ROOT / "Python" / "comparacion_resultados.py"
    if not script.exists():
        print("No se encontro comparacion_resultados.py.")
        return 1
    command = [sys.executable, str(script)]
    if reuse:
        command.append("--reuse")
    if skip_python:
        command.append("--skip-python")
    return subprocess.call(command, cwd=str(PROJECT_ROOT))


def _load_generated_values() -> List[float]:
    path = DATA_DIR / "python_secuencia_10000.csv"
    if not path.exists():
        return generate_sequence(DEFAULT_N, save=True)["values"]
    frame = pd.read_csv(path)
    return frame["u"].astype(float).tolist()


def interactive_menu() -> None:
    current_values: List[float] | None = None
    while True:
        print()
        print("=" * 62)
        print("APE 006 - SIMULACION - MENU PRINCIPAL (Python)")
        print("=" * 62)
        print("1. Generar numeros pseudoaleatorios")
        print("2. Ejecutar prueba Chi-cuadrado")
        print("3. Ejecutar prueba Kolmogorov-Smirnov")
        print("4. Ejecutar comparacion Python vs Java")
        print("5. Generar todas las pruebas y resultados")
        print("6. Salir")

        option = input("Seleccione una opcion: ").strip()
        if option == "1":
            raw = input(f"Cantidad de numeros [{DEFAULT_N}]: ").strip()
            n = int(raw) if raw else DEFAULT_N
            sequence = generate_sequence(n, save=True)
            current_values = sequence["values"]
            print(f"Generados {n} numeros. SHA-256: {sequence['sha256']}")
            print(sample_text(current_values, 10))
        elif option == "2":
            current_values = current_values or _load_generated_values()
            print(format_chi_square_report(run_chi_square(current_values)))
        elif option == "3":
            current_values = current_values or _load_generated_values()
            print(format_ks_report(run_ks(current_values)))
        elif option == "4":
            run_comparison_script()
        elif option == "5":
            run_all(verbose=True)
            print()
            print("Ejecutando comparacion automatica con Java...")
            run_comparison_script(skip_python=True)
        elif option == "6":
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida.")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="APE 006 - Python")
    parser.add_argument("--all", action="store_true", help="generar todos los resultados")
    parser.add_argument("--generate", type=int, nargs="?", const=DEFAULT_N,
                        help="generar una secuencia de N numeros")
    parser.add_argument("--chi", action="store_true", help="ejecutar Chi-cuadrado")
    parser.add_argument("--ks", action="store_true", help="ejecutar Kolmogorov-Smirnov")
    parser.add_argument("--compare", action="store_true", help="comparar Python vs Java")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    if not any([args.all, args.generate is not None, args.chi, args.ks, args.compare]):
        interactive_menu()
        return 0

    if args.all:
        run_all(verbose=True)
    if args.generate is not None:
        sequence = generate_sequence(args.generate, save=True)
        print(f"Secuencia de {args.generate} numeros generada.")
        print(f"SHA-256: {sequence['sha256']}")
        print(sample_text(sequence["values"], 10))
    if args.chi:
        values = _load_generated_values()
        print(format_chi_square_report(run_chi_square(values)))
    if args.ks:
        values = _load_generated_values()
        print(format_ks_report(run_ks(values)))
    if args.compare:
        return run_comparison_script()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
