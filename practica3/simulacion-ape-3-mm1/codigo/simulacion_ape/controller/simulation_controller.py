"""Controlador: simula los escenarios, muestra la comparación, guarda gráficas y abre la pantalla en vivo."""

import argparse
from pathlib import Path

from ..model.config import SCENARIOS, AnimationConfig, Scenario, SimulationConfig
from ..model.simulation import run_scenario
from ..model.theory import is_stable
from ..view.console_view import show_comparison, show_message, show_unstable

DEFAULT_OUTPUT = Path(__file__).resolve().parents[2] / "resultados"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m simulacion_ape",
        description="Simulación M/M/1 de una caja rápida de supermercado con SimPy.",
    )
    parser.add_argument("--escenario", type=int, choices=[s.number for s in SCENARIOS], default=1,
                        help="escenario que se abre primero en la pantalla en vivo (por defecto 1)")
    parser.add_argument("--llegada", type=float, help="λ personalizado (clientes/min); requiere --servicio")
    parser.add_argument("--servicio", type=float, help="μ personalizado (clientes/min); requiere --llegada")
    parser.add_argument("--tiempo", type=float, default=SimulationConfig.sim_time,
                        help="minutos simulados para las métricas (por defecto %(default).0f)")
    parser.add_argument("--semilla", type=int, default=SimulationConfig.seed, help="semilla aleatoria")
    parser.add_argument("--duracion", type=float, default=AnimationConfig.duration,
                        help="minutos del sistema que reproduce la pantalla en vivo (por defecto %(default).0f)")
    parser.add_argument("--velocidad", type=float, default=AnimationConfig.minutes_per_second,
                        help="minutos simulados por segundo al abrir la pantalla (por defecto %(default)s)")
    parser.add_argument("--sin-navegador", action="store_true",
                        help="genera resultados/simulacion.html sin abrir el navegador")
    parser.add_argument("--sin-animacion", action="store_true", help="solo tabla y gráficas")
    parser.add_argument("--resultados", type=Path, default=DEFAULT_OUTPUT, help="carpeta de salida")
    args = parser.parse_args(argv)
    if (args.llegada is None) != (args.servicio is None):
        parser.error("--llegada y --servicio se usan juntos")
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    scenarios = SCENARIOS
    start_scenario = args.escenario
    if args.llegada is not None:
        scenarios = (Scenario(0, args.llegada, args.servicio, "Personalizado"),)
        start_scenario = 0
    config = SimulationConfig(sim_time=args.tiempo, seed=args.semilla, scenarios=scenarios)

    results = []
    for scenario in config.scenarios:
        if not is_stable(scenario.arrival_rate, scenario.service_rate):
            show_unstable(scenario.label, scenario.arrival_rate, scenario.service_rate)
            continue
        results.append(run_scenario(scenario, config))
    if not results:
        return
    show_comparison(results)

    # Las vistas gráficas se importan aquí para que matplotlib solo se cargue cuando hay resultados.
    from ..view.chart_view import save_charts
    from ..view.html_view import open_in_browser, save_html

    for path in save_charts(results, args.resultados):
        show_message(f"Gráfica guardada: {path}")
    if args.sin_animacion:
        return
    animation = AnimationConfig(duration=args.duracion, minutes_per_second=args.velocidad)
    page = save_html(results, animation, args.resultados, start_scenario)
    show_message(f"Pantalla en vivo: {page}")
    if not args.sin_navegador and not open_in_browser(page):
        show_message("No se pudo abrir el navegador; abra el archivo anterior manualmente.")
