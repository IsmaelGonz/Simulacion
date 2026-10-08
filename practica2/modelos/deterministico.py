import numpy as np


def modelo_deterministico(p0, r, tiempo):
    """
    Modelo determinístico de crecimiento poblacional.

    Fórmula:
        P(t) = P0 * e^(r*t)

    Parámetros:
        p0     : población inicial
        r      : tasa de crecimiento
        tiempo : tiempo total de simulación

    Retorna:
        tiempos   : vector de tiempos
        poblacion : población calculada en cada instante
    """

    tiempos = np.arange(0, tiempo + 1)

    poblacion = p0 * np.exp(r * tiempos)

    return tiempos, poblacion