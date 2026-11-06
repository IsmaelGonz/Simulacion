"""Graficas de la practica con Matplotlib."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_histogram(values: Sequence[float], path: Path, bins: int = 20) -> None:
    data = np.asarray(values, dtype=float)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.hist(data, bins=bins, density=True, color="#3b82f6", edgecolor="white",
            alpha=0.85, label="Frecuencia relativa observada")
    ax.axhline(1.0, color="#dc2626", linewidth=2.0, linestyle="--",
               label="Densidad teorica U(0,1) = 1")
    ax.set_title("Histograma de 10 000 numeros pseudoaleatorios del LCG")
    ax.set_xlabel("Valor pseudoaleatorio U")
    ax.set_ylabel("Densidad")
    ax.set_xlim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right")
    _save(fig, path)


def plot_chi_square(result: Dict, path: Path) -> None:
    labels = result["etiquetas_intervalos"]
    observed = result["frecuencias_observadas"]
    expected = result["frecuencias_esperadas"]
    positions = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(11, 5.8))
    ax.bar(positions - 0.2, observed, width=0.4, color="#2563eb",
           label="Frecuencia observada", alpha=0.9)
    ax.bar(positions + 0.2, expected, width=0.4, color="#f59e0b",
           label="Frecuencia esperada", alpha=0.9)
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_title(
        "Chi-cuadrado: frecuencias observadas vs esperadas\n"
        f"chi2 = {result['estadistico']:.4f}, gl = {result['grados_libertad']}, "
        f"p = {result['valor_p']:.6f}"
    )
    ax.set_xlabel("Intervalo de U(0,1)")
    ax.set_ylabel("Frecuencia (cantidad de numeros)")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper right")
    _save(fig, path)


def plot_ks(values: Sequence[float], result: Dict, path: Path) -> None:
    ordered = np.sort(np.asarray(values, dtype=float))
    n = len(ordered)
    ecdf = np.arange(1, n + 1) / n

    fig, ax = plt.subplots(figsize=(9, 5.8))
    ax.step(ordered, ecdf, where="post", color="#2563eb", linewidth=1.6,
            label="Distribucion empirica F_n(x)")
    grid = np.linspace(0.0, 1.0, 400)
    ax.plot(grid, grid, color="#dc2626", linewidth=1.8, linestyle="--",
            label="Distribucion teorica F(x) = x")
    ax.set_title(
        "Kolmogorov-Smirnov: ECDF vs U(0,1)\n"
        f"D+ = {result['d_mas']:.6f}, D- = {result['d_menos']:.6f}, "
        f"D = {result['estadistico_d']:.6f}, p = {result['valor_p']:.6f}"
    )
    ax.set_xlabel("Valor x")
    ax.set_ylabel("Probabilidad acumulada F(x)")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.02)
    ax.grid(alpha=0.25)
    ax.legend(loc="lower right")
    _save(fig, path)

