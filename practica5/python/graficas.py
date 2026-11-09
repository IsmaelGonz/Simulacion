"""Generación de las gráficas del LCG con Matplotlib."""

from __future__ import annotations

from pathlib import Path

import matplotlib

# Backend sin ventana: permite generar archivos PNG en cualquier entorno.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


COLOR_PRINCIPAL = "#1F77B4"
COLOR_SECUNDARIO = "#D62728"
COLOR_ALTERNO = "#2CA02C"


def _preparar_figura(titulo: str, xlabel: str, ylabel: str):
    """Crea una figura con un estilo uniforme para todas las gráficas."""
    figura, eje = plt.subplots(figsize=(11, 6), dpi=150)
    eje.set_title(titulo, fontsize=13, fontweight="bold")
    eje.set_xlabel(xlabel)
    eje.set_ylabel(ylabel)
    eje.grid(True, alpha=0.30)
    return figura, eje


def _guardar(figura, ruta_salida: Path) -> Path:
    """Guarda la figura en disco y libera la memoria asociada."""
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(ruta_salida, dpi=150, bbox_inches="tight")
    plt.close(figura)
    return ruta_salida


def graficar_secuencia_x(
    secuencia: list[tuple[int, float]],
    ruta_salida: Path,
) -> Path:
    """Grafica X(n) frente al número de iteración."""
    iteraciones = list(range(1, len(secuencia) + 1))
    valores_x = [x for x, _ in secuencia]

    figura, eje = _preparar_figura(
        "Secuencia X(n) del generador congruencial lineal",
        "Número de iteración n",
        "X(n)",
    )
    eje.plot(iteraciones, valores_x, color=COLOR_PRINCIPAL, linewidth=0.5)
    eje.set_xlim(1, len(secuencia))
    eje.set_ylim(0, max(valores_x) * 1.05)
    eje.ticklabel_format(axis="y", style="plain")
    return _guardar(figura, ruta_salida)


def graficar_valores_u(
    secuencia: list[tuple[int, float]],
    ruta_salida: Path,
) -> Path:
    """Grafica los valores normalizados U(n) frente a la iteración."""
    iteraciones = list(range(1, len(secuencia) + 1))
    valores_u = [u for _, u in secuencia]

    figura, eje = _preparar_figura(
        "Valores normalizados U(n) del generador LCG",
        "Número de iteración n",
        "U(n)",
    )
    eje.plot(iteraciones, valores_u, color=COLOR_PRINCIPAL, linewidth=0.5)
    eje.axhline(0.5, color=COLOR_SECUNDARIO, linestyle="--", linewidth=1.0,
                label="Valor esperado 0.5")
    eje.set_xlim(1, len(secuencia))
    eje.set_ylim(0, 1)
    eje.legend(loc="upper right")
    return _guardar(figura, ruta_salida)


def graficar_histograma(
    secuencia: list[tuple[int, float]],
    ruta_salida: Path,
    cantidad_bins: int = 50,
) -> Path:
    """Grafica el histograma de U(n) y la densidad uniforme esperada."""
    valores_u = [u for _, u in secuencia]

    figura, eje = _preparar_figura(
        "Histograma de los valores normalizados U(n)",
        "U(n)",
        "Densidad",
    )
    eje.hist(
        valores_u,
        bins=cantidad_bins,
        density=True,
        color=COLOR_PRINCIPAL,
        edgecolor="white",
        linewidth=0.4,
        alpha=0.85,
        label=f"Frecuencia relativa ({cantidad_bins} bins)",
    )
    eje.axhline(
        1.0,
        color=COLOR_SECUNDARIO,
        linestyle="--",
        linewidth=1.2,
        label="Densidad uniforme esperada (1)",
    )
    eje.set_xlim(0, 1)
    eje.legend(loc="upper right")
    return _guardar(figura, ruta_salida)


def graficar_dispersion(
    secuencia: list[tuple[int, float]],
    ruta_salida: Path,
) -> Path:
    """Grafica la dispersión de los pares (U(n), U(n+1))."""
    valores_u = [u for _, u in secuencia]

    figura, eje = _preparar_figura(
        "Dispersión de pares consecutivos (U(n), U(n+1))",
        "U(n)",
        "U(n+1)",
    )
    eje.scatter(
        valores_u[:-1],
        valores_u[1:],
        s=3,
        alpha=0.30,
        color=COLOR_PRINCIPAL,
        edgecolors="none",
    )
    eje.set_xlim(0, 1)
    eje.set_ylim(0, 1)
    eje.set_aspect("equal", adjustable="box")
    return _guardar(figura, ruta_salida)


def graficar_comparacion_semillas(
    secuencia_a: list[tuple[int, float]],
    secuencia_b: list[tuple[int, float]],
    ruta_salida: Path,
    cantidad_visible: int = 100,
) -> Path:
    """Compara las primeras observaciones de dos secuencias con semillas distintas."""
    cantidad = min(cantidad_visible, len(secuencia_a), len(secuencia_b))
    iteraciones = list(range(1, cantidad + 1))

    figura, ejes = plt.subplots(2, 1, figsize=(11, 8), dpi=150, sharex=True)
    figura.suptitle(
        "Efecto del cambio de semilla en la secuencia del LCG",
        fontsize=13,
        fontweight="bold",
    )

    ejes[0].plot(
        iteraciones,
        [x for x, _ in secuencia_a[:cantidad]],
        color=COLOR_PRINCIPAL,
        linewidth=1.0,
        marker="o",
        markersize=2.0,
        label="Semilla 12 345",
    )
    ejes[0].plot(
        iteraciones,
        [x for x, _ in secuencia_b[:cantidad]],
        color=COLOR_SECUNDARIO,
        linewidth=1.0,
        marker="s",
        markersize=1.8,
        label="Semilla 54 321",
    )
    ejes[0].set_ylabel("X(n)")
    ejes[0].set_title("Primeros 100 estados X(n)", fontsize=10)
    ejes[0].grid(True, alpha=0.30)
    ejes[0].legend(loc="upper right")
    ejes[0].ticklabel_format(axis="y", style="plain")

    ejes[1].plot(
        iteraciones,
        [u for _, u in secuencia_a[:cantidad]],
        color=COLOR_PRINCIPAL,
        linewidth=1.0,
        marker="o",
        markersize=2.0,
        label="Semilla 12 345",
    )
    ejes[1].plot(
        iteraciones,
        [u for _, u in secuencia_b[:cantidad]],
        color=COLOR_SECUNDARIO,
        linewidth=1.0,
        marker="s",
        markersize=1.8,
        label="Semilla 54 321",
    )
    ejes[1].set_title("Primeros 100 valores normalizados U(n)", fontsize=10)
    ejes[1].set_xlabel("Número de iteración n")
    ejes[1].set_ylabel("U(n)")
    ejes[1].set_ylim(0, 1)
    ejes[1].grid(True, alpha=0.30)
    ejes[1].legend(loc="upper right")

    return _guardar(figura, ruta_salida)


def generar_todas_las_graficas(
    secuencia: list[tuple[int, float]],
    secuencia_semilla_alterna: list[tuple[int, float]],
    directorio_salida: Path,
) -> list[Path]:
    """Genera y guarda el conjunto completo de gráficas de la práctica."""
    directorio_salida.mkdir(parents=True, exist_ok=True)
    rutas = [
        graficar_secuencia_x(secuencia, directorio_salida / "secuencia_x.png"),
        graficar_valores_u(secuencia, directorio_salida / "valores_u.png"),
        graficar_histograma(secuencia, directorio_salida / "histograma_u.png"),
        graficar_dispersion(secuencia, directorio_salida / "dispersion_u.png"),
        graficar_comparacion_semillas(
            secuencia,
            secuencia_semilla_alterna,
            directorio_salida / "comparacion_semillas.png",
        ),
    ]
    return rutas
