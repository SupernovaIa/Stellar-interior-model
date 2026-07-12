# Code structure

The solver is split into focused modules under `src/`. `StellarModel`
([`src/model.py`](../src/model.py)) is the numerical integrator; energy
generation, parameter search and visualization live alongside it as independent
modules.

```
Stellar-interior-model
├── config/
│   ├── config.yaml     # parameters — single source of truth
│   └── config.py       # loads the YAML and exposes the values
├── src/
│   ├── model.py        # StellarModel — the integrator (core)
│   ├── energy.py       # nuclear energy generation (pure functions)
│   ├── optimization.py # parameter search over T_c, R, L
│   └── plotting.py     # profile plots and CSV export
├── notebook/
│   └── model_execution.ipynb
├── tests/
│   └── test_stellar_model.py
└── main.py             # entry point
```

## `src/energy.py`

Stateless functions for the energy generation rate, depending only on the local
$(T, P)$ and the composition:

- **`pp_chain(T, P, X, mu)`**, **`CNO_cycle(T, P, X, Z, mu)`** — piecewise rates
  and their luminosity coefficients.
- **`energy_generation_rate(T, P, X, Z, mu)`** — picks the dominant cycle.

## `src/model.py` — the `StellarModel` class

The core coupled solver. State is held as NumPy arrays indexed by layer: `R`,
`P`, `T`, `M`, `L`, their gradients (`dP_dr`, `dT_dr`, `dM_dr`, `dL_dr`), and
per-layer diagnostics (`epsilon`, `nu`, `cycle`, `C_l`, `transport_parameter`).

### Setup

- **`__init__`** — stores the inputs and calls the two initializers below.
- **`initialize_parameters`** — derives $Z$, $\mu$ and the scaled constants
  ($C_m$, $C_p$, $C_{t,\mathrm{rad}}$, $C_{t,\mathrm{conv}}$, $A_1$, $A_2$), and
  builds the radius grid ($r = 0.9\,R_\mathrm{total}$ inward to $0$, step $h$).
- **`initialize_arrays`** — allocates the per-layer arrays.

### Numerical helpers

- **`reversal(state)`** — flips every array so integration can proceed either
  inward (`"surface"`) or outward (`"center"`).
- **`delta_1`, `delta_2`** — the first/second discrete difference operators used
  by the predictor–corrector scheme.

### Integration

- **`three_layers_surface`** — analytic seed for the first three surface layers.
- **`radiative_envelope`** — integrates inward until $n + 1 < 2.5$; returns the
  last radiative layer index and fixes `k_polytrope`.
- **`three_layers_core`** — analytic seed for the first three central layers.
- **`convective_core`** — integrates the polytropic core; used both inward
  (from the surface side) and outward (from the center side).

### Matching and error

- **`transition_layer_down` / `transition_layer_up`** — interpolate the state at
  the transition radius from each side.
- **`calculate_relative_errors`** — the total relative error $E$ between the two
  sides.
- **`complete_model`** — orchestrates the whole pipeline: reversal → surface
  seed → radiative envelope → convective core → transition (down) → reversal →
  center seed → convective core (up) → transition (up) → error → append extra
  layers.

### Post-processing

- **`extra_layers`** — analytic layers between $0.9\,R_\mathrm{total}$ and the
  surface, appended by `complete_model`.
- **`extra_variables_calculation`** — fills density and energy generation across
  the full radius array.

## `src/optimization.py`

Functions that take a `StellarModel`, mutate its parameters in place and leave it
recomputed at the best fit:

- **`optimal_temperature_calculation(model, T_values)`** — 1-D sweep over $T_c$.
- **`optimal_grid_calculation(model, R_values, L_values, T_values)`** — 2-D grid
  over $(R_\mathrm{total}, L_\mathrm{total})$.

## `src/plotting.py`

Visualization and export helpers for a solved model:

- **`plot_normalized_variables(model, ...)`** — normalized profiles.
- **`plot_array_error(...)`, `plot_matrix_error(...)`** — error diagnostics.
- **`save_data(model, filename)`** — writes the full profile to
  `data/<filename>.csv`.

## A note on the stored arrays

After `complete_model`, the arrays hold the concatenation of both integrations
(inward + outward) plus the appended surface layers. They are **not** a single
monotonically ordered profile, so treat them as raw solver state rather than a
clean $r$-sorted table. `extra_variables_calculation` re-derives the density and
energy-generation arrays over the full radius grid for plotting and export.
