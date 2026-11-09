"""Implementación del Generador Congruencial Lineal (LCG).

La relación recursiva utilizada es:

    X(n+1) = (a * X(n) + c) mod m
    U(n)   = X(n) / m

Donde ``a`` es el multiplicador, ``c`` el incremento, ``m`` el módulo y
``X(0)`` la semilla inicial. Python utiliza enteros de precisión arbitraria,
por lo que la operación módulo reproduce exactamente la aritmética de 32 bits
sin desbordamientos.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


MULTIPLICADOR_POR_DEFECTO = 1_664_525
INCREMENTO_POR_DEFECTO = 1_013_904_223
MODULO_POR_DEFECTO = 2**32
SEMILLA_POR_DEFECTO = 12_345
CANTIDAD_POR_DEFECTO = 10_000


@dataclass(frozen=True)
class ParametrosLCG:
    """Parámetros que definen una instancia del generador congruencial lineal."""

    multiplicador: int = MULTIPLICADOR_POR_DEFECTO
    incremento: int = INCREMENTO_POR_DEFECTO
    modulo: int = MODULO_POR_DEFECTO
    semilla: int = SEMILLA_POR_DEFECTO

    def __post_init__(self) -> None:
        if self.modulo <= 0:
            raise ValueError("El módulo debe ser un entero positivo.")
        if self.multiplicador < 0:
            raise ValueError("El multiplicador no puede ser negativo.")
        if self.incremento < 0:
            raise ValueError("El incremento no puede ser negativo.")
        if not 0 <= self.semilla < self.modulo:
            raise ValueError(
                f"La semilla debe cumplir 0 <= semilla < {self.modulo}."
            )


class GeneradorLCG:
    """Generador de números pseudoaleatorios basado en la fórmula LCG."""

    def __init__(self, parametros: ParametrosLCG | None = None) -> None:
        self.parametros = parametros or ParametrosLCG()
        self._estado = self.parametros.semilla

    @property
    def estado(self) -> int:
        """Valor actual de X(n)."""
        return self._estado

    def reiniciar(self, semilla: int | None = None) -> None:
        """Reinicia el estado interno, opcionalmente con una nueva semilla."""
        nueva_semilla = self.parametros.semilla if semilla is None else semilla
        if not 0 <= nueva_semilla < self.parametros.modulo:
            raise ValueError(
                f"La semilla debe cumplir 0 <= semilla < {self.parametros.modulo}."
            )
        self._estado = nueva_semilla

    def siguiente(self) -> tuple[int, float]:
        """Calcula el siguiente par (X(n+1), U(n+1)) y actualiza el estado."""
        p = self.parametros
        self._estado = (p.multiplicador * self._estado + p.incremento) % p.modulo
        return self._estado, self._estado / p.modulo

    def generar(self, cantidad: int) -> list[tuple[int, float]]:
        """Genera ``cantidad`` pares (X, U) consecutivos."""
        if cantidad < 0:
            raise ValueError("La cantidad de valores no puede ser negativa.")
        return [self.siguiente() for _ in range(cantidad)]

    def __iter__(self) -> Iterator[tuple[int, float]]:
        """Permite recorrer la secuencia de forma infinita."""
        while True:
            yield self.siguiente()


def generar_secuencia(
    cantidad: int = CANTIDAD_POR_DEFECTO,
    semilla: int = SEMILLA_POR_DEFECTO,
    *,
    multiplicador: int = MULTIPLICADOR_POR_DEFECTO,
    incremento: int = INCREMENTO_POR_DEFECTO,
    modulo: int = MODULO_POR_DEFECTO,
) -> list[tuple[int, float]]:
    """Genera una secuencia LCG completa a partir de los parámetros indicados."""
    parametros = ParametrosLCG(
        multiplicador=multiplicador,
        incremento=incremento,
        modulo=modulo,
        semilla=semilla,
    )
    return GeneradorLCG(parametros).generar(cantidad)


if __name__ == "__main__":
    # Comprobación rápida de los primeros valores del generador.
    primeros = generar_secuencia(cantidad=5)
    for iteracion, (x, u) in enumerate(primeros, start=1):
        print(f"{iteracion:5d}  X = {x:>10d}  U = {u:.12f}")
