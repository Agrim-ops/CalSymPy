# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature2_lookup.py
#
# Plain-English Summary:
# Unit tests for Feature 2: Exact Point Lookup.
# Tests that point_lookup evaluates continuous analytical formulas directly
# (not snapping to nearest grid cells) and verifies all KNOWN VALUES:
# 1. Model A at (2, 2): T=85.0, Tx=0, Ty=0, Txx=-60, Tyy=-60, Laplacian=-120
# 2. Model A at (3, 2): T=61.39, Tx=-36.39, Ty=0
# 3. Model A at (3, 3): T=47.07, Tx=-22.07, Ty=-22.07, |grad|=31.22
# 4. Model B at (1, 2): T=55.36, Tx=27.77, Ty=0; Edge (0, 2): T=20.0
# 5. Model C2 at (1, 1): T=55.0, Tx=Ty=-11.78; Normal derivatives Tx=0 on x=0,4; Ty=0 on y=0,4
# 6. Continuous float evaluation: Arbitrary irrational coordinates evaluate smoothly without grid snapping.
# ==============================================================================

import pytest
import math

from models import get_model
from features import point_lookup


def test_lookup_model_a_center():
    """Verify Model A at hotspot centre (2, 2)."""
    model_a = get_model('A')
    res = point_lookup(model_a, 2.0, 2.0)

    assert pytest.approx(res['T'], abs=1e-2) == 85.0
    assert pytest.approx(res['Tx'], abs=1e-3) == 0.0
    assert pytest.approx(res['Ty'], abs=1e-3) == 0.0
    assert pytest.approx(res['grad_magnitude'], abs=1e-3) == 0.0
    assert pytest.approx(res['Txx'], abs=1e-2) == -60.0
    assert pytest.approx(res['Tyy'], abs=1e-2) == -60.0
    assert pytest.approx(res['laplacian'], abs=1e-2) == -120.0


def test_lookup_model_a_known_points():
    """Verify Model A at known test points (3, 2) and (3, 3)."""
    model_a = get_model('A')

    # Point (3, 2)
    res_32 = point_lookup(model_a, 3.0, 2.0)
    assert pytest.approx(res_32['T'], abs=0.01) == 61.39
    assert pytest.approx(res_32['Tx'], abs=0.01) == -36.39
    assert pytest.approx(res_32['Ty'], abs=0.01) == 0.0

    # Point (3, 3)
    res_33 = point_lookup(model_a, 3.0, 3.0)
    assert pytest.approx(res_33['T'], abs=0.01) == 47.07
    assert pytest.approx(res_33['Tx'], abs=0.01) == -22.07
    assert pytest.approx(res_33['Ty'], abs=0.01) == -22.07
    assert pytest.approx(res_33['grad_magnitude'], abs=0.01) == 31.22


def test_lookup_model_b_known_points():
    """Verify Model B at (1, 2) and on boundary."""
    model_b = get_model('B')

    # Point (1, 2)
    res_12 = point_lookup(model_b, 1.0, 2.0)
    assert pytest.approx(res_12['T'], abs=0.01) == 55.36
    assert pytest.approx(res_12['Tx'], abs=0.01) == 27.77
    assert pytest.approx(res_12['Ty'], abs=0.01) == 0.0

    # Cold edge at (0, 2)
    res_edge = point_lookup(model_b, 0.0, 2.0)
    assert pytest.approx(res_edge['T'], abs=1e-2) == 20.0


def test_lookup_model_c2_known_points_and_insulation():
    """Verify Model C2 at (1, 1) and true insulation ∂T/∂n = 0 on all edges."""
    model_c2 = get_model('C2')

    # Point (1, 1)
    res_11 = point_lookup(model_c2, 1.0, 1.0)
    assert pytest.approx(res_11['T'], abs=0.01) == 55.00
    assert pytest.approx(res_11['Tx'], abs=0.01) == -11.78
    assert pytest.approx(res_11['Ty'], abs=0.01) == -11.78

    # Verify normal derivatives vanish on all 4 boundaries
    # x=0 boundary (Tx must be 0)
    for y_test in [0.5, 1.7, 3.1]:
        res_x0 = point_lookup(model_c2, 0.0, y_test)
        assert pytest.approx(res_x0['Tx'], abs=1e-5) == 0.0

    # x=4 boundary (Tx must be 0)
    for y_test in [0.5, 1.7, 3.1]:
        res_x4 = point_lookup(model_c2, 4.0, y_test)
        assert pytest.approx(res_x4['Tx'], abs=1e-5) == 0.0

    # y=0 boundary (Ty must be 0)
    for x_test in [0.5, 1.7, 3.1]:
        res_y0 = point_lookup(model_c2, x_test, 0.0)
        assert pytest.approx(res_y0['Ty'], abs=1e-5) == 0.0

    # y=4 boundary (Ty must be 0)
    for x_test in [0.5, 1.7, 3.1]:
        res_y4 = point_lookup(model_c2, x_test, 4.0)
        assert pytest.approx(res_y4['Ty'], abs=1e-5) == 0.0


def test_lookup_arbitrary_continuous_coordinates():
    """Verify exact formula evaluation without snapping to a discrete grid."""
    model_a = get_model('A')
    # Use non-grid irrational coordinates
    x_exact = math.sqrt(2.0)  # ~1.41421356
    y_exact = math.e / 2.0    # ~1.35914091

    res = point_lookup(model_a, x_exact, y_exact)

    # Theoretical exact formula: T = 25 + 60*exp(-((x-2)^2 + (y-2)^2)/2)
    expected_T = 25.0 + 60.0 * math.exp(-((x_exact - 2.0)**2 + (y_exact - 2.0)**2) / 2.0)
    assert pytest.approx(res['T'], rel=1e-7) == expected_T
