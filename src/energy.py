"""Nuclear energy generation.

Pure functions for the pp chain and the CNO cycle energy generation rates.
They depend only on the local temperature and pressure and the star's
composition, so they carry no state.
"""

from math import inf

from config.config import K, Na

# Temperature regimes for each cycle. Each row is (T_upper, nu, epsilon_1):
# the first row whose upper bound exceeds T wins. The final inf row is the
# fallback that used to be the `else` branch of the if/elif chains. T is in
# units of 10^7 K.
_PP_REGIMES = [
    (0.6, 6, 10**(-6.84)),
    (0.95, 5, 10**(-6.04)),
    (1.2, 4.5, 10**(-5.56)),
    (1.65, 4, 10**(-5.02)),
    (2.4, 3.5, 10**(-4.40)),
    (inf, 1, 0),
]

_CNO_REGIMES = [
    (1.2, 0, 0),
    (1.6, 20, 10**(-22.2)),
    (2.25, 18, 10**(-19.8)),
    (2.75, 16, 10**(-17.1)),
    (3.6, 15, 10**(-15.6)),
    (5, 13, 10**(-12.5)),
    (inf, 1, 0),
]


def _select_regime(T, regimes):
    """Return the (nu, epsilon_1) of the first regime whose upper T bound exceeds T."""
    for T_upper, nu, epsilon_1 in regimes:
        if T < T_upper:
            return nu, epsilon_1


def _reaction_rate(T, P, mu, abundance, nu, epsilon_1, cycle):
    """Shared energy generation physics for both cycles.

    `abundance` is the composition-dependent factor: X^2 for the pp chain and
    X * Z/3 for the CNO cycle.
    """
    Rho = mu * P / (K * Na * T)
    epsilon = epsilon_1 * abundance * Rho * (T * 10)**nu
    C_l = 0.01845 * epsilon_1 * abundance * (10 ** nu) * (mu ** 2)
    return epsilon, nu, cycle, C_l


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
    nu_pp, epsilon_pp_1 = _select_regime(T, _PP_REGIMES)
    return _reaction_rate(T, P, mu, X * X, nu_pp, epsilon_pp_1, "pp")


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
    nu_CNO, epsilon_CNO_1 = _select_regime(T, _CNO_REGIMES)
    return _reaction_rate(T, P, mu, X * (Z / 3), nu_CNO, epsilon_CNO_1, "CNO")


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
