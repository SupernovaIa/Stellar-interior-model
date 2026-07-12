# Code structure

The project is small and centered on a single class,
`StellarModel`, in [`src/star_class.py`](../src/star_class.py).

```
Stellar-interior-model
├── config/
│   ├── config.yaml   # parameters — single source of truth
│   └── config.py     # loads the YAML and exposes the values
├── src/
│   └── star_class.py # the StellarModel class
├── notebook/
│   └── model_execution.ipynb
├── tests/
│   └── test_stellar_model.py
└── main.py           # entry point
```

## The `StellarModel` class

State is held as NumPy arrays indexed by layer: `R`, `P`, `T`, `M`, `L`, their
gradients (`dP_dr`, `dT_dr`, `dM_dr`, `dL_dr`), and per-layer diagnostics
(`epsilon`, `nu`, `cycle`, `C_l`, `transport_parameter`).

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

### Energy generation

- **`pp_chain`, `CNO_cycle`** — piecewise energy generation rates and their
  coefficients.
- **`energy_generation_rate`** — picks the dominant cycle at a given $(T, P)$.

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

### Optimization

- **`optimal_temperature_calculation`** — 1-D sweep over $T_c$.
- **`optimal_grid_calculation`** — 2-D grid over $(R_\mathrm{total}, L_\mathrm{total})$.

### Post-processing

- **`extra_layers`** — analytic layers between $0.9\,R_\mathrm{total}$ and the
  surface, appended by `complete_model`.
- **`extra_variables_calculation`** — fills density and energy generation across
  the full radius array.
- **`plot_normalized_variables`, `plot_array_error`, `plot_matrix_error`** —
  plotting helpers.
- **`save_data`** — writes the full profile to `data/<filename>.csv`.

## A note on the stored arrays

After `complete_model`, the arrays hold the concatenation of both integrations
(inward + outward) plus the appended surface layers. They are **not** a single
monotonically ordered profile, so treat them as raw solver state rather than a
clean $r$-sorted table. `extra_variables_calculation` re-derives the density and
energy-generation arrays over the full radius grid for plotting and export.
