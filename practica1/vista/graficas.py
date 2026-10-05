import os
import matplotlib.pyplot as plt


CARPETA_GRAFICAS = "graficas"

os.makedirs(CARPETA_GRAFICAS, exist_ok=True)

def graficar_variables_originales(horas, H, N, Tf):

    plt.figure(figsize=(10, 5))

    plt.plot(
        horas,
        H,
        marker="o",
        label="H (humedad)"
    )

    plt.plot(
        horas,
        N,
        marker="o",
        label="N (nubosidad)"
    )

    plt.plot(
        horas,
        Tf,
        marker="o",
        label="Tf (temperatura)"
    )

    plt.xlabel("Hora")
    plt.ylabel("Valor normalizado (0 a 1)")
    plt.title("Modelo original: variables")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICAS,
            "1_variables_original.png"
        ),
        dpi=300
    )

    plt.show()
    plt.close()


def graficar_indice_original(horas, indice):

    plt.figure(figsize=(10, 5))

    plt.plot(
        horas,
        indice,
        marker="o",
        color="black",
        linewidth=2,
        label="Índice I"
    )

    plt.axhline(
        y=0.40,
        linestyle="--",
        label="Límite 0.40"
    )

    plt.axhline(
        y=0.60,
        linestyle="--",
        label="Límite 0.60"
    )

    plt.axhline(
        y=0.75,
        linestyle="--",
        label="Límite 0.75"
    )

    plt.xlabel("Hora")
    plt.ylabel("Índice I")
    plt.title(
        "Índice de posibilidad de lluvia - Modelo original"
    )

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICAS,
            "2_indice_original.png"
        ),
        dpi=300
    )

    plt.show()
    plt.close()