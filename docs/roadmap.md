# Roadmap

Forward-looking work for the project, grouped by theme and roughly ordered by
value. Nothing here is committed to a schedule — it is a place to capture ideas
so they are not lost.

## Validation *(highest value)*

The current test suite pins the model's **behavior** (regression), not its
physical **correctness**: the golden values were captured from the code itself.

- [ ] Add a validation test against **external reference values** (course notes,
      textbook, or a published model) with a physical tolerance, kept separate
      from the exact regression tests.
- [ ] Benchmark the fitted observables (effective temperature, spectral type)
      against a real star of similar mass and composition.

## Scientific model extensions

- [ ] Incorporate the **temporal evolution** of the star as hydrogen is consumed.
- [ ] Let the **chemical composition vary with radius** instead of being uniform.
- [ ] Add **radiation pressure** to the equation of state.
- [ ] Consider **additional opacity sources** beyond the Kramers-type law.
- [ ] Extend support to **low-mass stars** (fully convective / radiative-core
      regimes).

## Numerical method & performance

- [ ] `optimal_grid_calculation` re-runs the full model for every
      `(R, L, T)` point; profile it and consider caching or a coarse-to-fine
      search.
- [ ] Explore an **adaptive step size** instead of the fixed `h = -0.01 R_initial`.
- [ ] Minor consistency: in `convective_core` the energy rate is evaluated at
      `est_T` while `dL_dr` uses `cal_T`; they agree to `max_err`, but using
      `cal_T` in both would be cleaner.

## Tooling & product

- [ ] **FastAPI backend** exposing the model (single run / temperature sweep),
      with the grid search made asynchronous or bounded. Pairs well with an
      interactive Swagger demo or a minimal frontend.
- [ ] Turn the HR-diagram classification (currently described in the notebook)
      into a reusable function with tests.
- [ ] Add **coverage reporting** and a **linter** (e.g. ruff) to CI.
- [ ] Bump `astral-sh/setup-uv` to `v8` once it publishes a moving major tag
      (today only `v1`–`v7` exist).

## Done

A snapshot of the larger items already completed, for context:

- Packaging with `uv` + `pyproject.toml`; `config.yaml` as the single source of
  truth.
- Modular layout: `model` / `energy` / `optimization` / `plotting`.
- Robustness: iteration caps, clean failure on non-physical states, and a
  parameter search that tolerates diverging points.
- Test suite (regression + profile + unit) and CI across Python 3.11–3.13.
- CLI, detailed `docs/`, and generated figures.
