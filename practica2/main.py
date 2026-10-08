from config.parametros import (
    P0,
    R,
    SIGMA,
    TIEMPO,
    DT
)

from modelos import (
    modelo_deterministico,
    modelo_discreto,
    modelo_estocastico,
    modelo_continuo
)

from graficos import graficar_comparacion


def ejecutar_simulacion():
    """
    Ejecuta los cuatro modelos de crecimiento poblacional.
    """

    # Modelo determinístico
    resultado_deterministico = modelo_deterministico(
        P0,
        R,
        TIEMPO
    )

    # Modelo discreto
    resultado_discreto = modelo_discreto(
        P0,
        R,
        TIEMPO
    )

    # Modelo estocástico
    resultado_estocastico = modelo_estocastico(
        P0,
        R,
        SIGMA,
        TIEMPO
    )

    # Modelo continuo mediante Euler
    resultado_continuo = modelo_continuo(
        P0,
        R,
        TIEMPO,
        DT
    )

    resultados = {
        "Determinístico": resultado_deterministico,
        "Discreto": resultado_discreto,
        "Estocástico": resultado_estocastico,
        "Continuo - Euler": resultado_continuo
    }

    return resultados


def mostrar_informacion():
    """
    Muestra en consola los parámetros utilizados.
    """

    print("=" * 50)
    print("SIMULACIÓN - CRECIMIENTO POBLACIONAL")
    print("=" * 50)

    print(f"Población inicial (P0): {P0}")
    print(f"Tasa de crecimiento (r): {R}")
    print(f"Nivel de aleatoriedad (sigma): {SIGMA}")
    print(f"Tiempo total: {TIEMPO}")
    print(f"Tamaño del paso (dt): {DT}")

    print("=" * 50)


def main():
    """
    Punto de entrada del programa.
    """

    mostrar_informacion()

    resultados = ejecutar_simulacion()

    print("Ejecutando modelos...")
    print("Modelo determinístico")
    print("Modelo discreto")
    print("Modelo estocástico")
    print("Modelo continuo mediante Euler")

    print("\nGenerando gráfica comparativa...")

    graficar_comparacion(resultados)


if __name__ == "__main__":
    main()