---
name: Caja rápida — Simulación M/M/1
description: Live replay of SimPy records, signposted like an airport terminal.
colors:
  ink: "#16171a"
  terminal-wall: "#e4e7ea"
  paper: "#f7f8f9"
  floor: "#d3d8dd"
  signal-yellow: "#ffc20e"
  exit-green: "#00875a"
  alert-red: "#c8102e"
  muted: "#5d636b"
  rule: "#c2c8cf"
  board-cell: "#24262b"
  board-cell-live: "#2e2b1c"
  board-label: "#a3a9b0"
typography:
  display:
    fontFamily: "Overpass, Noto Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "3.4rem"
    fontWeight: 900
    lineHeight: 1
    letterSpacing: "-0.02em"
  counter:
    fontFamily: "Overpass, sans-serif"
    fontSize: "2.9rem"
    fontWeight: 900
    lineHeight: 1
  title:
    fontFamily: "Overpass, sans-serif"
    fontSize: "2rem"
    fontWeight: 900
    lineHeight: 1
  flap:
    fontFamily: "Overpass, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Overpass, sans-serif"
    fontSize: "1.05rem"
    fontWeight: 400
    lineHeight: 1.3
  math-symbol:
    fontFamily: "Cambria Math, STIX Two Math, Noto Serif, Georgia, serif"
    fontSize: "1.7rem"
    fontWeight: 400
rounded:
  sign: "6px"
  cell: "3px"
spacing:
  gutter: "1.2rem"
  panel: "1.3rem"
  edge: "1.6rem"
components:
  gate:
    backgroundColor: "transparent"
    textColor: "#ffffff"
    rounded: "{rounded.sign}"
    padding: "0.55rem 1rem 0.55rem 0.55rem"
  gate-active:
    backgroundColor: "{colors.signal-yellow}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sign}"
  icon-button:
    backgroundColor: "#ffffff"
    textColor: "{colors.ink}"
    rounded: "{rounded.sign}"
    size: "3.2rem"
  icon-button-hover:
    backgroundColor: "{colors.signal-yellow}"
  board:
    backgroundColor: "{colors.ink}"
    textColor: "#ffffff"
    rounded: "{rounded.sign}"
    padding: "1.3rem 1.5rem"
  flap-cell:
    backgroundColor: "{colors.board-cell}"
    textColor: "#ffffff"
    typography: "{typography.flap}"
    rounded: "{rounded.cell}"
  flap-cell-live:
    backgroundColor: "{colors.board-cell-live}"
    textColor: "{colors.signal-yellow}"
    typography: "{typography.flap}"
    rounded: "{rounded.cell}"
  chart-panel:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.sign}"
---

# Design System: Caja rápida — Simulación M/M/1

## Overview

The screen is signposted like an airport terminal. Customers are Aicher-style pictograms. Flat black signage
panels carry the names and numbers, and a departures board holds the results. It is projected in a lit
classroom during an oral defense, so legibility from the back row outranks everything else. The world refuses
two things: the dashboard of identical cards and the dark neon demo. The only dark surfaces are signs and the
board, which sit on a cool terminal-gray wall.

## Colors

Restrained palette: neutrals plus three signal colors, each with exactly one meaning.

### Primary
- **Signal yellow** (`signal-yellow`): what is happening now. The active scenario gate, the live "Simulado ahora" column, the queue counter, the service progress bar, the current-time cursor on the chart, and the "Pase" floor mark.

### Secondary
- **Exit green** (`exit-green`): leaving or free. The Salida sign, customers walking out, the lane lamp when the cashier is free, and the Lq(t) series.

### Tertiary
- **Alert red** (`alert-red`): saturation only. It appears in one banner ("ρ = …: la cola crece") and nowhere else.

### Neutral
- `ink` for signs, pictograms, the board and the L(t) series; `terminal-wall` page ground; `paper` for the scene and chart grounds; `floor` for the floor band; `muted` for axis labels; `rule` for histogram bars.

### Named Rules
- **One meaning per signal color.** Yellow never means warning, and red never decorates.
- **Cool ground, no cream.** The wall stays a cool terminal gray. A warm off-white reads as a default here and was removed.

## Typography

Overpass, an open interpretation of the US highway-sign face, is self-hosted as base64 woff2 in weights 400, 700 and 900. Greek math symbols (ρ, L, Lq, W, Wq) are set in an italic math serif in signal yellow, the only second family.

### Hierarchy
- **Display** (3.4rem/900): the clock.
- **Counter** (2.9rem/900): the four board counters.
- **Title** (2rem/900): the product name on the sign strip.
- **Flap** (1.5rem/700, tabular numerals): metric values on the board.
- **Body** (1.05rem): labels, event log, chart titles at 1.2rem/700.
- The root size is `clamp(13px, 0.84vw, 22px)`, so the whole ramp scales with the projector width.

### Named Rules
- **Numbers big, words few.** A number the audience must read is never below 1.3rem. Explanatory text stays at one line.

## Layout

A 16:9 composition at 1920×1080 and 1366×768:
- A black sign strip on top with the brand, the three scenario gates and the controls.
- Below it, the scene on the left (about 62%) and the board on the right.
- Three equal chart panels across the bottom.
- The gutter is 1.2rem.

Under 820px of height the board goes compact and hides the event log. Under 1500px of width the brand subtitle hides. Under 1100px of width everything stacks.

## Elevation & Depth

Flat. Depth comes from overlap, not shadows: the customer at the counter stands in front of it, and the cashier stands behind it. There are no shadows anywhere.

## Shapes

Signs and panels use a 6px radius and board cells 3px. The pictograms are exact geometry: a circle head, a 30-unit torso stroke and 10–13-unit limbs with round caps. Queue posts are short ink strokes, and the belts are 5-unit lines that run between rows, never through people.

## Components

- **Scenario gate**: a numeral tile (white, or ink on yellow when active) plus the condition and λ μ ρ. `aria-pressed` marks the active one.
- **Icon button**: white square with an authored SVG icon, yellow on hover. It is used for play/pause and restart.
- **Speed group**: a segmented group (0.5, 1, 2, 4 min/s) with inset padding. The selected value is white.
- **Departures board**: clock, lamp, four counters, a metric table (Teórico, Simulado ahora, corrida larga) and an event log that only shows lines that fit completely.
- **Flap cell**: a dark cell. A value change runs a 260ms rotateX "flip". It applies to the counters, the live metrics and the whole-minute clock ticks.
- **Chart panel**: a black title tab with a one-line summary, and a canvas with a single ink baseline, faint gridlines and a legend drawn in the canvas (top-left for series, top-right for histograms).
- **Pictogram customer**: standing pose, or a two-frame stride (170ms) while moving. The id appears in white on the torso. A customer turns green and fades while leaving.

## Do's and Don'ts

- Do drive every moving thing from the SimPy records; the page never invents data.
- Do keep signs flat, black or green, with white type and one yellow tile.
- Do respect `prefers-reduced-motion`: no stride and no flips, and positions jump.
- Don't add cards, gradients, glow, glass or offset shadows.
- Don't use a dark page ground or neon accents; that is the reference this screen must not resemble.
- Don't use the middle dot `·` as a separator in Overpass; it collapses spacing. Use an em space or a comma.
