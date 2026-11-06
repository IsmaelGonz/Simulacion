"""Prueba Kolmogorov-Smirnov de una muestra contra U(0,1).

Se comparan la funcion de distribucion empirica F_n(x) y la teorica F(x) = x.

D+ = max_i ( i/n - x_(i) )
D- = max_i ( x_(i) - (i-1)/n )
D  = max(D+, D-)
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence

from statistics_utils import decision_text, kolmogorov_smirnov_p_value


def run_ks(values: Sequence[float], alpha: float = 0.05) -> Dict:
    """Ejecuta la prueba KS de una muestra y devuelve los resultados."""
    if not values:
        raise ValueError("La secuencia no puede estar vacia.")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha debe estar entre 0 y 1.")
    for value in values:
        if value < 0.0 or value >= 1.0:
            raise ValueError(f"Valor fuera del intervalo [0,1): {value}")

    n = len(values)
    ordered = sorted(values)
    d_plus = -math.inf
    d_minus = -math.inf
    d_plus_index = 0
    d_minus_index = 0

    for i, value in enumerate(ordered, start=1):
        empirical_after = i / n
        empirical_before = (i - 1) / n
        positive = empirical_after - value
        negative = value - empirical_before
        if positive > d_plus:
            d_plus = positive
            d_plus_index = i
        if negative > d_minus:
            d_minus = negative
            d_minus_index = i

    statistic = max(d_plus, d_minus)
    p_value = kolmogorov_smirnov_p_value(statistic, n)
    reject = p_value < alpha

    interpretation = (
        "La distribucion empirica difiere significativamente de la "
        "distribucion uniforme U(0,1) al nivel de significancia indicado."
        if reject
        else "No hay evidencia estadistica suficiente para afirmar que la "
        "distribucion empirica difiere de la uniforme U(0,1)."
    )

    return {
        "prueba": "Kolmogorov-Smirnov",
        "n": n,
        "d_mas": d_plus,
        "d_menos": d_minus,
        "estadistico_d": statistic,
        "indice_d_mas": d_plus_index,
        "indice_d_menos": d_minus_index,
        "valor_p": p_value,
        "alpha": alpha,
        "rechazar_h0": reject,
        "decision": decision_text(p_value, alpha, reject),
        "interpretacion": interpretation,
    }


def format_ks_report(result: Dict) -> str:
    lines = [
        "PRUEBA KOLMOGOROV-SMIRNOV (una muestra, H0: U(0,1))",
        "-" * 62,
        f"Datos analizados       : {result['n']}",
        f"Estadistico D          : {result['estadistico_d']:.10f}",
        f"Diferencia positiva D+ : {result['d_mas']:.10f}",
        f"Diferencia negativa D- : {result['d_menos']:.10f}",
        f"Nivel de significancia : alpha = {result['alpha']:g}",
        f"Valor p                : {result['valor_p']:.10f}",
        f"Decision               : {result['decision']}",
        f"Interpretacion         : {result['interpretacion']}",
    ]
    return "\n".join(lines)


def empirical_cdf_points(
    ordered_values: Sequence[float],
    max_points: int = 2000,
) -> List[Dict]:
    """Puntos reducidos de la ECDF para graficar sin perder la forma."""
    n = len(ordered_values)
    if n == 0:
        return []
    step = max(1, n // max_points)
    points = []
    for i in range(0, n, step):
        points.append(
            {
                "x": float(ordered_values[i]),
                "empirica_antes": i / n,
                "empirica_despues": (i + 1) / n,
                "teorica": float(ordered_values[i]),
            }
        )
    if points[-1]["x"] != ordered_values[-1]:
        i = n - 1
        points.append(
            {
                "x": float(ordered_values[i]),
                "empirica_antes": i / n,
                "empirica_despues": 1.0,
                "teorica": float(ordered_values[i]),
            }
        )
    return points
