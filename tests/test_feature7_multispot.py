# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature7_multispot.py
#
# Plain-English Summary:
# Unit tests for Feature 7: Multi-Hotspot Model (Model D).
# Verifies:
# 1. Formula: T = 25 + 45*exp(-((x-1.2)²+(y-1.2)²)/1.5) + 45*exp(-((x-2.8)²+(y-2.8)²)/1.5).
# 2. Temperature near primary hotspot at (1.3, 1.3) evaluates to ≈ 71.7 °C (exact 71.64 °C).
# 3. Centre point (2.0, 2.0) has zero gradient by symmetry and is classified as a Saddle Point (D < 0).
# 4. Pipeline integration: find_hottest_points, point_lookup, risk classification,
#    and double integration all execute smoothly for Model D.
# ==============================================================================

import pytest
from models import get_model
from features import find_hottest_points, point_lookup, compute_thermal_load
from calculus import classify_critical_point
from risk import classify_risk


def test_model_d_near_hotspot():
    """Verify Model D temperature near primary hotspot at (1.3, 1.3)."""
    model_d = get_model('D')
    res_13 = point_lookup(model_d, 1.3, 1.3)

    # Expected value: exact SymPy value 71.644 °C with tolerance 1e-3
    assert pytest.approx(res_13['T'], abs=1e-3) == 71.644


def test_model_d_centre_saddle_point():
    """
    Between the two hotspots, the center (2, 2) is a symmetric critical point
    with ∇T = <0, 0> and D < 0, creating a thermal saddle pass.
    """
    model_d = get_model('D')
    res_center = point_lookup(model_d, 2.0, 2.0)

    # Symmetric center
    assert pytest.approx(res_center['Tx'], abs=1e-3) == 0.0
    assert pytest.approx(res_center['Ty'], abs=1e-3) == 0.0

    D, classification, _ = classify_critical_point(
        res_center['Txx'], res_center['Tyy'], res_center['Txy']
    )
    assert D < 0
    assert classification == "Saddle Point"


def test_model_d_pipeline_integration():
    """Verify Model D through the entire analytical pipeline."""
    model_d = get_model('D')

    # 1. Hottest points finder
    hottest = find_hottest_points(model_d)
    assert pytest.approx(hottest['max_temperature'], abs=0.2) == 71.7

    # 2. Risk classification (71.7 °C falls in MODERATE: 70 <= T <= 90)
    risk_info = classify_risk(hottest['max_temperature'])
    assert risk_info['level'] == "MODERATE"
    assert "MODERATE" in risk_info['badge']

    # 3. Double integral & thermal load
    load = compute_thermal_load(model_d, material_key="FR-4", T_ambient=25.0)
    assert load['exact_average'] > 40.0
    assert load['stored_energy_joules'] > 0


def test_model_d_two_equal_maxima():
    """
    Verify Model D has two equal maxima at about (1.265, 1.265) and (2.735, 2.735),
    both reaching ~71.69 °C and classified as True Maxima (D > 0, Txx < 0).
    """
    model_d = get_model('D')
    res = find_hottest_points(model_d)

    assert res['is_tie'] is True
    assert len(res['peaks']) == 2
    assert pytest.approx(res['max_temperature'], abs=0.05) == 71.69

    # Sort peaks by x-coordinate
    peaks = sorted(res['peaks'], key=lambda p: p['x'])
    p1, p2 = peaks[0], peaks[1]

    # Peak 1 near (1.265, 1.265)
    assert pytest.approx(p1['x'], abs=0.015) == 1.265
    assert pytest.approx(p1['y'], abs=0.015) == 1.265
    assert pytest.approx(p1['T'], abs=0.05) == 71.69
    assert p1['D'] > 0
    assert p1['Txx'] < 0
    assert p1['classification'] == "True Maximum"

    # Peak 2 near (2.735, 2.735)
    assert pytest.approx(p2['x'], abs=0.015) == 2.735
    assert pytest.approx(p2['y'], abs=0.015) == 2.735
    assert pytest.approx(p2['T'], abs=0.05) == 71.69
    assert p2['D'] > 0
    assert p2['Txx'] < 0
    assert p2['classification'] == "True Maximum"


def test_model_d_exact_calculus_values_at_saddle_and_peaks():
    """
    Verify exact calculus derivatives for Model D:
    1. Saddle at (2, 2): T=63.34, Txx=-7.50, Tyy=-7.50, Txy=43.62, D=-1846.6.
    2. Each peak (about 1.267, 1.267 and 2.733, 2.733):
       T=71.69, Txx=-53.70, Tyy=-53.70, Txy=8.56, D=2810.45.
    Tolerance 0.01 (D tolerance 0.1).
    """
    model_d = get_model('D')
    pD = model_d.default_params

    # 1. Saddle point at (2, 2)
    saddle = point_lookup(model_d, 2.0, 2.0, pD)
    assert pytest.approx(saddle['T'], abs=0.01) == 63.34
    assert pytest.approx(saddle['Txx'], abs=0.01) == -7.50
    assert pytest.approx(saddle['Tyy'], abs=0.01) == -7.50
    assert pytest.approx(saddle['Txy'], abs=0.01) == 43.62
    D_saddle = saddle['Txx'] * saddle['Tyy'] - saddle['Txy']**2
    assert pytest.approx(D_saddle, abs=0.1) == -1846.6

    # 2. Peaks at (1.267, 1.267) and (2.733, 2.733)
    hottest = find_hottest_points(model_d, pD)
    assert len(hottest['peaks']) == 2
    peaks = sorted(hottest['peaks'], key=lambda p: p['x'])
    p1, p2 = peaks[0], peaks[1]

    # Peak 1 (near 1.267, 1.267)
    assert pytest.approx(p1['x'], abs=0.01) == 1.267
    assert pytest.approx(p1['y'], abs=0.01) == 1.267
    assert pytest.approx(p1['T'], abs=0.01) == 71.69
    assert pytest.approx(p1['Txx'], abs=0.01) == -53.70
    assert pytest.approx(p1['Tyy'], abs=0.01) == -53.70
    assert pytest.approx(p1['Txy'], abs=0.01) == 8.56
    assert pytest.approx(p1['D'], abs=0.01) == 2810.45

    # Peak 2 (near 2.733, 2.733)
    assert pytest.approx(p2['x'], abs=0.01) == 2.733
    assert pytest.approx(p2['y'], abs=0.01) == 2.733
    assert pytest.approx(p2['T'], abs=0.01) == 71.69
    assert pytest.approx(p2['Txx'], abs=0.01) == -53.70
    assert pytest.approx(p2['Tyy'], abs=0.01) == -53.70
    assert pytest.approx(p2['Txy'], abs=0.01) == 8.56
    assert pytest.approx(p2['D'], abs=0.01) == 2810.45


