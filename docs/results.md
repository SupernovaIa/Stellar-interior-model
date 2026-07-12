# Results

The three initially unknown parameters — central temperature $T_c$, total radius
$R_\mathrm{total}$ and total luminosity $L_\mathrm{total}$ — are refined by
minimizing the total relative error $E$ at the transition layer (see
[numerical-method.md](numerical-method.md)).

## Optimization

For the reference configuration ($M = 5\times10^{33}\ \mathrm{g}$, $X = 0.75$,
$Y = 0.22$):

| Step | Total relative error $E$ |
|------|--------------------------|
| Raw integration with the initial guesses | $\approx 67.8\ \%$ |
| Optimizing $T_c$ over $[1.5, 2.5)\times10^7\ \mathrm{K}$ | $16.82\ \%$ at $T_c = 1.95\times10^7\ \mathrm{K}$ |
| Full grid search over $(R_\mathrm{total}, L_\mathrm{total})$ | reduced further |

Reproduce the temperature optimization with:

```python
import numpy as np
from config.config import M_test, X_test, Y_test, T_test, R_test, L_test
from src.model import StellarModel

star = StellarModel(M_test, X_test, Y_test, T_test, R_test, L_test)
star.optimal_temperature_calculation(np.arange(1.5, 2.5, 0.05))
# -> minimum error 16.82 % at T_central = 1.95
```

## Outputs

Once solved, the model provides:

- **Radial profiles** of pressure, temperature, density, enclosed mass,
  luminosity and energy generation rate (`plot_normalized_variables`).
- The **location of the convective-core / radiative-envelope boundary**
  (`transition_layer_index`).
- **Derived observables** — effective temperature, spectral type and position on
  the Hertzsprung–Russell diagram.

## Reproducing the full analysis

The complete workflow — parameter optimization, profile plots and HR-diagram
classification — is in
[`notebook/model_execution.ipynb`](../notebook/model_execution.ipynb).

Visualization helpers on `StellarModel`:

- `plot_normalized_variables(...)` — normalized profiles vs radius or mass.
- `plot_array_error(...)` — error vs central temperature.
- `plot_matrix_error(...)` — error heat-map over the $(R, L)$ grid.

## Conclusions

This simplified model, despite its assumptions, yields useful insight into the
structure of a star with $M > 2\,M_\odot$: the run of pressure, temperature and
density through the interior, where and how energy is generated, and the mixed
inward/outward integration matched across the radiative/convective boundary.
From the best-fit solution one can recover observable parameters — total
luminosity, total radius and effective temperature — and thus classify the
star's spectral type and place it on the Hertzsprung–Russell diagram.

## Next steps

Possible extensions of the model:

- Incorporate the temporal evolution of the star as hydrogen is consumed.
- Let the chemical composition vary with distance from the center.
- Consider additional sources of opacity.
- Extend support to low-mass stars.
