import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from config.config import K, Na, max_err, M_total, X, Y, T_central, R_total, L_total, M_test, X_test, Y_test, T_test, R_test, L_test
from src.star_class import StellarModel


def main():
    # We create an instance of the class StellarModel with the parameters of the star
    star = StellarModel(M_total, X, Y, T_central, R_total, L_total)
    star.complete_model()
    print("Total error: ", star.error)

if __name__ == "__main__":
    main()