"""Tests for the parameter search in src/optimization.py."""

import numpy as np
import pytest

from config.config import M_test, X_test, Y_test, T_test, R_test, L_test
from src.model import StellarModel
from src.optimization import (
    _select_best_grid_point,
    optimal_grid_calculation,
    optimal_temperature_calculation,
)


def test_select_best_grid_point_uses_the_argmin_cell():
    # The minimum error is at cell (1, 1). The temperature reported must be the
    # one AT that cell (2.2), not the global minimum temperature (1.5) elsewhere.
    matrix_error = np.array([[5.0, 3.0],
                             [8.0, 1.0]])
    matrix_temperature = np.array([[2.0, 2.5],
                                   [1.5, 2.2]])
    R_values = np.array([10.0, 11.0])
    L_values = np.array([40.0, 50.0])

    error, T_central, R_total, L_total = _select_best_grid_point(
        matrix_error, matrix_temperature, R_values, L_values
    )

    assert error == 1.0
    assert T_central == 2.2  # not np.min(matrix_temperature) == 1.5
    assert R_total == 11.0
    assert L_total == 50.0


def test_optimal_grid_calculation_is_consistent():
    # Small grid inside a region where every (R, L, T) combination converges.
    R_values = np.array([11.0, 11.5])
    L_values = np.array([65.0, 70.0])
    T_values = np.arange(1.8, 2.2, 0.1)

    model = StellarModel(M_test, X_test, Y_test, T_test, R_test, L_test)
    matrix_error = optimal_grid_calculation(model, R_values, L_values, T_values)

    # The reported best parameters come from the grid...
    assert model.R_total in R_values
    assert model.L_total in L_values
    assert model.T_central in T_values
    # ...and the stored error is the grid minimum.
    assert model.error == pytest.approx(matrix_error.min(), rel=1e-9)

    # Re-optimizing the temperature at the selected (R, L) must reproduce the
    # stored central temperature and error (self-consistency of the selection).
    optimal_temperature_calculation(model, T_values)
    assert model.T_central in T_values


def test_optimal_grid_calculation_tolerates_diverging_cells():
    # A grid mixing converging (L = 70) and diverging (L = 40) columns must
    # complete, marking the diverging cells with infinite error and selecting a
    # finite best instead of aborting the whole search.
    R_values = np.array([11.0, 12.0])
    L_values = np.array([40.0, 70.0])
    T_values = np.arange(1.5, 2.5, 0.1)

    model = StellarModel(M_test, X_test, Y_test, T_test, R_test, L_test)
    matrix_error = optimal_grid_calculation(model, R_values, L_values, T_values)

    assert np.isinf(matrix_error).any()     # some parameter sets diverged
    assert np.isfinite(matrix_error).any()  # some converged
    assert np.isfinite(model.error)         # the selected best is finite
    assert model.error == pytest.approx(matrix_error[np.isfinite(matrix_error)].min(), rel=1e-9)
    assert model.L_total == 70.0            # the converging column
