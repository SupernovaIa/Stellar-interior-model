"""Visualization and data export helpers for a computed StellarModel.

These functions operate on an already-solved model (they read its profile
arrays) and are kept separate from the solver itself.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_array_error(T_values, array_error):
    """
    Plots the total relative error as a function of the central temperature.

    Parameters:
    - T_values: An array of central temperatures to iterate over.
    - array_error: An array of total relative errors for each central temperature.
    """
    plt.figure()
    plt.plot(T_values, array_error)
    plt.axvline(x=T_values[np.argmin(array_error)], color='r', linestyle='--')
    plt.xlabel('Central Temperature ($10^7$ K)')
    plt.ylabel('Total Relative Error (%)')
    plt.grid()
    plt.legend(['Total Relative Error', 'Minimum Total Relative Error'])
    plt.show()


def plot_matrix_error(matrix_error, R_values, L_values):
    """
    Plots the total relative error as a function of the total radius and luminosity.

    Parameters:
    - matrix_error: A matrix of total relative errors for each combination of total radius and luminosity.
    - R_values: An array of total radius values to iterate over.
    - L_values: An array of total luminosity values to iterate over.
    """
    # Radius in vertical axis, Luminosity in horizontal axis
    plt.figure()
    plt.imshow(matrix_error, extent=[min(L_values), max(L_values), max(R_values), min(R_values)], aspect='auto')
    plt.colorbar(label='Total Relative Error (%)')
    plt.xlabel('Total Luminosity ($10^{33}$ erg/s)')
    plt.ylabel('Total Radius ($10^{10}$ cm)')
    plt.grid(False)
    plt.show()


def plot_normalized_variables(model, variable='all', independent_variable='radius', vertical_line=False):
    """
    Plots the star's properties normalized by their maximum values as a function of the normalized radius.

    Parameters:
    - model: A solved StellarModel instance.
    - variable: The variable to plot ('all', 'Mass', 'Luminosity', 'Temperature', 'Pressure', 'Density', 'Epsilon').
    - independent_variable: 'radius' or 'mass'.
    - vertical_line: Whether to draw the transition layer as a vertical line.
    """
    if independent_variable == 'radius':
        independent_variable = model.R / model.R_total
        dependent_variable = model.M
        label = 'Mass'
        xlabel = "Normalized Radius"

    elif independent_variable == 'mass':
        independent_variable = model.M / model.M[-1]
        dependent_variable = model.R
        label = 'Radius'
        xlabel = "Normalized Mass"

    else:
        print("Invalid independent variable. Please choose 'radius' or 'mass'.")

    if variable == 'all':
        plt.figure()

        if  vertical_line:
            plt.axvline(x=model.R[model.transition_layer_index] / model.R[-1], color='k', linestyle='--', label = 'Transition Layer')
        plt.plot(independent_variable, dependent_variable / dependent_variable[-1], label = label)
        plt.plot(independent_variable, model.L / model.L[-1], label='Luminosity')
        plt.plot(independent_variable, model.T / model.T[0], label='Temperature')
        plt.plot(independent_variable, model.P / model.P[0], label='Pressure')
        plt.plot(independent_variable, model.Rho / model.Rho[0], label='Density')

        plt.xlabel(xlabel)
        plt.ylabel('Normalized Values')
        plt.legend()
        plt.grid()
        plt.show()

    elif variable == 'Mass' or variable == 'Radius':
        plt.figure()
        plt.plot(independent_variable, dependent_variable)
        plt.xlabel(xlabel)
        plt.ylabel('Mass ($10^^{33} g$)')
        plt.grid()
        plt.show()

    elif variable == 'Luminosity':
        plt.figure()
        plt.plot(independent_variable, model.L)
        plt.xlabel(xlabel)
        plt.ylabel('Luminosity ($10^{33} erg/s$)')
        plt.grid()
        plt.show()

    elif variable == 'Temperature':
        plt.figure()
        plt.plot(independent_variable, model.T)
        plt.xlabel(xlabel)
        plt.ylabel('Temperature ($10^7 K$)')
        plt.grid()
        plt.show()

    elif variable == 'Pressure':
        plt.figure()
        plt.plot(independent_variable, model.P)
        plt.xlabel(xlabel)
        plt.ylabel('Pressure ($10^{15} dyne/cm^2$)')
        plt.grid()
        plt.show()

    elif variable == 'Density':
        plt.figure()
        plt.plot(independent_variable, model.Rho)
        plt.xlabel(xlabel)
        plt.ylabel('Density ($g/cm^3$)')
        plt.grid()
        plt.show()

    elif variable == 'Epsilon':
        plt.figure()
        plt.plot(independent_variable, model.epsilon)
        plt.xlabel(xlabel)
        plt.ylabel('Energy Generation Rate ($erg/s/g$)')
        plt.grid()
        plt.show()

    else:
        print("Invalid variable. Please choose 'all', 'Mass', 'Luminosity', 'Temperature', 'Pressure', 'Density', or 'Epsilon'.")


def save_data(model, filename):
    """
    Saves the star's properties to a CSV file.

    Parameters:
    - model: A solved StellarModel instance (with extra variables computed).
    - filename: The name of the file to save the data.
    """
    # Create a DataFrame with the star's properties
    df = pd.DataFrame({
        'Radius': model.R,
        'Pressure': model.P,
        'Temperature': model.T,
        'Luminosity': model.L,
        'Mass': model.M,
        'Density': model.Rho,
        'Energy Generation Rate': model.epsilon,
        'Transport Parameter': model.transport_parameter,
        'Cycle': model.cycle,
    })

    # Resolve the data directory relative to the project root (parent of src/)
    # so the output location does not depend on the current working directory.
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Save the DataFrame to a CSV file
    df.to_csv(data_dir / f"{filename}.csv", index=False)
