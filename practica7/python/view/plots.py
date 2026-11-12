"""Graficos academicos de los resultados Monte Carlo."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model.monte_carlo import SAMPLE_SIZES
from model.splitmix64 import DEFAULT_SEED, SplitMix64

PYTHON_COLOR = "#1f77b4"
JAVA_COLOR = "#d62728"
PI_COLOR = "#2ca02c"
GRID_COLOR = "#d9d9d9"


def _format_n(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def _style_axis(ax: plt.Axes, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, which="both", color=GRID_COLOR, linewidth=0.7, alpha=0.8)
    ax.legend(fontsize=9, frameon=True)
    ax.tick_params(axis="both", labelsize=9)


def _set_sample_ticks(ax: plt.Axes, sample_sizes: list[int]) -> None:
    ax.set_xticks(sample_sizes)
    ax.set_xticklabels([_format_n(n) for n in sample_sizes])


def _plot_estimation(frame: pd.DataFrame, output_path: Path) -> None:
    sample_sizes = frame["n"].astype(int).tolist()
    estimates = frame["pi_estimado"].astype(float).tolist()
    real_pi = math.pi

    fig, ax = plt.subplots(figsize=(9.5, 5.8))
    ax.set_xscale("log")
    ax.plot(
        sample_sizes,
        estimates,
        marker="o",
        markersize=8,
        linewidth=2,
        color=PYTHON_COLOR,
        label="π estimado (Python y Java)",
    )
    ax.axhline(
        real_pi,
        color=PI_COLOR,
        linestyle="--",
        linewidth=1.8,
        label=f"π real = {real_pi:.10f}",
    )

    for n, estimate in zip(sample_sizes, estimates):
        ax.annotate(
            f"{estimate:.8f}",
            (n, estimate),
            textcoords="offset points",
            xytext=(0, 11),
            ha="center",
            fontsize=8.5,
            color="#1a1a1a",
        )

    all_values = np.asarray(estimates + [real_pi], dtype=float)
    span = float(all_values.max() - all_values.min())
    margin = max(span * 0.35, 0.0015)
    ax.set_ylim(float(all_values.min()) - margin, float(all_values.max()) + margin)
    _set_sample_ticks(ax, sample_sizes)
    _style_axis(
        ax,
        "Estimación de π mediante Monte Carlo según el tamaño de muestra",
        "Número de puntos N (escala logarítmica)",
        "Valor de π estimado",
    )
    fig.text(
        0.5,
        0.015,
        "Semilla SplitMix64 = 12345. Las estimaciones de Python y Java son idénticas.",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def _plot_error(frame: pd.DataFrame, output_path: Path) -> None:
    sample_sizes = frame["n"].astype(int).tolist()
    errors = frame["error_absoluto"].astype(float).tolist()

    fig, ax = plt.subplots(figsize=(9.5, 5.8))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.plot(
        sample_sizes,
        errors,
        marker="o",
        markersize=8,
        linewidth=2,
        color=JAVA_COLOR,
        label="Error absoluto (Python y Java)",
    )

    for n, error in zip(sample_sizes, errors):
        ax.annotate(
            f"{error:.3e}",
            (n, error),
            textcoords="offset points",
            xytext=(0, 11),
            ha="center",
            fontsize=8.5,
            color="#1a1a1a",
        )

    _set_sample_ticks(ax, sample_sizes)
    _style_axis(
        ax,
        "Error absoluto de la estimación de π en función de N",
        "Número de puntos N (escala logarítmica)",
        "Error absoluto |π real − π estimado| (escala logarítmica)",
    )
    fig.text(
        0.5,
        0.015,
        "El error no disminuye de forma estrictamente monótona en una sola ejecución.",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def _plot_times(frame: pd.DataFrame, output_path: Path) -> None:
    sample_sizes = frame["n"].astype(int).tolist()
    times_python = frame["tiempo_python_ms"].astype(float).tolist()
    times_java = frame["tiempo_java_ms"].astype(float).tolist()

    fig, ax = plt.subplots(figsize=(9.5, 5.8))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.plot(
        sample_sizes,
        times_python,
        marker="o",
        markersize=8,
        linewidth=2,
        color=PYTHON_COLOR,
        label="Python",
    )
    ax.plot(
        sample_sizes,
        times_java,
        marker="s",
        markersize=7,
        linewidth=2,
        color=JAVA_COLOR,
        label="Java",
    )

    for n, value in zip(sample_sizes, times_python):
        ax.annotate(
            f"{value:.4g} ms",
            (n, value),
            textcoords="offset points",
            xytext=(0, 11),
            ha="center",
            fontsize=8,
            color=PYTHON_COLOR,
        )
    for n, value in zip(sample_sizes, times_java):
        ax.annotate(
            f"{value:.4g} ms",
            (n, value),
            textcoords="offset points",
            xytext=(0, -17),
            ha="center",
            fontsize=8,
            color=JAVA_COLOR,
        )

    _set_sample_ticks(ax, sample_sizes)
    _style_axis(
        ax,
        "Tiempo de ejecución de Python y Java para cada tamaño de muestra",
        "Número de puntos N (escala logarítmica)",
        "Tiempo de ejecución (ms, escala logarítmica)",
    )
    fig.text(
        0.5,
        0.015,
        "Tiempo medido solo sobre el bucle Monte Carlo; mediana de 3 repeticiones.",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def generate_monte_carlo_points_plot(
    output_dir: Path, n: int, seed: int = DEFAULT_SEED
) -> Path:
    """Grafica los puntos (x, y) generados dentro/fuera del cuarto de círculo.

    Los puntos azules cumplen x^2 + y^2 <= 1 (son Nc); los rojos quedan fuera.
    Se genera una gráfica por tamaño de muestra solicitado.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"monte_carlo_puntos_{n}.png"

    rng = SplitMix64(seed)
    xs: list[float] = []
    ys: list[float] = []
    inside_mask: list[bool] = []
    for _ in range(n):
        x = rng.next_double()
        y = rng.next_double()
        xs.append(x)
        ys.append(y)
        inside_mask.append(x * x + y * y <= 1.0)

    inside_x = [x for x, inc in zip(xs, inside_mask) if inc]
    inside_y = [y for y, inc in zip(ys, inside_mask) if inc]
    outside_x = [x for x, inc in zip(xs, inside_mask) if not inc]
    outside_y = [y for y, inc in zip(ys, inside_mask) if not inc]

    fig, ax = plt.subplots(figsize=(7.2, 7.2))
    ax.scatter(
        inside_x,
        inside_y,
        c=PYTHON_COLOR,
        s=4,
        alpha=0.5,
        edgecolors="none",
        label=f"Dentro del círculo (Nc = {len(inside_x):,})",
    )
    ax.scatter(
        outside_x,
        outside_y,
        c=JAVA_COLOR,
        s=4,
        alpha=0.5,
        edgecolors="none",
        label=f"Fuera del círculo ({n - len(inside_x):,})",
    )

    theta = np.linspace(0.0, math.pi / 2, 200)
    ax.plot(
        np.cos(theta),
        np.sin(theta),
        color=PI_COLOR,
        lw=2,
        label="Frontera x² + y² = 1",
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_title(
        f"Puntos Monte Carlo (N = {_format_n(n)}) dentro y fuera del cuarto de círculo",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("y", fontsize=11)
    ax.legend(fontsize=9, frameon=True, loc="upper right")
    ax.grid(True, color=GRID_COLOR, linewidth=0.7, alpha=0.8)

    pi_approx = 4.0 * len(inside_x) / n
    fig.text(
        0.5,
        0.015,
        f"Semilla SplitMix64 = {seed}. π ≈ 4 × {len(inside_x):,} / {n:,} = {pi_approx:.6f}",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return output_path


def generate_plots(frame: pd.DataFrame, output_dir: Path) -> list[Path]:
    """Genera las graficas requeridas y una grafica de puntos Monte Carlo
    por cada tamaño de muestra (1 000, 10 000, 100 000 y 1 000 000)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = [
        output_dir / "estimacion_pi.png",
        output_dir / "error_absoluto.png",
        output_dir / "tiempos_ejecucion.png",
    ]
    _plot_estimation(frame, paths[0])
    _plot_error(frame, paths[1])
    _plot_times(frame, paths[2])
    for n in SAMPLE_SIZES:
        paths.append(generate_monte_carlo_points_plot(output_dir, int(n)))
    return paths
