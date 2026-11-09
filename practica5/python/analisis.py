"""Análisis estadístico y del período para las secuencias del LCG."""

from __future__ import annotations

import math
from dataclasses import dataclass

from generador_lcg import ParametrosLCG


@dataclass(frozen=True)
class EstadisticasBasicas:
    """Resumen descriptivo de los valores normalizados U(n)."""

    cantidad: int
    media: float
    desviacion_estandar: float
    minimo: float
    maximo: float
    mediana: float


@dataclass(frozen=True)
class ResultadoPeriodo:
    """Resultado del análisis de repeticiones observadas en la muestra."""

    cantidad_valores: int
    valores_unicos: int
    hay_repeticion: bool
    iteracion_repeticion: int | None
    iteracion_primera_aparicion: int | None
    periodo_empirico: int | None


@dataclass(frozen=True)
class ResultadoPeriodoMaximo:
    """Condiciones teóricas para que un LCG de módulo 2^k tenga período máximo."""

    modulo_potencia_de_dos: bool
    incremento_impar: bool
    multiplicador_congruente_uno_mod_cuatro: bool
    cumple_condiciones: bool
    periodo_maximo_teorico: int | None


def calcular_estadisticas(secuencia: list[tuple[int, float]]) -> EstadisticasBasicas:
    """Calcula media, desviación estándar, mínimo, máximo y mediana de U(n)."""
    if not secuencia:
        raise ValueError("La secuencia no puede estar vacía.")

    valores_u = [u for _, u in secuencia]
    cantidad = len(valores_u)
    media = sum(valores_u) / cantidad
    varianza = sum((u - media) ** 2 for u in valores_u) / cantidad
    valores_ordenados = sorted(valores_u)
    posicion_media = cantidad // 2

    if cantidad % 2 == 0:
        mediana = (
            valores_ordenados[posicion_media - 1] + valores_ordenados[posicion_media]
        ) / 2
    else:
        mediana = valores_ordenados[posicion_media]

    return EstadisticasBasicas(
        cantidad=cantidad,
        media=media,
        desviacion_estandar=math.sqrt(varianza),
        minimo=min(valores_u),
        maximo=max(valores_u),
        mediana=mediana,
    )


def analizar_periodo(secuencia: list[tuple[int, float]]) -> ResultadoPeriodo:
    """Busca la primera repetición del estado X dentro de la muestra generada.

    Una repetición de X implica que el generador entró en un ciclo. El período
    empírico observado es la distancia entre la primera aparición y la repetición.
    """
    primera_aparicion: dict[int, int] = {}

    for iteracion, (x, _) in enumerate(secuencia, start=1):
        if x in primera_aparicion:
            iteracion_inicial = primera_aparicion[x]
            return ResultadoPeriodo(
                cantidad_valores=len(secuencia),
                valores_unicos=len(primera_aparicion),
                hay_repeticion=True,
                iteracion_repeticion=iteracion,
                iteracion_primera_aparicion=iteracion_inicial,
                periodo_empirico=iteracion - iteracion_inicial,
            )
        primera_aparicion[x] = iteracion

    return ResultadoPeriodo(
        cantidad_valores=len(secuencia),
        valores_unicos=len(primera_aparicion),
        hay_repeticion=False,
        iteracion_repeticion=None,
        iteracion_primera_aparicion=None,
        periodo_empirico=None,
    )


def verificar_condiciones_periodo_maximo(
    parametros: ParametrosLCG,
) -> ResultadoPeriodoMaximo:
    """Verifica las condiciones de Hull-Dobell para módulo m = 2^k.

    Para que un LCG con módulo 2^k alcance el período máximo m se requiere:
      1. m sea potencia de 2.
      2. c sea impar (coprimo con m).
      3. a sea congruente con 1 módulo 4.
    """
    modulo = parametros.modulo
    es_potencia_de_dos = modulo > 0 and (modulo & (modulo - 1)) == 0
    incremento_impar = parametros.incremento % 2 == 1
    multiplicador_congruente = parametros.multiplicador % 4 == 1
    cumple = es_potencia_de_dos and incremento_impar and multiplicador_congruente

    return ResultadoPeriodoMaximo(
        modulo_potencia_de_dos=es_potencia_de_dos,
        incremento_impar=incremento_impar,
        multiplicador_congruente_uno_mod_cuatro=multiplicador_congruente,
        cumple_condiciones=cumple,
        periodo_maximo_teorico=modulo if cumple else None,
    )


def imprimir_estadisticas(estadisticas: EstadisticasBasicas) -> None:
    """Muestra en consola el resumen descriptivo de U(n)."""
    print("\n--- Estadísticas descriptivas de U(n) ---")
    print(f"Cantidad de valores : {estadisticas.cantidad}")
    print(f"Media               : {estadisticas.media:.12f}")
    print(f"Desviación estándar : {estadisticas.desviacion_estandar:.12f}")
    print(f"Mínimo              : {estadisticas.minimo:.12f}")
    print(f"Máximo              : {estadisticas.maximo:.12f}")
    print(f"Mediana             : {estadisticas.mediana:.12f}")
    print("Valores esperados para una distribución uniforme en [0, 1):")
    print("  media ≈ 0.5 y desviación estándar ≈ 0.288675134595.")


def imprimir_analisis_periodo(
    muestra: ResultadoPeriodo,
    condiciones: ResultadoPeriodoMaximo,
) -> None:
    """Muestra en consola el análisis del período y sus condiciones teóricas."""
    print("\n--- Análisis del período ---")
    print(f"Valores generados : {muestra.cantidad_valores}")
    print(f"Estados X únicos  : {muestra.valores_unicos}")

    if muestra.hay_repeticion:
        print(
            "Se encontró una repetición del estado X en la iteración "
            f"{muestra.iteracion_repeticion} (primera aparición en la iteración "
            f"{muestra.iteracion_primera_aparicion})."
        )
        print(f"Período empírico observado: {muestra.periodo_empirico}.")
    else:
        print(
            "No se encontró ninguna repetición de X en la muestra. Esto solo "
            "demuestra que el período es mayor que la cantidad de valores "
            "generados; no demuestra que se haya recorrido el período completo."
        )

    print("\nCondiciones de Hull-Dobell para módulo m = 2^k:")
    print(f"  m es potencia de 2 : {'sí' if condiciones.modulo_potencia_de_dos else 'no'}")
    print(f"  c es impar         : {'sí' if condiciones.incremento_impar else 'no'}")
    print(
        "  a ≡ 1 (mod 4)      : "
        f"{'sí' if condiciones.multiplicador_congruente_uno_mod_cuatro else 'no'}"
    )
    if condiciones.cumple_condiciones:
        print(
            "  Las condiciones se cumplen: el período máximo teórico es "
            f"m = {condiciones.periodo_maximo_teorico:,} estados."
        )
        print(
            "  Con 10 000 valores no es posible comprobar experimentalmente un "
            "período de 4 294 967 296 estados."
        )
    else:
        print("  No se garantiza el período máximo con los parámetros actuales.")
