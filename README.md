# Stellar Interior Simulation Project

## 📜 Project Overview

This project focuses on developing a numerical model to simulate the interior of a massive star in the main sequence. Specifically, we study the structure of a star characterized by a convective core and a radiative envelope. Starting with known values of mass and chemical composition, the model integrates the fundamental equations governing plasma behavior to analyze the stellar interior.

The process involves integrating from the star's surface inward and from the core outward, adjusting the boundary between the convective core and radiative envelope to ensure a smooth transition. To achieve this, central temperature, total luminosity, and total radius (initially unknown) are iteratively refined.


### Assumptions

WIP


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

WIP


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