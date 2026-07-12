"""Parameter search for the stellar model.

These routines refine the initially unknown parameters (central temperature,
total radius and total luminosity) by minimizing the total relative error at the
transition layer. They operate on a StellarModel instance, mutating its
parameters in place and leaving it recomputed at the best-fit solution.
"""

import numpy as np


def _select_best_grid_point(matrix_error, matrix_temperature, R_values, L_values):
    """
    Selects the grid cell with the minimum total relative error and returns the
    parameters at that cell.

    All four values must come from the SAME cell (the argmin of the error): in
    particular the central temperature is the one optimized at that cell, not the
    global minimum temperature across the grid.

    Parameters:
    - matrix_error: 2-D array of total relative errors, indexed [R, L].
    - matrix_temperature: 2-D array of optimal central temperatures, indexed [R, L].
    - R_values: Array of total radius values.
    - L_values: Array of total luminosity values.

    Returns:
    - (error, T_central, R_total, L_total) at the minimum-error cell.
    """
    i, j = np.unravel_index(np.argmin(matrix_error, axis=None), matrix_error.shape)
    return matrix_error[i, j], matrix_temperature[i, j], R_values[i], L_values[j]


def optimal_temperature_calculation(model, T_values):
    """
    Computes the central temperature that minimizes the total relative error
    by iterating over a range of central temperatures and calculating the total relative error
    for each central temperature.

    Parameters:
    - model: A StellarModel instance (mutated in place).
    - T_values: An array of central temperatures to iterate over.

    Returns:
    - array_error: An array of total relative errors for each central temperature.
    """
    # We define an array to store the total relative error for each central temperature
    array_error = np.zeros(len(T_values))

    # We iterate over the range of central temperatures
    for i, T_central in enumerate(T_values):
        # We update the central temperature
        model.T_central = T_central
        # We reinitialize the parameters and arrays
        model.initialize_parameters()
        model.initialize_arrays()
        # We compute the total relative error for the current central temperature.
        # A parameter set for which the integration diverges is recorded as an
        # infinite error so the sweep continues instead of aborting.
        try:
            model.complete_model()
            array_error[i] = model.error
        except (RuntimeError, IndexError, FloatingPointError, ZeroDivisionError):
            array_error[i] = np.inf

    best = np.argmin(array_error)
    model.T_central = T_values[best]
    model.error = array_error[best]

    if not np.isfinite(model.error):
        print("No central temperature in the given range produced a converged model.")
        return array_error

    # Now that we have the optimal temperature, we compute the complete model
    model.initialize_parameters()
    model.initialize_arrays()
    model.complete_model()

    # Print the central temperature that minimizes the total relative error
    print("Central Temperature that minimizes the Total Relative Error (K):", model.T_central)

    # Print the minimum total relative error
    print("Minimum Total Relative Error (%):", model.error)

    return array_error


def optimal_grid_calculation(model, R_values, L_values, T_values):
    """
    Computes the total radius and luminosity that minimize the total relative error
    by iterating over a grid of total radius and luminosity values and calculating the total
    relative error for each combination of total radius and luminosity.

    Parameters:
    - model: A StellarModel instance (mutated in place).
    - R_values: An array of total radius values to iterate over.
    - L_values: An array of total luminosity values to iterate over.
    - T_values: An array of central temperatures to use in the calculations.

    Returns:
    - matrix_error: A matrix of total relative errors for each combination of total radius and luminosity.
    """
    matrix_error = np.zeros((len(R_values), len(L_values)))
    matrix_temperature = np.zeros((len(R_values), len(L_values)))

    for i, R_total in enumerate(R_values):
        model.R_total = R_total

        for j, L_total in enumerate(L_values):
            model.L_total = L_total
            optimal_temperature_calculation(model, T_values)
            matrix_error[i, j] = model.error
            matrix_temperature[i, j] = model.T_central

    model.error, model.T_central, model.R_total, model.L_total = _select_best_grid_point(
        matrix_error, matrix_temperature, R_values, L_values
    )

    print("----------------------------------------------------------------------------------")

    # Print the central temperature that minimizes the total relative error
    print("Central Temperature that minimizes the Total Relative Error (K):", model.T_central)

    # Print the total radius that minimizes the total relative error
    print("Total Radius that minimizes the Total Relative Error ($10^{10}$ cm):", model.R_total)

    # Print the total luminosity that minimizes the total relative error
    print("Total Luminosity that minimizes the Total Relative Error ($10^{33}$ erg/s):", model.L_total)

    # Print the minimum total relative error
    print("Minimum Total Relative Error (%):", model.error)

    return matrix_error
