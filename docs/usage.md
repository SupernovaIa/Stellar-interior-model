# Usage

## Requirements

The project is managed with [uv](https://docs.astral.sh/uv/) and targets
Python ≥ 3.11. Runtime dependencies are `numpy`, `matplotlib`, `pandas` and
`pyyaml` (declared in [`pyproject.toml`](../pyproject.toml)).

## Installation

```bash
uv sync                    # runtime dependencies only
uv sync --group notebook   # + Jupyter for the analysis notebook
uv sync --group dev        # + pytest for the test suite
```

`uv sync` creates a local `.venv` and resolves the locked dependencies from
`uv.lock`.

## Running the simulation

```bash
uv run python main.py
```

`main.py` builds a `StellarModel` from the parameters in `config/config.yaml`,
computes the model and prints a summary (total relative error and the fitted
central temperature, radius and luminosity).

Any parameter can be overridden from the command line, and the central
temperature can be optimized on the fly:

```bash
# Override individual parameters (defaults come from config.yaml)
uv run python main.py --mass 5.0 -X 0.75 -Y 0.22 --radius 11.5 --luminosity 70

# Sweep the central temperature over [1.5, 2.5) K and keep the best fit
uv run python main.py --optimize-temperature 1.5 2.5 0.05

# Save the full profile to data/my_star.csv
uv run python main.py --save my_star
```

See `uv run python main.py --help` for the full list of options. If the
integration diverges for the given parameters the program exits with a clear
message instead of a traceback.

## Configuration

All parameters live in [`config/config.yaml`](../config/config.yaml), the single
source of truth. `config/config.py` loads that file and exposes every value as a
module-level name, so both `main.py` and the notebook read the same numbers.

```yaml
star_model:
  M_total: 5.0            # total mass in 1e33 g
  composition:
    X: 0.75               # hydrogen fraction
    Y: 0.20               # helium fraction
  initial_conditions:
    R_total: 12           # total radius in 1e10 cm
    L_total: 40           # total luminosity in 1e33 erg/s
    T_central: 1.5        # central temperature in 1e7 K
```

There is a separate `test_star` block used as a known reference case.

> **YAML gotcha.** PyYAML only parses a scalar as a float if the exponent carries
> a sign (`6.022e+23`, `1.0e-4`) — a bare `1e-4` or `6.022e23` is read as a
> **string**. Keep the signed/decimal form when editing numeric constants.

## The notebook

```bash
uv sync --group notebook
uv run jupyter lab   # then open notebook/model_execution.ipynb
```

The notebook imports the model and configuration from the packages directly
(`from config.config import ...`) and walks through building the model,
optimizing the parameters and plotting the profiles.

## Tests

```bash
uv run --group dev pytest
```

The suite ([`tests/test_stellar_model.py`](../tests/test_stellar_model.py))
pins the deterministic output of `complete_model` for the reference
configurations (total error and concrete profile values) so that any accidental
change in the numerics is caught, plus a few physical sanity checks.

## Saving results

`StellarModel.save_data(filename)` writes the full profile to
`data/<filename>.csv`. The `data/` directory is resolved relative to the project
root and created on demand, so it works regardless of the current working
directory.
