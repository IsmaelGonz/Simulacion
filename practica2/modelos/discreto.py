def modelo_discreto(p0, r, tiempo):
    """
    Modelo discreto de crecimiento poblacional.

    La población cambia en intervalos de tiempo definidos.

    Parámetros:
        p0     : población inicial
        r      : tasa de crecimiento
        tiempo : número de períodos

    Retorna:
        tiempos   : períodos de la simulación
        poblacion : población calculada en cada período
    """

    tiempos = list(range(tiempo + 1))

    poblacion = [p0]

    for _ in range(1, tiempo + 1):

        poblacion_actual = poblacion[-1]

        incremento = r * poblacion_actual

        nueva_poblacion = poblacion_actual + incremento

        poblacion.append(nueva_poblacion)

    return tiempos, poblacion