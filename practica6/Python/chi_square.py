"""Prueba de bondad de ajuste Chi-cuadrado para uniformidad en [0, 1).

H0: los numeros siguen una distribucion uniforme U(0,1).
H1: los numeros no siguen una distribucion uniforme U(0,1).
"""

from __future__ import annotations

from typing import Dict, List, Sequence

from statistics_utils import chi_square_survival, decision_text


def _interval_label(index: int, bins: int) -> str:
    lower = index / bins
    upper = (index + 1) / bins
    if index == bins - 1:
        return f"[{lower:.1f}, {upper:.1f}]"
    return f"[{lower:.1f}, {upper:.1f})"


def run_chi_square(
    values: Sequence[float],
    bins: int = 10,
    alpha: float = 0.05,
) -> Dict:
    """Ejecuta la prueba Chi-cuadrado y devuelve todos los resultados."""
    if bins <= 1:
        raise ValueError("El numero de intervalos debe ser mayor que 1.")
    if not values:
        raise ValueError("La secuencia no puede estar vacia.")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha debe estar entre 0 y 1.")

    n = len(values)
    observed = [0] * bins
    for value in values:
        if value < 0.0 or value >= 1.0:
            raise ValueError(f"Valor fuera del intervalo [0,1): {value}")
        index = int(value * bins)
        if index >= bins:
            index = bins - 1
        observed[index] += 1

    expected = [n / bins] * bins
    statistic = sum((obs - exp) ** 2 / exp for obs, exp in zip(observed, expected))
    degrees_of_freedom = bins - 1
    p_value = chi_square_survival(statistic, degrees_of_freedom)
    reject = p_value < alpha

    labels = [_interval_label(i, bins) for i in range(bins)]
    interpretation = (
        "Las frecuencias observadas son incompatibles con una distribucion "
        "uniforme U(0,1) al nivel de significancia indicado."
        if reject
        else "No hay evidencia estadistica suficiente para afirmar que las "
        "frecuencias observadas se apartan de una distribucion uniforme U(0,1)."
    )

    return {
        "prueba": "Chi-cuadrado",
        "n": n,
        "intervalos": bins,
        "amplitud": 1.0 / bins,
        "etiquetas_intervalos": labels,
        "frecuencias_observadas": observed,
        "frecuencias_esperadas": expected,
        "estadistico": statistic,
        "grados_libertad": degrees_of_freedom,
        "alpha": alpha,
        "valor_p": p_value,
        "rechazar_h0": reject,
        "decision": decision_text(p_value, alpha, reject),
        "interpretacion": interpretation,
    }


def format_chi_square_report(result: Dict) -> str:
    """Genera un informe de texto legible de la prueba."""
    lines = [
        "PRUEBA CHI-CUADRADO (bondad de ajuste a U(0,1))",
        "-" * 62,
        f"Datos analizados      : {result['n']}",
        f"Intervalos            : {result['intervalos']} (amplitud {result['amplitud']:.2f})",
        f"Grados de libertad    : {result['grados_libertad']}",
        f"Nivel de significancia: alpha = {result['alpha']:g}",
        f"Estadistico chi2      : {result['estadistico']:.10f}",
        f"Valor p (cola superior): {result['valor_p']:.10f}",
        f"Decision              : {result['decision']}",
        f"Interpretacion        : {result['interpretacion']}",
        "",
        f"{'Intervalo':<16}{'Observado':>12}{'Esperado':>12}{'Diferencia':>14}",
        "-" * 54,
    ]
    for label, obs, exp in zip(
        result["etiquetas_intervalos"],
        result["frecuencias_observadas"],
        result["frecuencias_esperadas"],
    ):
        lines.append(f"{label:<16}{obs:>12}{exp:>12.1f}{obs - exp:>14.1f}")
    lines.append("-" * 54)
    lines.append(
        f"{'Total':<16}{sum(result['frecuencias_observadas']):>12}"
        f"{sum(result['frecuencias_esperadas']):>12.1f}"
    )
    return "\n".join(lines)


def chi_square_rows(result: Dict) -> List[Dict]:
    """Convierte el resultado en filas exportables a CSV."""
    return [
        {
            "intervalo": label,
            "observado": obs,
            "esperado": exp,
            "diferencia": obs - exp,
        }
        for label, obs, exp in zip(
            result["etiquetas_intervalos"],
            result["frecuencias_observadas"],
            result["frecuencias_esperadas"],
        )
    ]
