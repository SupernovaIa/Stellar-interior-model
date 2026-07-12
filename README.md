# Stellar Interior Simulation

[![CI](https://github.com/SupernovaIa/Stellar-interior-model/actions/workflows/ci.yml/badge.svg)](https://github.com/SupernovaIa/Stellar-interior-model/actions/workflows/ci.yml)

A numerical model of the interior of a massive main-sequence star (`M > 2 M☉`)
with a **convective core** and a **radiative envelope**. The model integrates the
equations of stellar structure from the surface inward and from the center
outward, matching both solutions at the radiative/convective transition layer,
and refines the central temperature, total radius and total luminosity by
minimizing the matching error.

## Quickstart

The project uses [uv](https://docs.astral.sh/uv/):

```bash
uv sync                    # install runtime dependencies
uv run python main.py      # run the simulation
```

```bash
uv sync --group notebook   # dependencies for the analysis notebook
uv run jupyter lab         # open notebook/model_execution.ipynb

uv run --group dev pytest  # run the test suite
```

Simulation parameters live in [`config/config.yaml`](config/config.yaml), the
single source of truth for the configuration.

## Documentation

Detailed documentation lives in [`docs/`](docs/):

- [Physics](docs/physics.md) — the physical model and the equations it solves.
- [Numerical method](docs/numerical-method.md) — mixed integration, transition
  layer matching and error minimization.
- [Usage](docs/usage.md) — installation, configuration, running and testing.
- [Results](docs/results.md) — optimization, profiles and stellar classification.
- [Code structure](docs/code-structure.md) — a tour of the `StellarModel` class.
- [Roadmap](docs/roadmap.md) — planned extensions and open work.

## Author

Javier Carreira — [GitHub](https://github.com/SupernovaIa)
