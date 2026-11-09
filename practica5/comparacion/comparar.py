"""Comparación automática de las secuencias generadas en Python y Java.

También compara las secuencias de Python obtenidas con las semillas 12 345 y
54 321, genera las tablas solicitadas y produce las gráficas de Java a partir
de sus propios archivos CSV.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DIRECTORIO_COMPARACION = Path(__file__).resolve().parent
RAIZ_PROYECTO = DIRECTORIO_COMPARACION.parent
DIRECTORIO_RESULTADOS = DIRECTORIO_COMPARACION / "resultados"

ARCHIVO_PYTHON = RAIZ_PROYECTO / "python" / "resultados" / "secuencia_python.csv"
ARCHIVO_JAVA = RAIZ_PROYECTO / "java" / "resultados" / "secuencia_java.csv"
ARCHIVO_PYTHON_ALTERNO = (
    RAIZ_PROYECTO / "python" / "resultados" / "secuencia_python_semilla_54321.csv"
)
ARCHIVO_JAVA_ALTERNO = (
    RAIZ_PROYECTO / "java" / "resultados" / "secuencia_java_semilla_54321.csv"
)

TOLERANCIA_U = 1e-9
CANTIDAD_TABLA = 20

# Se reutiliza el módulo de gráficas de Python para visualizar los datos de Java.
sys.path.insert(0, str(RAIZ_PROYECTO / "python"))
from graficas import generar_todas_las_graficas  # noqa: E402


@dataclass(frozen=True)
class Registro:
    """Una fila del CSV: iteración, estado X y valor normalizado U."""

    iteracion: int
    x: int
    u: float


def leer_secuencia(ruta: Path) -> list[Registro]:
    """Lee y valida un CSV generado por cualquiera de las dos implementaciones."""
    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe el archivo {ruta}. Ejecute primero el programa correspondiente."
        )

    registros: list[Registro] = []
    with ruta.open("r", newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        try:
            encabezado = next(lector)
        except StopIteration as error:
            raise ValueError(f"El archivo {ruta} está vacío.") from error

        if [campo.strip() for campo in encabezado] != ["iteracion", "X", "U"]:
            raise ValueError(
                f"Encabezado inesperado en {ruta}: {encabezado}. "
                "Se esperaba: iteracion, X, U."
            )

        for numero_fila, fila in enumerate(lector, start=2):
            if not fila or all(not campo.strip() for campo in fila):
                continue
            if len(fila) != 3:
                raise ValueError(f"Fila inválida en {ruta}, línea {numero_fila}.")
            iteracion, x, u = fila
            registros.append(
                Registro(
                    iteracion=int(iteracion),
                    x=int(x),
                    u=float(u),
                )
            )

    if not registros:
        raise ValueError(f"El archivo {ruta} no contiene datos.")

    for posicion, registro in enumerate(registros, start=1):
        if registro.iteracion != posicion:
            raise ValueError(
                f"La iteración {registro.iteracion} no es consecutiva en {ruta}."
            )

    return registros


def comparar_registros(
    secuencia_a: list[Registro],
    secuencia_b: list[Registro],
) -> tuple[list[int], int, float]:
    """Compara dos secuencias y devuelve discrepancias, coincidencias X y error U."""
    if len(secuencia_a) != len(secuencia_b):
        raise ValueError(
            f"Las secuencias tienen distinta longitud: "
            f"{len(secuencia_a)} y {len(secuencia_b)}."
        )

    discrepancias: list[int] = []
    coincidencias_x = 0
    diferencia_maxima_u = 0.0

    for registro_a, registro_b in zip(secuencia_a, secuencia_b):
        if registro_a.iteracion != registro_b.iteracion:
            discrepancias.append(registro_a.iteracion)
            continue

        diferencia_u = abs(registro_a.u - registro_b.u)
        diferencia_maxima_u = max(diferencia_maxima_u, diferencia_u)

        coincide = (
            registro_a.x == registro_b.x and diferencia_u <= TOLERANCIA_U
        )
        if coincide:
            coincidencias_x += 1
        else:
            discrepancias.append(registro_a.iteracion)

    return discrepancias, coincidencias_x, diferencia_maxima_u


def guardar_tabla_cross_language(
    ruta_salida: Path,
    secuencia_python: list[Registro],
    secuencia_java: list[Registro],
) -> Path:
    """Guarda la tabla comparativa de las primeras 20 observaciones."""
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    with ruta_salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        escritor.writerow(
            [
                "iteracion",
                "X_python",
                "X_java",
                "U_python",
                "U_java",
                "verificacion_igualdad",
            ]
        )
        for registro_py, registro_java in zip(
            secuencia_python[:CANTIDAD_TABLA],
            secuencia_java[:CANTIDAD_TABLA],
        ):
            igual = (
                registro_py.x == registro_java.x
                and abs(registro_py.u - registro_java.u) <= TOLERANCIA_U
            )
            escritor.writerow(
                [
                    registro_py.iteracion,
                    registro_py.x,
                    registro_java.x,
                    f"{registro_py.u:.12f}",
                    f"{registro_java.u:.12f}",
                    "SI" if igual else "NO",
                ]
            )
    return ruta_salida


def guardar_tabla_semillas(
    ruta_salida: Path,
    secuencia_12345: list[Registro],
    secuencia_54321: list[Registro],
) -> Path:
    """Guarda la tabla de las primeras 20 observaciones para ambas semillas."""
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    with ruta_salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        escritor.writerow(
            [
                "iteracion",
                "X_semilla_12345",
                "X_semilla_54321",
                "U_semilla_12345",
                "U_semilla_54321",
                "verificacion_igualdad",
            ]
        )
        for registro_a, registro_b in zip(
            secuencia_12345[:CANTIDAD_TABLA],
            secuencia_54321[:CANTIDAD_TABLA],
        ):
            igual = (
                registro_a.x == registro_b.x
                and abs(registro_a.u - registro_b.u) <= TOLERANCIA_U
            )
            escritor.writerow(
                [
                    registro_a.iteracion,
                    registro_a.x,
                    registro_b.x,
                    f"{registro_a.u:.12f}",
                    f"{registro_b.u:.12f}",
                    "SI" if igual else "NO",
                ]
            )
    return ruta_salida


def imprimir_tabla_cross_language(
    secuencia_python: list[Registro],
    secuencia_java: list[Registro],
) -> None:
    """Muestra en consola las primeras 20 observaciones de ambos lenguajes."""
    print("\nPrimeras 20 observaciones (Python vs Java):")
    print(
        f"{'n':>5}  {'X Python':>12}  {'X Java':>12}  "
        f"{'U Python':>14}  {'U Java':>14}  {'¿Iguales?':>9}"
    )
    print("-" * 83)
    for registro_py, registro_java in zip(
        secuencia_python[:CANTIDAD_TABLA],
        secuencia_java[:CANTIDAD_TABLA],
    ):
        igual = (
            registro_py.x == registro_java.x
            and abs(registro_py.u - registro_java.u) <= TOLERANCIA_U
        )
        print(
            f"{registro_py.iteracion:5d}  {registro_py.x:12d}  "
            f"{registro_java.x:12d}  {registro_py.u:14.12f}  "
            f"{registro_java.u:14.12f}  {'SI' if igual else 'NO':>9}"
        )


def main() -> None:
    print("=" * 72)
    print("COMPARACIÓN DE SECUENCIAS LCG")
    print("=" * 72)

    secuencia_python = leer_secuencia(ARCHIVO_PYTHON)
    secuencia_java = leer_secuencia(ARCHIVO_JAVA)

    print(f"Python: {ARCHIVO_PYTHON} ({len(secuencia_python)} valores)")
    print(f"Java  : {ARCHIVO_JAVA} ({len(secuencia_java)} valores)")

    discrepancias, coincidencias, diferencia_maxima = comparar_registros(
        secuencia_python, secuencia_java
    )
    imprimir_tabla_cross_language(secuencia_python, secuencia_java)

    print("\n--- Verificación de las 10 000 observaciones ---")
    print(f"Coincidencias exactas de X : {coincidencias} de {len(secuencia_python)}")
    print(f"Diferencia máxima |U_py-U_java| : {diferencia_maxima:.3e}")
    print(f"Discrepancias : {len(discrepancias)}")

    if discrepancias:
        print(
            "RESULTADO: las secuencias NO coinciden. Iteraciones con diferencia: "
            f"{discrepancias[:20]}"
        )
        sys.exit(1)

    print("RESULTADO: las secuencias de Python y Java son idénticas.")
    ruta_tabla = guardar_tabla_cross_language(
        DIRECTORIO_RESULTADOS / "comparacion_20.csv",
        secuencia_python,
        secuencia_java,
    )
    print(f"Tabla comparativa guardada en: {ruta_tabla}")

    print("\n--- Comparación de semillas (Python) ---")
    secuencia_alterna = leer_secuencia(ARCHIVO_PYTHON_ALTERNO)
    coincidencias_semillas = sum(
        1
        for registro_a, registro_b in zip(secuencia_python, secuencia_alterna)
        if registro_a.x == registro_b.x
    )
    print(f"Coincidencias exactas de X entre semillas: "
          f"{coincidencias_semillas} de {len(secuencia_python)}")
    print("Primeras 20 observaciones con semilla 12 345 vs 54 321:")
    print(
        f"{'n':>5}  {'X 12345':>12}  {'X 54321':>12}  "
        f"{'U 12345':>14}  {'U 54321':>14}  {'¿Iguales?':>9}"
    )
    print("-" * 83)
    for registro_a, registro_b in zip(
        secuencia_python[:CANTIDAD_TABLA],
        secuencia_alterna[:CANTIDAD_TABLA],
    ):
        igual = (
            registro_a.x == registro_b.x
            and abs(registro_a.u - registro_b.u) <= TOLERANCIA_U
        )
        print(
            f"{registro_a.iteracion:5d}  {registro_a.x:12d}  "
            f"{registro_b.x:12d}  {registro_a.u:14.12f}  "
            f"{registro_b.u:14.12f}  {'SI' if igual else 'NO':>9}"
        )

    ruta_tabla_semillas = guardar_tabla_semillas(
        DIRECTORIO_RESULTADOS / "comparacion_semillas_20.csv",
        secuencia_python,
        secuencia_alterna,
    )
    print(f"Tabla de comparación de semillas guardada en: {ruta_tabla_semillas}")

    if ARCHIVO_JAVA_ALTERNO.exists():
        secuencia_java_alterna = leer_secuencia(ARCHIVO_JAVA_ALTERNO)
        discrepancias_altas, coincidencias_altas, diferencia_altas = comparar_registros(
            secuencia_alterna, secuencia_java_alterna
        )
        print("\n--- Verificación de la semilla 54 321 entre Python y Java ---")
        print(f"Coincidencias exactas de X : "
              f"{coincidencias_altas} de {len(secuencia_alterna)}")
        print(f"Diferencia máxima |U_py-U_java| : {diferencia_altas:.3e}")
        if discrepancias_altas:
            print("RESULTADO: las secuencias con semilla 54 321 NO coinciden.")
            sys.exit(1)
        print("RESULTADO: las secuencias con semilla 54 321 son idénticas.")

        print("\nGenerando las gráficas de Java a partir de sus propios CSV...")
        rutas_java = generar_todas_las_graficas(
            [(registro.x, registro.u) for registro in secuencia_java],
            [(registro.x, registro.u) for registro in secuencia_java_alterna],
            RAIZ_PROYECTO / "java" / "graficas",
        )
        for ruta in rutas_java:
            print(f"  Gráfica guardada en: {ruta}")
    else:
        print(
            "\nAviso: no se encontró el CSV de Java para la semilla 54 321; "
            "se omite la verificación cruzada y la generación de gráficas de Java."
        )

    print("\nComparación finalizada correctamente.")


if __name__ == "__main__":
    main()
