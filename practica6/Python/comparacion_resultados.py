"""Comparacion automatica de las implementaciones Python y Java.

Por defecto ejecuta realmente ambos programas (Python y Java), luego compara
los archivos JSON/CSV producidos e imprime el resultado en consola.

Uso:
    py Python/comparacion_resultados.py                 # ejecuta ambos y compara
    py Python/comparacion_resultados.py --reuse         # reutiliza resultados existentes
    py Python/comparacion_resultados.py --skip-python   # no vuelve a ejecutar Python
    py Python/comparacion_resultados.py --skip-java     # no vuelve a ejecutar Java
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYTHON_DATA_DIR = PROJECT_ROOT / "Python" / "resultados" / "datos"
JAVA_DATA_DIR = PROJECT_ROOT / "Java" / "resultados" / "datos"
PYTHON_JSON = PYTHON_DATA_DIR / "python_resultados.json"
JAVA_JSON = JAVA_DATA_DIR / "java_resultados.json"
PYTHON_CSV = PYTHON_DATA_DIR / "python_secuencia_10000.csv"
JAVA_CSV = JAVA_DATA_DIR / "java_secuencia_10000.csv"

SEQUENCE_TOLERANCE = 1.0e-15
STATISTIC_TOLERANCE = 1.0e-9
KS_TOLERANCE = 1.0e-12
P_TOLERANCE = 1.0e-6


class Check:
    def __init__(self, name: str, passed: bool, detail: str) -> None:
        self.name = name
        self.passed = passed
        self.detail = detail


def run_python() -> None:
    print("Ejecutando implementacion Python (--all)...")
    command = [sys.executable, str(PROJECT_ROOT / "Python" / "main.py"), "--all"]
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def run_java() -> None:
    javac = shutil.which("javac")
    java = shutil.which("java")
    if not javac or not java:
        raise RuntimeError("No se encontro javac/java en el PATH.")
    sources = sorted((PROJECT_ROOT / "Java" / "src" / "ape006").glob("*.java"))
    if not sources:
        raise RuntimeError("No se encontraron fuentes Java.")
    output = PROJECT_ROOT / "Java" / "out"
    output.mkdir(parents=True, exist_ok=True)
    print("Compilando implementacion Java...")
    compile_command = [javac, "-encoding", "UTF-8", "-d", str(output)] + [str(s) for s in sources]
    subprocess.run(compile_command, cwd=PROJECT_ROOT, check=True)
    print("Ejecutando implementacion Java (--all)...")
    run_command = [java, "-cp", str(output), "ape006.Main", "--all"]
    subprocess.run(run_command, cwd=PROJECT_ROOT, check=True)


def ensure_results(args: argparse.Namespace) -> None:
    PYTHON_DATA_DIR.mkdir(parents=True, exist_ok=True)
    JAVA_DATA_DIR.mkdir(parents=True, exist_ok=True)

    need_python = not args.skip_python and (not args.reuse or not PYTHON_JSON.exists())
    need_java = not args.skip_java and (not args.reuse or not JAVA_JSON.exists())

    if need_python:
        run_python()
    elif not PYTHON_JSON.exists():
        raise FileNotFoundError("No existe python_resultados.json.")
    if need_java:
        run_java()
    elif not JAVA_JSON.exists():
        raise FileNotFoundError("No existe java_resultados.json.")


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def close_enough(left: float, right: float, tolerance: float) -> bool:
    return abs(left - right) <= tolerance or abs(left - right) <= tolerance * max(
        1.0, abs(left)
    )


def compare_sequences(python: Dict, java: Dict) -> List[Check]:
    checks: List[Check] = []
    checks.append(
        Check(
            "Parametros del LCG",
            python["parametros"] == java["parametros"],
            str(python["parametros"]),
        )
    )

    py_hash = python["secuencia"]["sha256_estados"]
    jv_hash = java["secuencia"]["sha256_estados"]
    checks.append(
        Check("Secuencia de 10 000 numeros (SHA-256)", py_hash == jv_hash,
              f"Python={py_hash}; Java={jv_hash}")
    )

    py_first = np.asarray(python["secuencia"]["primeros_valores"], dtype=float)
    jv_first = np.asarray(java["secuencia"]["primeros_valores"], dtype=float)
    first_ok = py_first.shape == jv_first.shape and bool(
        np.allclose(py_first, jv_first, rtol=0.0, atol=SEQUENCE_TOLERANCE)
    )
    checks.append(
        Check("Primeros 10 valores pseudoaleatorios", first_ok,
              f"tolerancia absoluta {SEQUENCE_TOLERANCE:g}")
    )

    if PYTHON_CSV.exists() and JAVA_CSV.exists():
        py_csv = pd.read_csv(PYTHON_CSV)
        jv_csv = pd.read_csv(JAVA_CSV)
        states_ok = (
            len(py_csv) == len(jv_csv)
            and int(py_csv["estado"].iloc[0]) == int(jv_csv["estado"].iloc[0])
            and py_csv["estado"].equals(jv_csv["estado"])
        )
        checks.append(
            Check("Estados completos en CSV", states_ok,
                  f"{len(py_csv)} estados comparados exactamente")
        )
        u_ok = bool(np.allclose(py_csv["u"].to_numpy(), jv_csv["u"].to_numpy(),
                                rtol=0.0, atol=SEQUENCE_TOLERANCE))
        checks.append(
            Check("Valores U completos en CSV", u_ok,
                  f"tolerancia absoluta {SEQUENCE_TOLERANCE:g}")
        )
    return checks


def compare_chi_square(python: Dict, java: Dict) -> List[Check]:
    py = python["chi_cuadrado"]
    jv = java["chi_cuadrado"]
    checks = [
        Check(
            "Frecuencias observadas Chi-cuadrado",
            py["frecuencias_observadas"] == jv["frecuencias_observadas"],
            f"Python={py['frecuencias_observadas']}; Java={jv['frecuencias_observadas']}",
        ),
        Check(
            "Frecuencias esperadas Chi-cuadrado",
            close_enough(py["frecuencias_esperadas"][0],
                         jv["frecuencias_esperadas"][0], STATISTIC_TOLERANCE),
            f"{py['frecuencias_esperadas'][0]} por intervalo",
        ),
        Check(
            "Estadistico Chi-cuadrado",
            close_enough(py["estadistico"], jv["estadistico"], STATISTIC_TOLERANCE),
            f"Python={py['estadistico']:.12f}; Java={jv['estadistico']:.12f}",
        ),
        Check(
            "Grados de libertad Chi-cuadrado",
            py["grados_libertad"] == jv["grados_libertad"],
            f"Python={py['grados_libertad']}; Java={jv['grados_libertad']}",
        ),
        Check(
            "Valor p Chi-cuadrado",
            close_enough(py["valor_p"], jv["valor_p"], P_TOLERANCE),
            f"Python={py['valor_p']:.12f}; Java={jv['valor_p']:.12f}",
        ),
        Check(
            "Decision Chi-cuadrado",
            py["rechazar_h0"] == jv["rechazar_h0"] and py["alpha"] == jv["alpha"],
            f"rechazar_h0 Python={py['rechazar_h0']}; Java={jv['rechazar_h0']}; "
            f"alpha={py['alpha']}",
        ),
    ]
    return checks


def compare_ks(python: Dict, java: Dict) -> List[Check]:
    py = python["kolmogorov_smirnov"]
    jv = java["kolmogorov_smirnov"]
    return [
        Check(
            "Diferencia positiva D+",
            close_enough(py["d_mas"], jv["d_mas"], KS_TOLERANCE),
            f"Python={py['d_mas']:.12f}; Java={jv['d_mas']:.12f}",
        ),
        Check(
            "Diferencia negativa D-",
            close_enough(py["d_menos"], jv["d_menos"], KS_TOLERANCE),
            f"Python={py['d_menos']:.12f}; Java={jv['d_menos']:.12f}",
        ),
        Check(
            "Estadistico D de Kolmogorov-Smirnov",
            close_enough(py["estadistico_d"], jv["estadistico_d"], KS_TOLERANCE),
            f"Python={py['estadistico_d']:.12f}; Java={jv['estadistico_d']:.12f}",
        ),
        Check(
            "Valor p Kolmogorov-Smirnov",
            close_enough(py["valor_p"], jv["valor_p"], P_TOLERANCE),
            f"Python={py['valor_p']:.12f}; Java={jv['valor_p']:.12f}",
        ),
        Check(
            "Decision Kolmogorov-Smirnov",
            py["rechazar_h0"] == jv["rechazar_h0"] and py["alpha"] == jv["alpha"],
            f"rechazar_h0 Python={py['rechazar_h0']}; Java={jv['rechazar_h0']}",
        ),
    ]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Comparacion Python vs Java")
    parser.add_argument("--reuse", action="store_true",
                        help="reutilizar resultados existentes en lugar de regenerarlos")
    parser.add_argument("--skip-python", action="store_true",
                        help="no ejecutar la implementacion Python")
    parser.add_argument("--skip-java", action="store_true",
                        help="no ejecutar la implementacion Java")
    args = parser.parse_args(argv)

    try:
        ensure_results(args)
    except Exception as exception:
        print(f"Error al ejecutar las implementaciones: {exception}", file=sys.stderr)
        return 1

    python = load_json(PYTHON_JSON)
    java = load_json(JAVA_JSON)

    checks: List[Check] = []
    checks.extend(compare_sequences(python, java))
    checks.extend(compare_chi_square(python, java))
    checks.extend(compare_ks(python, java))

    all_passed = all(check.passed for check in checks)

    print()
    print("=" * 72)
    print("COMPARACION PYTHON VS JAVA")
    print("=" * 72)
    for check in checks:
        print(f"[{'OK' if check.passed else 'FALLA'}] {check.name}: {check.detail}")
    print("-" * 72)
    print("RESULTADO:", "EQUIVALENTES" if all_passed else "SE ENCONTRARON DIFERENCIAS")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
