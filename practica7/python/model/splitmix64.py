"""Generador pseudoaleatorio SplitMix64 reproducible.

SplitMix64 es un generador determinista de 64 bits. Su estado avanza con la
constante dorada y cada salida se obtiene aplicando dos mezclas multiplicativas
y desplazamientos XOR. La misma implementacion existe en Java, de modo que
ambos lenguajes producen exactamente la misma secuencia de numeros.

La conversion a double usa solo los 53 bits superiores del entero generado:

    U = (salida >> 11) * 2**-53

Esa operacion es exacta en IEEE 754 de doble precision y produce valores en
[0, 1). Gracias a ello, Python y Java obtienen bits identicos.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass

MASK64 = (1 << 64) - 1
GOLDEN_GAMMA = 0x9E3779B97F4A7C15
MIX1 = 0xBF58476D1CE4E5B9
MIX2 = 0x94D049BB133111EB
DEFAULT_SEED = 12345
TWO_POW_MINUS_53 = 1.0 / (1 << 53)


@dataclass
class SplitMix64:
    """Estado y operaciones del generador SplitMix64."""

    seed: int = DEFAULT_SEED

    def __post_init__(self) -> None:
        if not (0 <= self.seed <= MASK64):
            raise ValueError("La semilla debe estar en el rango [0, 2**64 - 1].")
        self.state = self.seed

    def reset(self, seed: int | None = None) -> None:
        if seed is not None:
            if not (0 <= seed <= MASK64):
                raise ValueError("La semilla debe estar en el rango [0, 2**64 - 1].")
            self.seed = seed
        self.state = self.seed

    def next_u64(self) -> int:
        """Devuelve el siguiente entero sin signo de 64 bits mezclado."""
        self.state = (self.state + GOLDEN_GAMMA) & MASK64
        z = self.state
        z = ((z ^ (z >> 30)) * MIX1) & MASK64
        z = ((z ^ (z >> 27)) * MIX2) & MASK64
        return z ^ (z >> 31)

    def next_double(self) -> float:
        """Devuelve un valor pseudoaleatorio uniforme en [0, 1)."""
        return (self.next_u64() >> 11) * TWO_POW_MINUS_53


def double_bits_hex(value: float) -> str:
    """Representacion hexadecimal exacta de los bits IEEE 754 de un double."""
    bits = struct.unpack("<Q", struct.pack("<d", value))[0]
    return f"{bits:016x}"


def verify_sequence(pairs: int = 1000, seed: int = DEFAULT_SEED) -> dict:
    """Genera una muestra de verificacion y su huella SHA-256.

    La huella se calcula sobre los 8 bytes little-endian de cada coordenada
    x e y. Java construye la misma cadena de bytes, por lo que los hashes
    deben coincidir si las secuencias son identicas.
    """
    rng = SplitMix64(seed)
    digest = hashlib.sha256()
    first_pairs: list[tuple[int, float, float]] = []

    for index in range(1, pairs + 1):
        x = rng.next_double()
        y = rng.next_double()
        digest.update(struct.pack("<d", x))
        digest.update(struct.pack("<d", y))
        if index <= 10:
            first_pairs.append((index, x, y))

    return {
        "pares": pairs,
        "sha256": digest.hexdigest(),
        "primeros_pares": first_pairs,
    }
