import matplotlib.pyplot as plt


def graficar_comparacion(resultados):
    """
    Genera una gráfica comparativa de los cuatro modelos.

    Parámetros:
        resultados : diccionario con los resultados
                       de cada modelo.
    """

    plt.figure(figsize=(10, 6))

    for nombre, datos in resultados.items():

        tiempo, poblacion = datos

        plt.plot(
            tiempo,
            poblacion,
            marker="o",
            label=nombre
        )

    plt.title("Comparación de modelos de crecimiento poblacional")
    plt.xlabel("Tiempo")
    plt.ylabel("Población")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.show()