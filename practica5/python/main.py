"""Punto de entrada de la implementación Python de la práctica LCG.

Genera 10 000 valores con la semilla 12 345, guarda el CSV, analiza el
período, calcula estadísticas descriptivas y crea las gráficas. También genera
una segunda secuencia con semilla 54 321 para estudiar el efecto de la semilla.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from analisis import (
    analizar_periodo,
    calcular_estadisticas,
    imprimir_analisis_periodo,
    imprimir_estadisticas,
    verificar_condiciones_periodo_maximo,
)
from generador_lcg import (
    CANTIDAD_POR_DEFECTO,
    ParametrosLCG,
    SEMILLA_POR_DEFECTO,
    generar_secuencia,
)
from graficas import generar_todas_las_graficas


# Si la consola de Windows no usa UTF-8, se fuerza para mostrar tildes y símbolos.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DIRECTORIO_PYTHON = Path(__file__).resolve().parent
RAIZ_PROYECTO = DIRECTORIO_PYTHON.parent
DIRECTORIO_RESULTADOS = DIRECTORIO_PYTHON / "resultados"
DIRECTORIO_GRAFICAS = DIRECTORIO_PYTHON / "graficas"

SEMILLA_ALTERNA = 54_321


def guardar_secuencia_csv(
    ruta_salida: Path,
    secuencia: list[tuple[int, float]],
) -> Path:
    """Guarda la secuencia generada en un archivo CSV con columnas iteracion, X, U."""
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    with ruta_salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        escritor.writerow(["iteracion", "X", "U"])
        for iteracion, (x, u) in enumerate(secuencia, start=1):
            escritor.writerow([iteracion, x, f"{u:.12f}"])
    return ruta_salida


def mostrar_primeros_valores(
    secuencia: list[tuple[int, float]],
    cantidad: int = 5,
) -> None:
    """Muestra en consola los primeros valores generados."""
    print(f"\nPrimeros {cantidad} valores generados:")
    print(f"{'n':>6}  {'X(n)':>12}  {'U(n)':>14}")
    print("-" * 38)
    for iteracion, (x, u) in enumerate(secuencia[:cantidad], start=1):
        print(f"{iteracion:6d}  {x:12d}  {u:14.12f}")


def main() -> None:
    print("=" * 72)
    print("PRÁCTICA 05 - GENERADOR CONGRUENCIAL LINEAL (LCG)")
    print("=" * 72)

    parametros = ParametrosLCG()
    print("Parámetros utilizados:")
    print(f"  a (multiplicador) = {parametros.multiplicador}")
    print(f"  c (incremento)    = {parametros.incremento}")
    print(f"  m (módulo)        = {parametros.modulo}")
    print(f"  X0 (semilla)      = {parametros.semilla}")
    print(f"  cantidad          = {CANTIDAD_POR_DEFECTO}")

    print("\nGenerando la secuencia principal en Python...")
    secuencia = generar_secuencia(
        cantidad=CANTIDAD_POR_DEFECTO,
        semilla=SEMILLA_POR_DEFECTO,
    )
    ruta_csv = guardar_secuencia_csv(
        DIRECTORIO_RESULTADOS / "secuencia_python.csv",
        secuencia,
    )
    mostrar_primeros_valores(secuencia)
    print(f"\nCSV principal guardado en: {ruta_csv}")

    print("\nGenerando la secuencia con la semilla alterna 54 321...")
    secuencia_alterna = generar_secuencia(
        cantidad=CANTIDAD_POR_DEFECTO,
        semilla=SEMILLA_ALTERNA,
    )
    ruta_csv_alterna = guardar_secuencia_csv(
        DIRECTORIO_RESULTADOS / "secuencia_python_semilla_54321.csv",
        secuencia_alterna,
    )
    print(f"CSV con semilla alterna guardado en: {ruta_csv_alterna}")

    estadisticas = calcular_estadisticas(secuencia)
    imprimir_estadisticas(estadisticas)

    resultado_periodo = analizar_periodo(secuencia)
    condiciones = verificar_condiciones_periodo_maximo(parametros)
    imprimir_analisis_periodo(resultado_periodo, condiciones)

    print("\nGenerando gráficas...")
    rutas_graficas = generar_todas_las_graficas(
        secuencia,
        secuencia_alterna,
        DIRECTORIO_GRAFICAS,
    )
    for ruta in rutas_graficas:
        print(f"  Gráfica guardada en: {ruta}")

    print("\nProceso de Python finalizado correctamente.")
    print(
        "Ejecute ahora la implementación Java y luego "
        "comparacion/comparar.py para verificar la igualdad de las secuencias."
    )


if __name__ == "__main__":
    main()
