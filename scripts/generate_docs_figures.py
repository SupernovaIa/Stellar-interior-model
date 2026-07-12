"""Regenerate the figures embedded in docs/results.md.

Builds the optimized test-star model and saves the profile and error-curve
figures to docs/images/. Run with:

    uv run python scripts/generate_docs_figures.py
"""

import sys
from pathlib import Path

# Make the project root importable when run as a standalone script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")  # headless: render to files, no display needed
import matplotlib.pyplot as plt
import numpy as np

from config.config import M_test, X_test, Y_test, T_test, R_test, L_test
from src.model import StellarModel
from src.optimization import optimal_temperature_calculation
from src import plotting

IMAGES_DIR = Path(__file__).resolve().parent.parent / "docs" / "images"


def save_current_figure(name):
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(IMAGES_DIR / name, dpi=120, bbox_inches="tight")
    plt.close("all")


def main():
    star = StellarModel(M_test, X_test, Y_test, T_test, R_test, L_test)

    # Error vs central temperature, and select the best-fit model.
    T_values = np.arange(1.5, 2.5, 0.05)
    array_error = optimal_temperature_calculation(star, T_values)
    plotting.plot_array_error(T_values, array_error)
    save_current_figure("error_vs_temperature.png")

    # Normalized interior profiles of the best-fit model.
    star.extra_variables_calculation()
    plotting.plot_normalized_variables(star, "all", vertical_line=True)
    save_current_figure("profiles.png")

    print(f"Figures written to {IMAGES_DIR}")


if __name__ == "__main__":
    main()
