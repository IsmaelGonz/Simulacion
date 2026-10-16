"""Vista HTML: escribe una página autocontenida que reproduce en vivo los registros de SimPy.

La página muestra la animación de la caja, la tabla teórico vs. simulado y las gráficas en la misma
pantalla. No simula nada: recibe la lista de clientes (llegada, inicio de atención, salida) que generó
el modelo y la reproduce minuto a minuto.
"""

import base64
import json
import webbrowser
from pathlib import Path

from ..model.config import AnimationConfig
from ..model.simulation import ScenarioResult
from ..model.theory import QueueMetrics

ASSETS = Path(__file__).resolve().parent / "assets"
FONT_WEIGHTS = (400, 700, 900)


def _metrics(metrics: QueueMetrics) -> dict[str, float]:
    return {field: round(value, 6) for field, value in vars(metrics).items()}


def _round(value: float | None) -> float | None:
    return None if value is None else round(value, 5)


def build_payload(results: list[ScenarioResult], config: AnimationConfig, start_scenario: int) -> dict:
    """Datos que necesita la página: parámetros, métricas y clientes que llegan dentro de la animación."""
    scenarios = []
    for result in results:
        scenario = result.scenario
        customers = [
            [record.customer_id, _round(record.arrival), _round(record.service_start), _round(record.departure)]
            for record in result.customers
            if record.arrival <= config.duration
        ]
        scenarios.append({
            "number": scenario.number,
            "condition": scenario.condition,
            "label": scenario.label,
            "lambda": scenario.arrival_rate,
            "mu": scenario.service_rate,
            "theory": _metrics(result.theory),
            "longRun": _metrics(result.simulated),
            "longRunMinutes": result.sim_time,
            "customers": customers,
        })
    return {
        "duration": config.duration,
        "minutesPerSecond": config.minutes_per_second,
        "startScenario": start_scenario,
        "scenarios": scenarios,
    }


def _font_faces() -> str:
    faces = []
    for weight in FONT_WEIGHTS:
        data = base64.b64encode((ASSETS / "fonts" / f"overpass-latin-{weight}-normal.woff2").read_bytes()).decode()
        faces.append(
            f'@font-face {{ font-family: "Overpass"; font-weight: {weight}; font-display: block; '
            f'src: url(data:font/woff2;base64,{data}) format("woff2"); }}'
        )
    return "\n".join(faces)


def render_html(payload: dict) -> str:
    template = (ASSETS / "simulacion.html").read_text(encoding="utf-8")
    core = (ASSETS / "core.js").read_text(encoding="utf-8")
    # "</" se escapa para que ningún dato pueda cerrar la etiqueta <script>.
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return (
        template.replace("/*__FONT_FACES__*/", _font_faces())
        .replace("/*__CORE__*/", core)
        .replace("/*__DATA__*/", data)
    )


def save_html(results: list[ScenarioResult], config: AnimationConfig, output_dir: Path, start_scenario: int = 1) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "simulacion.html"
    path.write_text(render_html(build_payload(results, config, start_scenario)), encoding="utf-8")
    return path


def open_in_browser(path: Path) -> bool:
    return webbrowser.open(path.resolve().as_uri())
