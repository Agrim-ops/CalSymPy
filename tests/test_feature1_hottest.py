# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature1_hottest.py
#
# Plain-English Summary:
# Unit tests for Feature 1: Hottest Point + Second Derivative Test.
# Verifies:
# 1. Model A reaches single peak at (2, 2) with T=85.0°C and D=3600 (True Maximum).
# 2. Model B reaches single peak at (2, 2) with T=70.0°C and D > 0 (True Maximum).
# 3. Model C reaches single peak at (2, 2) with T=70.0°C and D > 0 (True Maximum).
# 4. Model C2 handles TIED peaks at corners (0, 0) and (4, 4), both at 70.0°C,
#    verifying D > 0 and Txx < 0 at both corners.
# 5. Model C2 centre point (2, 2) is verified as a saddle point (D < 0).
# 6. Second derivative test classifications: Minimum, Maximum, Saddle Point, Inconclusive.
# ==============================================================================

import pytest
import numpy as np

from models import get_model
from calculus import classify_critical_point, compute_discriminant
from features import find_hottest_points


def test_model_a_hottest_point():
    """Verify Model A single hotspot at (2, 2) with T=85°C and second derivative test."""
    model_a = get_model('A')
    result = find_hottest_points(model_a)

    assert pytest.approx(result['max_temperature'], abs=1e-2) == 85.0
    assert result['is_tie'] is False
    assert len(result['peaks']) == 1

    peak = result['peaks'][0]
    assert pytest.approx(peak['x'], abs=0.05) == 2.0
    assert pytest.approx(peak['y'], abs=0.05) == 2.0
    assert pytest.approx(peak['T'], abs=1e-2) == 85.0
    assert pytest.approx(peak['Tx'], abs=1e-3) == 0.0
    assert pytest.approx(peak['Ty'], abs=1e-3) == 0.0
    assert pytest.approx(peak['Txx'], abs=1e-2) == -60.0
    assert pytest.approx(peak['Tyy'], abs=1e-2) == -60.0
    assert pytest.approx(peak['Txy'], abs=1e-2) == 0.0
    assert peak['D'] > 0
    assert peak['classification'] == "True Maximum"


def test_model_b_hottest_point():
    """Verify Model B centre peak at (2, 2) with T=70°C and True Maximum."""
    model_b = get_model('B')
    result = find_hottest_points(model_b)

    assert pytest.approx(result['max_temperature'], abs=1e-2) == 70.0
    assert result['is_tie'] is False
    peak = result['peaks'][0]
    assert pytest.approx(peak['x'], abs=0.05) == 2.0
    assert pytest.approx(peak['y'], abs=0.05) == 2.0
    assert peak['D'] > 0
    assert peak['Txx'] < 0
    assert peak['classification'] == "True Maximum"


def test_model_c_hottest_point():
    """Verify Model C centre peak at (2, 2) with T=70°C and True Maximum."""
    model_c = get_model('C')
    result = find_hottest_points(model_c)

    assert pytest.approx(result['max_temperature'], abs=1e-2) == 70.0
    assert result['is_tie'] is False
    peak = result['peaks'][0]
    assert pytest.approx(peak['x'], abs=0.05) == 2.0
    assert pytest.approx(peak['y'], abs=0.05) == 2.0
    assert peak['D'] > 0
    assert peak['Txx'] < 0
    assert peak['classification'] == "True Maximum"


def test_model_c2_tied_corner_peaks():
    """
    Verify Model C2 has TIED hottest points at corners (0,0) and (4,4), both at 70°C.
    Both corners must have D > 0 and Txx < 0, confirming them as True Maxima.
    """
    model_c2 = get_model('C2')
    result = find_hottest_points(model_c2)

    # Maximum temperature must be 70.0°C
    assert pytest.approx(result['max_temperature'], abs=1e-2) == 70.0

    # Must detect a tie with at least 2 distinct peak locations
    assert result['is_tie'] is True
    assert len(result['peaks']) == 2

    # Collect coordinates of the peaks
    peak_coords = sorted([(p['x'], p['y']) for p in result['peaks']])
    assert pytest.approx(peak_coords[0][0], abs=0.05) == 0.0
    assert pytest.approx(peak_coords[0][1], abs=0.05) == 0.0

    assert pytest.approx(peak_coords[1][0], abs=0.05) == 4.0
    assert pytest.approx(peak_coords[1][1], abs=0.05) == 4.0

    # Verify second derivative test at both corners
    for p in result['peaks']:
        assert pytest.approx(p['T'], abs=1e-2) == 70.0
        assert p['D'] > 0
        assert p['Txx'] < 0
        assert p['classification'] == "True Maximum"


def test_model_c2_centre_is_saddle_point():
    """
    Verify that the centre (2, 2) of Model C2 is a SADDLE POINT (D < 0),
    not the maximum.
    """
    model_c2 = get_model('C2')
    t_centre = float(model_c2.evaluate_T(2.0, 2.0))
    txx, tyy, txy = model_c2.evaluate_hessian(2.0, 2.0)
    D, classification, explanation = classify_critical_point(txx, tyy, txy)

    assert pytest.approx(t_centre, abs=1e-2) == 40.0
    assert D < 0
    assert classification == "Saddle Point"


def test_second_derivative_test_classifications():
    """Verify all 4 mathematical cases of the second derivative test."""
    # Case 1: True Maximum (D > 0, Txx < 0)
    D1, class1, _ = classify_critical_point(Txx=-4.0, Tyy=-4.0, Txy=0.0)
    assert D1 == 16.0
    assert class1 == "True Maximum"

    # Case 2: True Minimum (D > 0, Txx > 0)
    D2, class2, _ = classify_critical_point(Txx=3.0, Tyy=3.0, Txy=1.0)
    assert D2 == 8.0
    assert class2 == "True Minimum"

    # Case 3: Saddle Point (D < 0)
    D3, class3, _ = classify_critical_point(Txx=2.0, Tyy=-2.0, Txy=0.0)
    assert D3 == -4.0
    assert class3 == "Saddle Point"

    # Case 4: Inconclusive (D == 0)
    D4, class4, _ = classify_critical_point(Txx=0.0, Tyy=0.0, Txy=0.0)
    assert D4 == 0.0
    assert class4 == "Inconclusive"
