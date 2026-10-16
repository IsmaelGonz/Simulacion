# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Python 3 + SimPy run the simulation (required by the course guide). A view module writes one self-contained
HTML file (inline CSS/JS, no build step, no CDN) that replays the SimPy records in the browser.

## Users

The professor (Ing. José Guamán) and classmates watching the group's oral defense of APE 3 on a classroom
projector, from several meters away. Secondary: the group members presenting it live.

## Product Purpose

Make an M/M/1 queue visible as a real, everyday system: customers arriving at random, waiting in a single
FIFO line and being served one at a time, while the theoretical metrics (ρ, L, Lq, W, Wq) and the
simulated ones converge on the same screen as the animation advances. Success: the audience understands
why the queue explodes when λ approaches μ just by watching scenarios 1 → 3.

## Positioning

Every movement, counter and chart point comes from SimPy's event records (arrival, service start,
departure per customer); the browser never simulates on its own.

## Operating Context

Projected in a lit university classroom during a graded oral defense (rubric: model explanation, demo
quality, visualization). Presenter switches between the guide's three scenarios
(λ = 2.0 / 2.5 / 2.9, μ = 3.0 customers/min) and pauses to explain.

## Capabilities and Constraints

- Real system: a supermarket express checkout ("caja rápida"), single line, one cashier.
- Three guide scenarios plus a custom λ/μ from the CLI; λ ≥ μ is reported as unstable, never simulated.
- UI copy in Spanish (course deliverable).
- Must not resemble the professor's example (dark background with neon accents, "Banda neón").
- Large numbers and minimal text: legible from the back of the room.
- Not a generic dashboard of cards and template charts.

## Evidence on Hand

Simulated records and metrics generated at run time by `python -m simulacion_ape`. No real store data.

## Product Principles

1. The model is the source of truth; the view only replays it.
2. Readable from the back of the room before anything else.
3. The real-world scene carries the explanation; numbers confirm it.
