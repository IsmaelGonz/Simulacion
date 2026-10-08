import numpy as np


def modelo_estocastico(p0, r, sigma, tiempo):
    """
    Modelo estocástico de crecimiento poblacional.

    Incorpora aleatoriedad mediante una distribución normal.

    Parámetros:
        p0     : población inicial
        r      : tasa de crecimiento
        sigma  : nivel de variabilidad
        tiempo : tiempo total de simulación

    Retorna:
        tiempos   : períodos de la simulación
        poblacion : población calculada en cada período
    """

    tiempos = list(range(tiempo + 1))

    poblacion = [p0]

    for _ in range(1, tiempo + 1):

        poblacion_actual = poblacion[-1]

        ruido = np.random.normal(0, sigma)

        nueva_poblacion = (
            poblacion_actual
            + (r * poblacion_actual)
            + ruido
        )

        if nueva_poblacion < 0:
            nueva_poblacion = 0

        poblacion.append(nueva_poblacion)

    return tiempos, poblacion