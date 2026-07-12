# Stellar Interior Simulation Project

## 📜 Project Overview

This project focuses on developing a numerical model to simulate the interior of a massive star in the main sequence. Specifically, we study the structure of a star characterized by a convective core and a radiative envelope. Starting with known values of mass and chemical composition, the model integrates the fundamental equations governing plasma behavior to analyze the stellar interior.

The process involves integrating from the star's surface inward and from the core outward, adjusting the boundary between the convective core and radiative envelope to ensure a smooth transition. To achieve this, central temperature, total luminosity, and total radius (initially unknown) are iteratively refined.


### Assumptions

The model relies on the following simplifying assumptions:

- **Massive main-sequence star** with `M > 2 M☉` (the example configuration uses
  `M = 5 × 10^33 g`), so the interior is split into an **adiabatic convective core**
  and a **radiative envelope**, matched at a transition layer.
- **Static, hydrostatic structure**: the star does not evolve in time.
- **Fully ionized ideal gas** as the equation of state, with radiation pressure
  neglected: `ρ = μ P / (k_B N_A T)`, and mean molecular weight
  `μ = 1 / (2X + 0.75Y + 0.5Z)`.
- **Uniform chemical composition** (`X`, `Y`, `Z` constant throughout the star).
- **Nuclear energy generation** from the pp chain and the CNO cycle, with
  temperature-dependent exponents (`ε ∝ ρ T^ν`, piecewise in temperature).
- **Energy transport**: radiative diffusion in the envelope (a Kramers-type
  opacity is folded into the integration constants) and adiabatic convection in
  the core, modelled as a polytrope `P = k T^(5/2)` (index `n = 3/2`, `γ = 5/3`).
- The **convective boundary** is placed where the transport parameter (`n + 1`)
  drops below `2.5`.
- **Scaled CGS units** are used throughout: mass in `10^33 g`, radius in
  `10^10 cm`, luminosity in `10^33 erg/s`, temperature in `10^7 K` and pressure
  in `10^15 dyn/cm²`.


## 💻 Project Structure

```
StellarInteriorSimulation
├── config/                             # Configuration files for the simulation
├── data/                               # Folder containing data files
├── notebook/                           # Jupyter Notebooks for analysis and modeling
├── src/                                # Source code
├── .gitignore                          # Git ignore file
├── main.py                             # Main script for running simulations
├── README.md                           # Project description and documentation
```


## 🔧 Installation and Requirements

The project uses [uv](https://docs.astral.sh/uv/) for dependency management. With uv installed:

```bash
# Install the runtime dependencies (numpy, matplotlib, pandas, pyyaml)
uv sync

# Run the simulation
uv run python main.py
```

To also install the dependencies needed to run the Jupyter notebook:

```bash
uv sync --group notebook
uv run jupyter lab
```

The simulation parameters (chemical composition, initial radius, luminosity and
central temperature) are defined in `config/config.yaml`, the single source of
truth for the configuration.

To run the test suite:

```bash
uv run --group dev pytest
```


## 📊 Results

The three initially unknown parameters (central temperature, total radius and
total luminosity) are refined by **minimizing the total relative error at the
transition layer** — the quadratic sum of the relative differences in
`(r, P, T, L, M)` between the inward (surface → center) and outward
(center → surface) integrations.

For the example configuration (`M = 5 × 10^33 g`, `X = 0.75`, `Y = 0.22`):

- A raw integration with the initial guesses yields a total relative error of
  **≈ 67.8 %**.
- Optimizing the central temperature over `[1.5, 2.5) × 10^7 K` reduces it to
  **16.82 %** at `T_central = 1.95 × 10^7 K`.
- A full grid search over `(R_total, L_total)` (see
  `optimal_grid_calculation` in `src/star_class.py`) reduces the error further.

Once solved, the model provides:

- Radial profiles of pressure, temperature, density, enclosed mass, luminosity
  and energy generation rate.
- The location of the convective-core / radiative-envelope boundary.
- Derived observables (effective temperature, spectral type and position on the
  Hertzsprung–Russell diagram).

The full workflow — optimization, profile plots and HR-diagram classification —
is reproduced in `notebook/model_execution.ipynb`.


## 🧠 Conclusions

Throughout this work, a numerical model of a stellar interior was developed, providing valuable insights into the structure of a star with mass M > 2M☉. The project involved implementing numerical integration of the differential equations governing its behavior.

In particular, the project allowed for a deeper understanding of the mixed integration approach, combining integration from the surface inward and from the core outward, with matching solutions in the transition layer between radiative and convective zones.

We conclude that this simplified model, despite significant assumptions, offers valuable information about stellar structure, energy generation within the star, and even observable parameters such as total luminosity, total radius, and effective temperature. These results made it possible to classify the star's spectral type and position it on a Hertzsprung-Russell diagram alongside similar known stars.


## 🔄 Next Steps

The project lays the groundwork for possible future enhancements to the model, such as:

- Incorporating temporal evolution of the star as hydrogen is consumed.
- Studying chemical composition as a function of distance from the center.
- Considering additional sources of opacity.
- Extending support to model low-mass stars.


## ✍️ Author

Javier Carreira - Lead Developer - [GitHub](https://github.com/SupernovaIa)

This project was developed with gratitude for the foundational work in stellar astrophysics and numerical methods, and for the support of academic and open-source communities.