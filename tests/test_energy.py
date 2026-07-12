"""Unit tests for the nuclear energy generation functions in src/energy.py.

Now that energy generation is a set of pure functions, its regime boundaries and
cycle-selection logic can be tested directly, without building a full model.
"""

import pytest

from src.energy import pp_chain, CNO_cycle, energy_generation_rate

# Reference composition (X = 0.75, Y = 0.22).
X = 0.75
Z = 1 - X - 0.22
MU = 1 / (2 * X + 0.75 * 0.22 + 0.5 * Z)
P = 50.0


# --- pp chain ---------------------------------------------------------------

def test_pp_chain_below_threshold_is_inert():
    # Below T = 0.4 the pp chain produces no energy and reports the "NA" cycle.
    assert pp_chain(0.3, P, X, MU) == (0, 0, "NA", 0)


@pytest.mark.parametrize("T, expected_nu", [
    (0.5, 6),
    (0.8, 5),
    (1.0, 4.5),
    (1.4, 4),
    (2.0, 3.5),
])
def test_pp_chain_nu_regimes(T, expected_nu):
    _, nu, cycle, _ = pp_chain(T, P, X, MU)
    assert nu == expected_nu
    assert cycle == "pp"


def test_pp_chain_regression_value():
    epsilon, nu, cycle, C_l = pp_chain(1.0, P, X, MU)
    assert nu == 4.5
    assert cycle == "pp"
    assert epsilon == pytest.approx(1.7536748122849062e-08, rel=1e-6)
    assert C_l == pytest.approx(0.0003202582556339625, rel=1e-6)


# --- CNO cycle --------------------------------------------------------------

def test_CNO_cycle_below_threshold_is_inert():
    # Below T = 1.2 the CNO exponent and coefficient vanish.
    epsilon, nu, cycle, C_l = CNO_cycle(1.0, P, X, Z, MU)
    assert nu == 0
    assert epsilon == 0
    assert C_l == 0


@pytest.mark.parametrize("T, expected_nu", [
    (1.4, 20),
    (2.0, 18),
    (2.5, 16),
    (3.0, 15),
    (4.0, 13),
])
def test_CNO_cycle_nu_regimes(T, expected_nu):
    _, nu, cycle, _ = CNO_cycle(T, P, X, Z, MU)
    assert nu == expected_nu
    assert cycle == "CNO"


def test_CNO_cycle_regression_value():
    epsilon, nu, cycle, C_l = CNO_cycle(2.0, P, X, Z, MU)
    assert nu == 18
    assert cycle == "CNO"
    assert epsilon == pytest.approx(5.576962538012738e-06, rel=1e-6)
    assert C_l == pytest.approx(7.770322970054077e-07, rel=1e-6)


# --- dispatch ---------------------------------------------------------------

def test_energy_generation_rate_below_all_thresholds():
    assert energy_generation_rate(0.3, P, X, Z, MU) == (0, 0, "NA", 0)


def test_energy_generation_rate_uses_pp_at_low_temperature():
    # For T < 1.2 only the pp chain is considered.
    assert energy_generation_rate(1.0, P, X, Z, MU)[2] == "pp"


def test_energy_generation_rate_uses_CNO_at_high_temperature():
    # For T > 2.4 only the CNO cycle is considered.
    assert energy_generation_rate(3.0, P, X, Z, MU)[2] == "CNO"


def test_energy_generation_rate_picks_dominant_cycle_in_overlap():
    # In the overlap region the dominant cycle (larger epsilon) wins.
    T = 2.0
    eps_pp = pp_chain(T, P, X, MU)[0]
    eps_cno = CNO_cycle(T, P, X, Z, MU)[0]
    epsilon, _, cycle, _ = energy_generation_rate(T, P, X, Z, MU)
    assert epsilon == max(eps_pp, eps_cno)
    assert cycle == ("pp" if eps_pp > eps_cno else "CNO")
