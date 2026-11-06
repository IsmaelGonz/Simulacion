"""Generador congruencial lineal (LCG) reproducible.

Formula:
    X(n+1) = (a * X(n) + c) mod m
    U(n+1) = X(n+1) / m

La configuracion por defecto es la utilizada en Python y Java para que ambas
implementaciones produzcan exactamente la misma secuencia.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, List


DEFAULT_SEED = 12345
DEFAULT_A = 1664525
DEFAULT_C = 1013904223
DEFAULT_M = 2**32


@dataclass(frozen=True)
class LcgParameters:
    """Parametros del generador congruencial lineal."""

    seed: int = DEFAULT_SEED
    a: int = DEFAULT_A
    c: int = DEFAULT_C
    m: int = DEFAULT_M

    def validate(self) -> None:
        if self.m <= 1:
            raise ValueError("El modulo m debe ser mayor que 1.")
        if not (0 <= self.seed < self.m):
            raise ValueError("La semilla debe cumplir 0 <= semilla < m.")
        if not (0 < self.a < self.m):
            raise ValueError("El multiplicador debe cumplir 0 < a < m.")
        if not (0 <= self.c < self.m):
            raise ValueError("El incremento debe cumplir 0 <= c < m.")

    def as_dict(self) -> dict:
        return {
            "semilla": self.seed,
            "multiplicador": self.a,
            "incremento": self.c,
            "modulo": self.m,
        }


class Lcg:
    """Implementacion escalar y reproducible del LCG."""

    def __init__(self, parameters: LcgParameters | None = None) -> None:
        self.parameters = parameters or LcgParameters()
        self.parameters.validate()
        self.state = self.parameters.seed

    def reset(self) -> None:
        self.state = self.parameters.seed

    def next_state(self) -> int:
        p = self.parameters
        self.state = (p.a * self.state + p.c) % p.m
        return self.state

    def next_u(self) -> float:
        return self.next_state() / self.parameters.m

    def generate_states(self, n: int) -> List[int]:
        """Genera n estados enteros X(n+1)."""
        if n < 0:
            raise ValueError("La cantidad de numeros debe ser no negativa.")
        p = self.parameters
        state = self.state
        a, c, m = p.a, p.c, p.m
        states = [0] * n
        for i in range(n):
            state = (a * state + c) % m
            states[i] = state
        self.state = state
        return states

    def generate(self, n: int) -> List[float]:
        """Genera n numeros pseudoaleatorios normalizados en [0, 1)."""
        if n < 0:
            raise ValueError("La cantidad de numeros debe ser no negativa.")
        p = self.parameters
        state = self.state
        a, c, m = p.a, p.c, p.m
        inv_m = 1.0 / m
        values = [0.0] * n
        for i in range(n):
            state = (a * state + c) % m
            values[i] = state * inv_m
        self.state = state
        return values

    def generate_iter(self, n: int) -> Iterator[float]:
        if n < 0:
            raise ValueError("La cantidad de numeros debe ser no negativa.")
        p = self.parameters
        state = self.state
        a, c, m = p.a, p.c, p.m
        inv_m = 1.0 / m
        for _ in range(n):
            state = (a * state + c) % m
            yield state * inv_m
        self.state = state

    def copy(self) -> "Lcg":
        return Lcg(self.parameters)


def sample_text(values: List[float], count: int = 10) -> str:
    """Devuelve una muestra legible de los primeros valores."""
    lines = [f"  U({i + 1:>5}) = {value:.12f}" for i, value in enumerate(values[:count])]
    return "\n".join(lines)
