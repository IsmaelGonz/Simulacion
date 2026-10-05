from modelo.modelo import (
    horas,
    humedad,
    nubosidad,
    temperatura,
    calcular_modelo,
    obtener_estado
)

from vista.graficas import (
    graficar_variables_originales,
    graficar_indice_original
)

def mostrar_resultados():

    H, N, Tf, I = calcular_modelo()

    print()
    print("MODELO MATEMÁTICO DE POSIBILIDAD DE LLUVIA")
    print("=" * 100)

    print(
        f"{'Hora':<8}"
        f"{'Hum.':<8}"
        f"{'Nub.':<8}"
        f"{'Temp.':<8}"
        f"{'H':<8}"
        f"{'N':<8}"
        f"{'Tf':<8}"
        f"{'Índice':<10}"
        f"{'Estado'}"
    )

    print("-" * 100)

    for i in range(len(horas)):

        estado = obtener_estado(I[i])

        print(
            f"{horas[i]:<8}"
            f"{humedad[i]:<8}"
            f"{nubosidad[i]:<8}"
            f"{temperatura[i]:<8}"
            f"{H[i]:<8.2f}"
            f"{N[i]:<8.2f}"
            f"{Tf[i]:<8.2f}"
            f"{I[i]:<10.2f}"
            f"{estado}"
        )

    print()
    print("Modelo utilizado:")
    print("I = 0.5H + 0.3N + 0.2Tf")

    print()
    print("Generando gráficas...")

    graficar_variables_originales(
        horas,
        H,
        N,
        Tf
    )

    graficar_indice_original(
        horas,
        I
    )

    print()
    print("Las gráficas fueron guardadas en la carpeta 'graficas'.")

if __name__ == "__main__":
    mostrar_resultados()