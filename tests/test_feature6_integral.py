# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature6_integral.py
#
# Plain-English Summary:
# Unit tests for Feature 6: Double Integrals & Stored Thermal Energy.
# Verifies:
# 1. Exact average temperature using scipy.integrate.dblquad matches analytical expectation.
# 2. Model C2 integral evaluates to exact theoretical mean of 40.0°C (since ∫ cos(πx/L) dx = 0).
# 3. Discrete grid mean converges closely to the continuous exact average.
# 4. Stored thermal energy E = ρ * cp * thickness * ∬(T - T_amb) dA yields correct physical Joules.
# 5. FR-4 specific heat cp is explicitly flagged as approximate (range 1000–1200 J/(kg·K)).
# ==============================================================================

import pytest
from models import get_model
from features import compute_thermal_load


def test_model_a_double_integral_and_energy():
    """Verify Model A exact double integral, comparison with grid mean, and energy in Joules."""
    model_a = get_model('A')
    res = compute_thermal_load(model_a, material_key="FR-4", T_ambient=25.0)

    # Exact average is approximately 46.47 °C
    assert pytest.approx(res['exact_average'], abs=0.1) == 46.47
    # Grid mean is close to exact continuous average (within 0.5 °C)
    assert abs(res['exact_average'] - res['grid_average']) < 0.5
    # Trapezoid rule average is virtually identical to continuous integral (within 0.01 °C)
    assert pytest.approx(res['trapz_average'], abs=0.01) == 46.46
    assert abs(res['exact_average'] - res['trapz_average']) < 0.01
    assert "cooler edge points" in res['gap_explanation']

    # Thermal energy for Model A is approximately 111.8 Joules
    assert pytest.approx(res['stored_energy_joules'], abs=1.0) == 111.8

    # Specific heat must be labeled as approximate
    assert res['cp_approx'] is True
    assert res['cp'] == 1100.0


def test_model_c2_exact_analytical_integral():
    """
    For Model C2: T = 40 + 30*cos(πx/4)*cos(πy/4).
    Analytically, ∫_0^4 cos(πx/4) dx = 0, so the double integral of the cosine term is 0.
    Therefore, the exact continuous average must be IDENTICALLY 40.0 °C.
    """
    model_c2 = get_model('C2')
    res = compute_thermal_load(model_c2, material_key="FR-4", T_ambient=25.0)

    # Must equal exactly 40.0 °C
    assert pytest.approx(res['exact_average'], abs=1e-3) == 40.00
    assert pytest.approx(res['integral_T'], abs=1e-2) == 40.0 * 16.0  # 640.0 °C·cm²

    # Theoretical energy: (40 - 25) * 0.0016 m² * 1850 * 1100 * 0.0016 = 78.144 J
    expected_energy = 1850.0 * 1100.0 * 0.0016 * (15.0 * 0.0016)
    assert pytest.approx(res['stored_energy_joules'], abs=0.1) == expected_energy


def test_copper_material_properties():
    """Verify stored energy calculation with Copper plate option."""
    model_a = get_model('A')
    res = compute_thermal_load(model_a, material_key="Copper", T_ambient=25.0)

    assert "Copper" in res['material_name']
    assert res['rho'] == 8960.0
    assert res['cp'] == 385.0
    assert res['cp_approx'] is False
    assert res['stored_energy_joules'] > 0
