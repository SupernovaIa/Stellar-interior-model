"""Nuclear energy generation.

Pure functions for the pp chain and the CNO cycle energy generation rates.
They depend only on the local temperature and pressure and the star's
composition, so they carry no state.
"""

from config.config import K, Na


def pp_chain(T, P, X, mu):
    """
    Computes the energy generation rate for the pp chain and the associated parameters.

    Parameters:
    - T: Temperature (in units of 10^7 K).
    - P: Pressure (in CGS units).
    - X: Hydrogen mass fraction.
    - mu: Mean molecular weight.

    Returns:
    - epsilon_pp: Energy generation rate for the pp chain.
    - nu_pp: Exponent for the temperature dependence of the pp chain.
    - cycle: Type of nuclear cycle (pp chain).
    - C_l_pp: Coefficient for the energy generation rate.
    """
    if T < 0.4:
        return 0, 0, "NA", 0
    elif T < 0.6:
        nu_pp = 6
        epsilon_pp_1 = 10**(-6.84)
    elif T < 0.95:
        nu_pp = 5
        epsilon_pp_1 = 10**(-6.04)
    elif T < 1.2:
        nu_pp = 4.5
        epsilon_pp_1 = 10**(-5.56)
    elif T < 1.65:
        nu_pp = 4
        epsilon_pp_1 = 10**(-5.02)
    elif T < 2.4:
        nu_pp = 3.5
        epsilon_pp_1 = 10**(-4.40)
    else:
        nu_pp = 1
        epsilon_pp_1 = 0

    Rho = mu * P / (K * Na * T)
    epsilon_pp = epsilon_pp_1 * X * X * Rho * (T * 10)**nu_pp
    cycle = 'pp'
    C_l_pp = 0.01845 * epsilon_pp_1 * X * X * (10 ** nu_pp) * (mu ** 2)

    return epsilon_pp, nu_pp, cycle, C_l_pp


def CNO_cycle(T, P, X, Z, mu):
    """
    Computes the energy generation rate for the CNO cycle and the associated parameters.

    Parameters:
    - T: Temperature (in units of 10^7 K).
    - P: Pressure (in CGS units).
    - X: Hydrogen mass fraction.
    - Z: Metal mass fraction.
    - mu: Mean molecular weight.

    Returns:
    - epsilon_CNO: Energy generation rate for the CNO cycle.
    - nu_CNO: Exponent for the temperature dependence of the CNO cycle.
    - cycle: Type of nuclear cycle (CNO cycle).
    - C_l_CNO: Coefficient for the energy generation rate.
    """
    if T < 1.2:
        nu_CNO = 0
        epsilon_CNO_1 = 0
    elif T < 1.6:
        nu_CNO = 20
        epsilon_CNO_1 = 10**(-22.2)
    elif T < 2.25:
        nu_CNO = 18
        epsilon_CNO_1 = 10**(-19.8)
    elif T < 2.75:
        nu_CNO = 16
        epsilon_CNO_1 = 10**(-17.1)
    elif T < 3.6:
        nu_CNO = 15
        epsilon_CNO_1 = 10**(-15.6)
    elif T < 5:
        nu_CNO = 13
        epsilon_CNO_1 = 10**(-12.5)
    else:
        nu_CNO = 1
        epsilon_CNO_1 = 0

    Rho = mu * P / (K * Na * T)
    epsilon_CNO = epsilon_CNO_1 * X * (Z/3) * Rho * (T * 10)**nu_CNO
    cycle = 'CNO'
    C_l_CNO = 0.01845 * epsilon_CNO_1 * X * (Z/3) * (10 ** nu_CNO) * (mu ** 2)

    return epsilon_CNO, nu_CNO, cycle, C_l_CNO


def energy_generation_rate(T, P, X, Z, mu):
    """
    Computes the energy generation rate and associated parameters based on the temperature and pressure.

    Parameters:
    - T: Temperature (in units of 10^7 K).
    - P: Pressure (in CGS units).
    - X: Hydrogen mass fraction.
    - Z: Metal mass fraction.
    - mu: Mean molecular weight.

    Returns:
    - epsilon: Energy generation rate.
    - nu: Exponent for the temperature dependence.
    - cycle: Type of nuclear cycle.
    - C_l: Coefficient for the energy generation rate.
    """
    if T < 1.2:
        epsilon, nu, cycle, C_l = pp_chain(T, P, X, mu)
    elif T > 2.4:
        epsilon, nu, cycle, C_l = CNO_cycle(T, P, X, Z, mu)
    else:
        epsilon_pp, nu_pp, cycle_pp, C_l_pp = pp_chain(T, P, X, mu)
        epsilon_CNO, nu_CNO, cycle_CNO, C_l_CNO = CNO_cycle(T, P, X, Z, mu)

        if epsilon_pp > epsilon_CNO:
            epsilon = epsilon_pp
            nu = nu_pp
            cycle = cycle_pp
            C_l = C_l_pp

        else:
            epsilon = epsilon_CNO
            nu = nu_CNO
            cycle = cycle_CNO
            C_l = C_l_CNO

    return epsilon, nu, cycle, C_l
