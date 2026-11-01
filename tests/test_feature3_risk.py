# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature3_risk.py
#
# Plain-English Summary:
# Unit tests for Feature 3: Risk Translation.
# Verifies:
# 1. Strict boundary tests at 69.9, 70.0, 90.0, and 90.1 °C.
# 2. Peak temperatures of Model B and Model C (both exactly 70.0 °C) evaluate to MODERATE.
# 3. Model A slider operating scenarios (T_edge=25):
#    - T0 = 30 -> Peak 55.0°C -> LOW
#    - T0 = 60 -> Peak 85.0°C -> MODERATE
#    - T0 = 70 -> Peak 95.0°C -> HIGH
# 4. Plain-English strings match the required stakeholder explanations exactly.
# ==============================================================================

import pytest

from risk import classify_risk, LEVEL_LOW, LEVEL_MODERATE, LEVEL_HIGH
from models import get_model
from features import find_hottest_points


def test_risk_boundary_conditions():
    """Verify exact boundary classifications at 69.9, 70.0, 90.0, and 90.1 °C."""
    # 69.9 °C must be LOW
    r699 = classify_risk(69.9)
    assert r699['level'] == LEVEL_LOW
    assert "LOW" in r699['badge']

    # 70.0 °C must be MODERATE (70.0 <= T <= 90.0)
    r700 = classify_risk(70.0)
    assert r700['level'] == LEVEL_MODERATE
    assert "MODERATE" in r700['badge']

    # 90.0 °C must be MODERATE (70.0 <= T <= 90.0)
    r900 = classify_risk(90.0)
    assert r900['level'] == LEVEL_MODERATE
    assert "MODERATE" in r900['badge']

    # 90.1 °C must be HIGH (T > 90.0)
    r901 = classify_risk(90.1)
    assert r901['level'] == LEVEL_HIGH
    assert "HIGH" in r901['badge']


def test_rounding_before_classification():
    """Verify that numbers like 69.94 round to 69.9 (LOW) while 69.96 rounds to 70.0 (MODERATE)."""
    assert classify_risk(69.94)['level'] == LEVEL_LOW
    assert classify_risk(69.96)['level'] == LEVEL_MODERATE
    assert classify_risk(90.04)['level'] == LEVEL_MODERATE
    assert classify_risk(90.06)['level'] == LEVEL_HIGH


def test_model_b_and_c_peak_risk_badges():
    """
    Models B and C both peak at exactly 70.0 °C.
    Verify they both receive the MODERATE badge.
    """
    model_b = get_model('B')
    res_b = find_hottest_points(model_b)
    risk_b = classify_risk(res_b['max_temperature'])
    assert pytest.approx(res_b['max_temperature'], abs=1e-2) == 70.0
    assert risk_b['level'] == LEVEL_MODERATE
    assert risk_b['badge'] == "🟡 MODERATE RISK"

    model_c = get_model('C')
    res_c = find_hottest_points(model_c)
    risk_c = classify_risk(res_c['max_temperature'])
    assert pytest.approx(res_c['max_temperature'], abs=1e-2) == 70.0
    assert risk_c['level'] == LEVEL_MODERATE
    assert risk_c['badge'] == "🟡 MODERATE RISK"


def test_model_a_slider_load_scenarios():
    """
    Verify Model A (T_edge=25) risk levels across slider loads:
    - T0 = 30 -> T_max = 55.0 °C -> LOW
    - T0 = 60 -> T_max = 85.0 °C -> MODERATE
    - T0 = 70 -> T_max = 95.0 °C -> HIGH
    """
    model_a = get_model('A')

    # Idle load scenario: T0 = 30
    res_idle = find_hottest_points(model_a, params={'T_edge': 25.0, 'T0': 30.0})
    risk_idle = classify_risk(res_idle['max_temperature'])
    assert pytest.approx(res_idle['max_temperature'], abs=1e-2) == 55.0
    assert risk_idle['level'] == LEVEL_LOW

    # Normal load scenario: T0 = 60
    res_norm = find_hottest_points(model_a, params={'T_edge': 25.0, 'T0': 60.0})
    risk_norm = classify_risk(res_norm['max_temperature'])
    assert pytest.approx(res_norm['max_temperature'], abs=1e-2) == 85.0
    assert risk_norm['level'] == LEVEL_MODERATE

    # Heavy load scenario: T0 = 70
    res_heavy = find_hottest_points(model_a, params={'T_edge': 25.0, 'T0': 70.0})
    risk_heavy = classify_risk(res_heavy['max_temperature'])
    assert pytest.approx(res_heavy['max_temperature'], abs=1e-2) == 95.0
    assert risk_heavy['level'] == LEVEL_HIGH


def test_all_15_model_scenario_presets():
    """
    Verify all 15 model and scenario combinations (5 models x 3 presets):
    - Idle: Target Peak ≈ 55 °C -> LOW
    - Normal: Target Peak ≈ 80 °C -> MODERATE
    - Heavy: Target Peak ≈ 100 °C -> HIGH
    """
    preset_configs = {
        'A':  {'Idle': 30.0, 'Normal': 55.0, 'Heavy': 75.0},
        'B':  {'Idle': 35.0, 'Normal': 60.0, 'Heavy': 80.0},
        'C':  {'Idle': 15.0, 'Normal': 40.0, 'Heavy': 60.0},
        'C2': {'Idle': 15.0, 'Normal': 40.0, 'Heavy': 60.0},
        'D':  {'Idle': 29.0, 'Normal': 53.0, 'Heavy': 72.3},
    }

    expected_levels = {'Idle': LEVEL_LOW, 'Normal': LEVEL_MODERATE, 'Heavy': LEVEL_HIGH}

    for m_id in ['A', 'B', 'C', 'C2', 'D']:
        model = get_model(m_id)
        for preset_name, expected_level in expected_levels.items():
            t0_val = preset_configs[m_id][preset_name]
            params = model.default_params.copy()
            if m_id == 'D':
                params['T1'] = t0_val
                params['T2'] = t0_val
            else:
                params['T0'] = t0_val

            res = find_hottest_points(model, params)
            peak_t = res['max_temperature']
            risk_info = classify_risk(peak_t)

            if preset_name == 'Idle':
                assert pytest.approx(peak_t, abs=1.0) == 55.0
                assert risk_info['level'] == LEVEL_LOW
            elif preset_name == 'Normal':
                assert pytest.approx(peak_t, abs=1.0) == 80.0
                assert risk_info['level'] == LEVEL_MODERATE
            else:  # Heavy
                assert pytest.approx(peak_t, abs=1.0) == 100.0
                assert risk_info['level'] == LEVEL_HIGH


def test_plain_english_exact_text():
    """Verify that plain-English sentences match the required phrasing for non-technical readers."""
    r_low = classify_risk(50.0)
    assert r_low['plain_english'] == "This component is running at a safe temperature. No action needed right now."

    r_mod = classify_risk(80.0)
    assert r_mod['plain_english'] == (
        "This part is running warmer than ideal. It's not an emergency, but it's "
        "worth adding some cooling soon - cheaper to prevent now than repair later."
    )

    r_high = classify_risk(95.0)
    assert r_high['plain_english'] == (
        "This part is running dangerously hot. If nothing changes it will likely "
        "slow down or fail, which usually costs more to fix later than to prevent now."
    )
