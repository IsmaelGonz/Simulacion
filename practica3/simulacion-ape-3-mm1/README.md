# APE 3 — Simulación de un sistema de líneas de espera M/M/1 mediante SimPy

Práctica grupal de la asignatura Simulación (Carrera de Computación, Universidad Nacional de Loja).
Docente: Ing. José O. Guamán Q. — Unidad 1: Introducción a la Simulación.

## Integrantes

| Integrante | Responsabilidad |
| --- | --- |
| <Nombre 1> | <parte a cargo> |
| <Nombre 2> | <parte a cargo> |
| <Nombre 3> | <parte a cargo> |

## 1. Enunciado y objetivo

Simular un sistema de líneas de espera M/M/1 utilizando Python y SimPy, analizando el comportamiento de los
clientes, la cola y el servidor.

- Implementar un modelo M/M/1 utilizando la biblioteca SimPy.
- Calcular las principales métricas teóricas del sistema de espera (ρ, L, Lq, W, Wq).
- Comparar los resultados teóricos con los obtenidos mediante la simulación.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| <modelo / agente> | <para qué se usó> |

## 3. Proceso con IA

1. <Título de la iteración 1>
2. <Título de la iteración 2>

## 4. Errores de la IA y correcciones

- <respuesta incorrecta> → <cómo se detectó y corrigió>

## 5. Arquitectura del código

```text
codigo/simulacion_ape/
├── __main__.py                  # Delgado: solo llama al controlador
├── model/
│   ├── config.py                # Parámetros de la simulación (λ, μ, tiempo, semilla)
│   ├── dice.py                  # Entidades y reglas del sistema
│   ├── simulation.py            # Motor de ejecución de corridas
│   └── analysis.py              # Estadísticas de resultados
├── view/
│   └── console_view.py          # Salida de resultados (tablas, gráficas)
└── controller/
    └── simulation_controller.py # Orquesta modelo y vistas
```

<Justificación de la arquitectura elegida.>

## 6. Ejecución

```bash
cd codigo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m simulacion_ape
pytest
```

## 7. Resultados

<Resultados principales y su interpretación. El detalle está en `documento/`.>
