"""Regression tests for the stellar interior model.

These tests pin the deterministic output of ``complete_model`` for the two
configurations defined in ``config/config.yaml`` so that any accidental change
in the numerical integration is caught. They also check a few basic physical
sanity conditions on the resulting profiles.
"""

import numpy as np
import pytest

from config.config import (
    M_total,
    X,
    Y,
    T_central,
    R_total,
    L_total,
    M_test,
    X_test,
    Y_test,
    T_test,
    R_test,
    L_test,
)
from src.star_class import StellarModel


def _build_model(params):
    star = StellarModel(*params)
    star.complete_model()
    return star


@pytest.fixture(scope="module")
def test_star():
    return _build_model((M_test, X_test, Y_test, T_test, R_test, L_test))


@pytest.fixture(scope="module")
def star():
    return _build_model((M_total, X, Y, T_central, R_total, L_total))


def test_test_star_error_regression(test_star):
    # Known total relative error for the test-star configuration.
    assert test_star.error == pytest.approx(67.76104608765111, rel=1e-6)


def test_star_error_regression(star):
    # Known total relative error for the star configuration.
    assert star.error == pytest.approx(102.16159150215643, rel=1e-6)


def test_profile_arrays_have_consistent_length(test_star):
    n = len(test_star.R)
    for attr in ("P", "T", "M", "L"):
        assert len(getattr(test_star, attr)) == n


def test_enclosed_mass_reaches_total(test_star):
    # The enclosed mass profile must reach the star's total mass.
    assert test_star.M.max() == pytest.approx(test_star.M_total, rel=1e-6)


def test_error_is_finite(test_star, star):
    assert np.isfinite(test_star.error)
    assert np.isfinite(star.error)
