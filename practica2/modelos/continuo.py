import numpy as np


def modelo_continuo(p0, r, tiempo, dt):
    """
    Modelo continuo de crecimiento poblacional
    mediante el método numérico de Euler.

    Parámetros:
        p0     : población inicial
        r      : tasa de crecimiento
        tiempo : tiempo total de simulación
        dt     : tamaño del paso

    Retorna:
        tiempos   : vector de tiempos
        poblacion : población calculada en cada instante
    """

    tiempos = np.arange(0, tiempo + dt, dt)

    poblacion = [p0]

    for _ in range(1, len(tiempos)):

        poblacion_actual = poblacion[-1]

        cambio = r * poblacion_actual

        nueva_poblacion = (
            poblacion_actual
            + dt * cambio
        )

        poblacion.append(nueva_poblacion)

    return tiempos, poblacion