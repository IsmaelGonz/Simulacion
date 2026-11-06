"""Funciones estadisticas compartidas por las pruebas de la practica.

Los valores p se calculan con los mismos algoritmos en Python y Java para que
la comparacion entre lenguajes sea directa:

* Chi-cuadrado: funcion gamma incompleta regularizada Q(a, x), que corresponde
  a la cola superior de la distribucion chi-cuadrado.
* Kolmogorov-Smirnov: distribucion asintotica de Kolmogorov con la correccion
  de Stephens (1970). Para n = 10 000 la aproximacion asintotica es adecuada.
"""

from __future__ import annotations

import math


_EPS = 3.0e-14
_FPMIN = 1.0e-300
_MAX_ITER = 1000


def _gser(a: float, x: float) -> float:
    """Serie para P(a, x) (gamma incompleta regularizada inferior)."""
    if x <= 0.0:
        return 0.0
    ap = a
    total = 1.0 / a
    delta = total
    for _ in range(_MAX_ITER):
        ap += 1.0
        delta *= x / ap
        total += delta
        if abs(delta) < abs(total) * _EPS:
            break
    return total * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gcf(a: float, x: float) -> float:
    """Fraccion continua para Q(a, x) (gamma incompleta regularizada superior)."""
    b = x + 1.0 - a
    c = 1.0 / _FPMIN
    d = 1.0 / b if abs(b) > _FPMIN else 1.0 / _FPMIN
    h = d
    for i in range(1, _MAX_ITER + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = b + an / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < _EPS:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def regularized_gamma_q(a: float, x: float) -> float:
    """Devuelve Q(a, x) = 1 - P(a, x), la cola superior gamma."""
    if a <= 0.0:
        raise ValueError("El parametro a debe ser positivo.")
    if x < 0.0:
        raise ValueError("El parametro x debe ser no negativo.")
    if x == 0.0:
        return 1.0
    if x < a + 1.0:
        return max(0.0, min(1.0, 1.0 - _gser(a, x)))
    return max(0.0, min(1.0, _gcf(a, x)))


def chi_square_survival(statistic: float, degrees_of_freedom: int) -> float:
    """Valor p de cola superior para una distribucion chi-cuadrado."""
    if degrees_of_freedom <= 0:
        raise ValueError("Los grados de libertad deben ser positivos.")
    if statistic <= 0.0:
        return 1.0
    return regularized_gamma_q(degrees_of_freedom / 2.0, statistic / 2.0)


def kolmogorov_smirnov_p_value(d: float, n: int) -> float:
    """Valor p asintotico de una prueba KS de una muestra.

    Se aplica la correccion de Stephens:
        lambda = (sqrt(n) + 0.12 + 0.11 / sqrt(n)) * D
    y luego se evalua la distribucion de Kolmogorov.

    Para lambda pequeno se usa la serie de la CDF (evita cancelacion numerica);
    para lambda grande se usa la serie alternante de la cola superior.
    """
    if n <= 0:
        raise ValueError("El tamano de muestra debe ser positivo.")
    if d <= 0.0:
        return 1.0
    if d >= 1.0:
        return 0.0

    sqrt_n = math.sqrt(n)
    lam = (sqrt_n + 0.12 + 0.11 / sqrt_n) * d
    if lam < 1.0e-12:
        return 1.0

    if lam < 0.82:
        # K(lambda) = sqrt(2*pi)/lambda * sum exp(-(2k-1)^2*pi^2/(8*lambda^2))
        factor = math.sqrt(2.0 * math.pi) / lam
        total = 0.0
        for k in range(1, 200):
            exponent = -((2.0 * k - 1.0) ** 2) * math.pi * math.pi / (8.0 * lam * lam)
            term = factor * math.exp(exponent) if exponent > -745.0 else 0.0
            total += term
            if term < 1.0e-16:
                break
        return max(0.0, min(1.0, 1.0 - total))

    total = 0.0
    for k in range(1, 200):
        term = 2.0 * ((-1.0) ** (k - 1)) * math.exp(-2.0 * k * k * lam * lam)
        total += term
        if abs(term) < 1.0e-16:
            break
    return max(0.0, min(1.0, total))


def decision_text(p_value: float, alpha: float, reject: bool) -> str:
    if reject:
        return f"Se rechaza H0 (p = {p_value:.6g} < alpha = {alpha:g})."
    return f"No se rechaza H0 (p = {p_value:.6g} >= alpha = {alpha:g})."
