"""Experimento Monte Carlo para estimar el valor de pi.

Modelo:

    pi ~= 4 * (Nc / N)

Se generan N puntos (x, y) uniformes en [0, 1) x [0, 1). Un punto pertenece al
cuarto de circulo unitario si x**2 + y**2 <= 1. La proporcion de puntos
interiores multiplicada por 4 aproxima pi.

El bucle principal esta escrito de forma explicita para reducir el costo de
llamadas a funciones durante la medicion de tiempos. Las operaciones son las
mismas que en la implementacion Java, incluida la conversion exacta del entero
de 64 bits a double mediante los 53 bits superiores.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from model.splitmix64 import (
    DEFAULT_SEED,
    GOLDEN_GAMMA,
    MASK64,
    MIX1,
    MIX2,
    TWO_POW_MINUS_53,
)

REAL_PI = math.pi
SAMPLE_SIZES: tuple[int, ...] = (1_000, 10_000, 100_000, 1_000_000)
REPETITIONS = 3
WARMUP_RUNS = 1
VERIFICATION_PAIRS = 1_000


@dataclass(frozen=True)
class ExperimentResult:
    """Resultado de una ejecucion del experimento Monte Carlo."""

    n: int
    n_c: int
    pi_estimate: float
    absolute_error: float
    seed: int = DEFAULT_SEED

    @property
    def pi_real(self) -> float:
        return REAL_PI


def estimate_pi(n: int, seed: int = DEFAULT_SEED) -> ExperimentResult:
    """Estima pi generando n puntos con SplitMix64.

    Solo se cronometra esta funcion: no incluye lectura/escritura de archivos,
    impresion en consola ni generacion de graficos.
    """
    if n <= 0:
        raise ValueError("El numero de puntos debe ser positivo.")
    if not (0 <= seed <= MASK64):
        raise ValueError("La semilla debe estar en el rango [0, 2**64 - 1].")

    state = seed
    gamma = GOLDEN_GAMMA
    mix1 = MIX1
    mix2 = MIX2
    mask = MASK64
    scale = TWO_POW_MINUS_53
    inside = 0

    for _ in range(n):
        state = (state + gamma) & mask
        z = state
        z = ((z ^ (z >> 30)) * mix1) & mask
        z = ((z ^ (z >> 27)) * mix2) & mask
        z ^= z >> 31
        x = (z >> 11) * scale

        state = (state + gamma) & mask
        z = state
        z = ((z ^ (z >> 30)) * mix1) & mask
        z = ((z ^ (z >> 27)) * mix2) & mask
        z ^= z >> 31
        y = (z >> 11) * scale

        if x * x + y * y <= 1.0:
            inside += 1

    pi_estimate = 4.0 * inside / n
    return ExperimentResult(
        n=n,
        n_c=inside,
        pi_estimate=pi_estimate,
        absolute_error=abs(REAL_PI - pi_estimate),
        seed=seed,
    )
