import numpy as np

horas = np.array([
    "06:00",
    "08:00",
    "10:00",
    "12:00",
    "14:00",
    "16:00",
    "18:00",
    "20:00",
    "22:00"
])

humedad = np.array([
    65,
    70,
    68,
    60,
    75,
    85,
    92,
    88,
    80
])

nubosidad = np.array([
    40,
    50,
    45,
    30,
    70,
    85,
    95,
    90,
    75
])

temperatura = np.array([
    14,
    16,
    18,
    22,
    20,
    18,
    16,
    17,
    15
])


def obtener_factor_temperatura(temp):

    factores = {
        10: 1.00,
        12: 0.90,
        14: 0.80,
        16: 0.70,
        18: 0.60,
        20: 0.50,
        22: 0.40,
        24: 0.30,
        26: 0.20,
        28: 0.10
    }

    if temp <= 10:
        return 1.00

    if temp >= 28:
        return 0.10

    if temp in factores:
        return factores[temp]


    temperaturas = sorted(factores.keys())

    for i in range(len(temperaturas) - 1):

        t1 = temperaturas[i]
        t2 = temperaturas[i + 1]

        if t1 < temp < t2:

            f1 = factores[t1]
            f2 = factores[t2]

            factor = f1 + (temp - t1) * (f2 - f1) / (t2 - t1)

            return factor


def calcular_modelo():

    
    H = humedad / 100

    N = nubosidad / 100

    Tf = np.array([
        obtener_factor_temperatura(t)
        for t in temperatura
    ])

    I = (
        0.5 * H
        + 0.3 * N
        + 0.2 * Tf
    )

    return H, N, Tf, I


def obtener_estado(indice):

    if indice < 0.40:
        return "SIN LLUVIA"

    elif indice < 0.60:
        return "BAJA POSIBILIDAD"

    elif indice < 0.75:
        return "LLUVIA PROBABLE"

    else:
        return "LLUVIA"