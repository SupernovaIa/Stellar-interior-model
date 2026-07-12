"""Command-line entry point for the stellar interior model.

Runs the model with parameters taken from config/config.yaml, overridable via
command-line flags, and prints a summary of the solution.
"""

import argparse

import numpy as np

from config.config import M_total, X, Y, T_central, R_total, L_total
from src.model import StellarModel
from src.optimization import optimal_temperature_calculation
from src.plotting import save_data


def build_parser():
    parser = argparse.ArgumentParser(
        description="Compute the interior structure of a massive main-sequence star.",
    )
    parser.add_argument("--mass", type=float, default=M_total,
                        help="Total mass in 1e33 g (default: from config.yaml)")
    parser.add_argument("-X", "--hydrogen", type=float, default=X,
                        help="Hydrogen mass fraction X (default: from config.yaml)")
    parser.add_argument("-Y", "--helium", type=float, default=Y,
                        help="Helium mass fraction Y (default: from config.yaml)")
    parser.add_argument("--radius", type=float, default=R_total,
                        help="Total radius in 1e10 cm (default: from config.yaml)")
    parser.add_argument("--luminosity", type=float, default=L_total,
                        help="Total luminosity in 1e33 erg/s (default: from config.yaml)")
    parser.add_argument("--central-temperature", type=float, default=T_central,
                        help="Central temperature in 1e7 K (default: from config.yaml)")
    parser.add_argument("--optimize-temperature", nargs=3, type=float,
                        metavar=("MIN", "MAX", "STEP"),
                        help="Sweep the central temperature over [MIN, MAX) with the "
                             "given STEP and keep the value that minimizes the error.")
    parser.add_argument("--save", metavar="NAME",
                        help="Save the full profile to data/NAME.csv")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    star = StellarModel(args.mass, args.hydrogen, args.helium,
                        args.central_temperature, args.radius, args.luminosity)

    try:
        if args.optimize_temperature:
            lo, hi, step = args.optimize_temperature
            optimal_temperature_calculation(star, np.arange(lo, hi, step))
        else:
            star.complete_model()
    except RuntimeError as error:
        raise SystemExit(f"The model did not converge for these parameters: {error}")

    if not np.isfinite(star.error):
        raise SystemExit("The model did not converge for any temperature in the given range.")

    star.extra_variables_calculation()

    print(f"Total relative error: {star.error:.4f} %")
    print(f"Central temperature:  {star.T_central:.4f} (1e7 K)")
    print(f"Total radius:         {star.R_total:.4f} (1e10 cm)")
    print(f"Total luminosity:     {star.L_total:.4f} (1e33 erg/s)")

    if args.save:
        save_data(star, args.save)
        print(f"Profile saved to data/{args.save}.csv")


if __name__ == "__main__":
    main()
