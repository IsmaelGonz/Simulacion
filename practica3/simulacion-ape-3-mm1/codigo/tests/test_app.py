import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from simulacion_ape.controller.simulation_controller import main
from simulacion_ape.model.analysis import records_until, simulated_metrics
from simulacion_ape.model.config import SCENARIOS, AnimationConfig, SimulationConfig
from simulacion_ape.model.simulation import run_scenario
from simulacion_ape.model.state import state_at
from simulacion_ape.view.html_view import ASSETS, build_payload, render_html

MAIN_FILE = Path(__file__).resolve().parents[1] / "simulacion_ape" / "__main__.py"


def embedded_data(html: str) -> dict:
    return json.loads(re.search(r"const DATA = (.*);\n", html).group(1).replace("<\\/", "</"))


def test_entry_point_runs_when_executed_by_file_path(tmp_path):
    # El botón "Run" del editor ejecuta el archivo por ruta, no con python -m.
    result = subprocess.run(
        [sys.executable, str(MAIN_FILE), "--sin-navegador", "--tiempo", "300", "--resultados", str(tmp_path)],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Escenario 3: Cerca de saturación" in result.stdout
    assert f"Pantalla en vivo: {tmp_path / 'simulacion.html'}" in result.stdout
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "cola_en_el_tiempo.png", "comparacion_teorico_simulado.png",
        "convergencia_espera.png", "histograma_espera.png", "simulacion.html",
    ]


def test_unstable_custom_scenario_is_not_simulated(tmp_path, capsys):
    main(["--llegada", "3.5", "--servicio", "3", "--resultados", str(tmp_path)])
    assert "el sistema no es estable (λ = 3.5 ≥ μ = 3.0)" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_html_is_self_contained_and_carries_simpy_records():
    results = [run_scenario(scenario, SimulationConfig(sim_time=200, seed=4)) for scenario in SCENARIOS]
    html = render_html(build_payload(results, AnimationConfig(duration=20), start_scenario=2))
    assert "/*__" not in html
    assert not re.search(r"""(src|href)=["']https?://""", html)  # sin recursos externos
    data = embedded_data(html)
    assert data["startScenario"] == 2 and data["duration"] == 20
    for scenario, result in zip(data["scenarios"], results):
        expected = [r for r in result.customers if r.arrival <= 20]
        assert [c[0] for c in scenario["customers"]] == [r.customer_id for r in expected]
        assert scenario["customers"][0][1] == pytest.approx(expected[0].arrival, abs=1e-5)
        assert scenario["theory"]["mean_in_queue"] == pytest.approx(result.theory.mean_in_queue)
        assert scenario["longRun"]["mean_wait"] == pytest.approx(result.simulated.mean_wait)


@pytest.mark.skipif(shutil.which("node") is None, reason="se necesita Node.js para ejecutar core.js")
def test_browser_logic_matches_python_model():
    # La página debe mostrar exactamente lo que calcula el modelo Python en cada minuto.
    result = run_scenario(SCENARIOS[2], SimulationConfig(sim_time=120, seed=9))
    payload = build_payload([result], AnimationConfig(duration=60), start_scenario=3)
    times = [0.5, 7.3, 18.0, 33.3, 59.9]
    script = (
        f"const Core = require({json.dumps(str(ASSETS / 'core.js'))});"
        f"const records = {json.dumps(payload['scenarios'][0]['customers'])};"
        f"console.log(JSON.stringify({json.dumps(times)}.map(t => "
        "[Core.stateAt(records, t, 0.8), Core.metricsAt(records, t)])));"
    )
    output = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True).stdout
    for t, (state, metrics) in zip(times, json.loads(output)):
        expected_state = state_at(result.customers, t, exit_window=0.8)
        assert tuple(state["waiting"]) == expected_state.waiting
        assert state["inService"] == expected_state.in_service
        assert tuple(state["leaving"]) == expected_state.leaving
        assert (state["served"], state["arrived"]) == (expected_state.served, expected_state.arrived)
        expected = simulated_metrics(records_until(result.customers, t), t)
        for field, value in vars(expected).items():
            if value != value:  # NaN: aún no hay clientes con ese dato
                assert metrics[field] is None
            else:
                assert metrics[field] == pytest.approx(value, abs=1e-4), (t, field)
