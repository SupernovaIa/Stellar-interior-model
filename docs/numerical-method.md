# Numerical method

This document describes how [`src/model.py`](../src/model.py)
integrates the equations of [physics.md](physics.md) and how it solves for the
unknown parameters.

## 1. Mixed integration

The structure equations are stiff near both boundaries, so the model integrates
from **both ends** and matches in the middle (`complete_model`):

1. **Surface → center** (radiative envelope). Starting just below the surface at
   $r = 0.9\,R_\mathrm{total}$ with step $h = -0.01\,R_\mathrm{initial}$, it seeds
   the first three layers analytically (`three_layers_surface`) and integrates
   inward through the radiative envelope (`radiative_envelope`) until the
   convection criterion $n + 1 < 2.5$ is met.
2. **Center → surface** (convective core). It seeds the first three layers around
   $r = 0$ (`three_layers_core`) and integrates outward through the convective
   core (`convective_core`) up to the transition radius.

The two integrations produce independent estimates of $(r, P, T, L, M)$ at the
transition layer; the goal is to make them agree.

## 2. Difference operators

Integration uses a predictor–corrector scheme built on discrete differences of
the derivatives. For a discretized quantity $f_i$ with step $h$:

$$\Delta_1 f_i = h\,(f_i - f_{i-1}), \qquad \Delta_2 f_i = \Delta_1 f_i - \Delta_1 f_{i-1}.$$

These are `delta_1` and `delta_2`. They appear in the predictor/corrector update
formulas, e.g. for pressure in the envelope

$$P_{i+1}^{\text{est}} = P_i + h\,P'_i + \tfrac{1}{2}\Delta_1 P'_i + \tfrac{5}{12}\Delta_2 P'_i,$$

$$P_{i+1}^{\text{cal}} = P_i + h\,P'_{i+1} - \tfrac{1}{2}\Delta_1 P'_{i+1},$$

where $P' \equiv \mathrm{d}P/\mathrm{d}r$.

## 3. Per-layer convergence loops

Within each layer the calculated values feed back into the derivatives, so each
layer is solved by fixed-point iteration until the relative change falls below
`max_err` (default $10^{-4}$):

- **Radiative envelope** (`radiative_envelope`): a nested loop converges the
  pressure (inner) and then the temperature (outer) of the layer.
- **Convective core** (`convective_core`): a single loop converges the
  temperature; the pressure follows from the polytrope $P = k\,T^{5/2}$.

Each loop is capped at `max_iter` iterations (default $10^4$, in
`config/config.yaml`). If a layer fails to converge within that many iterations
the model raises a `RuntimeError` instead of looping forever.

## 4. Transition layer matching

The transition radius $R_\mathrm{down}$ is found by interpolating the transport
parameter to $n + 1 = 2.5$ (`transition_layer_down`). The state from the
**inward** integration is interpolated at $R_\mathrm{down}$ ("down" values), and
the state from the **outward** integration is interpolated at the same radius
("up" values, `transition_layer_up`).

The mismatch is quantified by the **total relative error**
(`calculate_relative_errors`): for each variable $x \in \{r, P, T, L, M\}$,

$$e_x = \left|\frac{x_\mathrm{up} - x_\mathrm{down}}{x_\mathrm{down}}\right| \times 100,
\qquad
E = \sqrt{\sum_x e_x^2}\ \ [\%].$$

## 5. Solving for the unknowns

$E$ is a function of the three initially unknown parameters
$(T_c, R_\mathrm{total}, L_\mathrm{total})$, which are refined by minimizing it:

- **`optimal_temperature_calculation(T_values)`** sweeps a range of central
  temperatures and keeps the one that minimizes $E$.
- **`optimal_grid_calculation(R_values, L_values, T_values)`** performs a 2-D grid
  search over $(R_\mathrm{total}, L_\mathrm{total})$, optimizing $T_c$ at each grid
  point.

The best-fit model is then recomputed and its full profiles stored.

## 6. Stitching the full profile

After matching, `complete_model` appends the analytic **extra layers**
(`extra_layers`) between the integration start ($0.9\,R_\mathrm{total}$) and the
true surface ($R_\mathrm{total}$) so the stored profile spans the whole star.
`extra_variables_calculation` then fills in derived quantities (density, energy
generation rate) across the full radius array.

> **Note.** After `complete_model` the arrays hold the concatenated state of both
> integrations plus the appended surface layers — they are not a single
> monotonically ordered profile. See [code-structure.md](code-structure.md).
