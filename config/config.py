# config.py
#
# Loads the simulation configuration from config.yaml (the single source of truth)
# and exposes the values as module-level names for backward compatibility.

from pathlib import Path

import yaml

# Resolve config.yaml relative to this file so it works regardless of the CWD.
CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"

with open(CONFIG_PATH, "r") as file:
    _config = yaml.safe_load(file)

# Physical constants
K = _config["physical_constants"]["K"]  # Boltzmann constant in erg/K
Na = _config["physical_constants"]["Na"]  # Avogadro's number, dimensionless

# Numerical parameters
max_err = _config["numerical_parameters"]["max_err"]  # Maximum allowed integration error

# Star model parameters
_star = _config["star_model"]
M_total = _star["M_total"]  # Total mass of the star in 10^33 grams
X = _star["composition"]["X"]  # Fraction of Hydrogen
Y = _star["composition"]["Y"]  # Fraction of Helium
R_total = _star["initial_conditions"]["R_total"]  # Total radius in 10^10 cm
L_total = _star["initial_conditions"]["L_total"]  # Total luminosity in 10^33 erg/s
T_central = _star["initial_conditions"]["T_central"]  # Central temperature in 10^7 K

# Test star parameters
_test = _config["test_star"]
M_test = _test["M_test"]  # Test star total mass
X_test = _test["composition"]["X_test"]  # Fraction of Hydrogen
Y_test = _test["composition"]["Y_test"]  # Fraction of Helium
R_test = _test["initial_conditions"]["R_test"]  # Total radius in 10^10 cm
L_test = _test["initial_conditions"]["L_test"]  # Total luminosity in 10^33 erg/s
T_test = _test["initial_conditions"]["T_test"]  # Central temperature in 10^7 K
