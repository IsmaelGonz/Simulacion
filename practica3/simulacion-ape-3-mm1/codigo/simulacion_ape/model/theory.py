"""Métricas teóricas del modelo M/M/1."""

from dataclasses import dataclass


class UnstableSystemError(ValueError):
    """λ ≥ μ: la cola crece sin límite y no existen valores de estado estable."""


@dataclass(frozen=True)
class QueueMetrics:
    utilization: float  # ρ
    mean_in_system: float  # L
    mean_in_queue: float  # Lq
    mean_time_in_system: float  # W
    mean_wait: float  # Wq


def is_stable(arrival_rate: float, service_rate: float) -> bool:
    return arrival_rate < service_rate


def theoretical_metrics(arrival_rate: float, service_rate: float) -> QueueMetrics:
    lam, mu = arrival_rate, service_rate
    if not is_stable(lam, mu):
        raise UnstableSystemError(f"El sistema no es estable: λ = {lam} ≥ μ = {mu}")
    return QueueMetrics(
        utilization=lam / mu,
        mean_in_system=lam / (mu - lam),
        mean_in_queue=lam**2 / (mu * (mu - lam)),
        mean_time_in_system=1 / (mu - lam),
        mean_wait=lam / (mu * (mu - lam)),
    )
