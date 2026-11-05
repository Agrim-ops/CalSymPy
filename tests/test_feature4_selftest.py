# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature4_selftest.py
#
# Plain-English Summary:
# Unit tests for Feature 4: Self-Test Panel.
# Verifies that run_all_self_tests() runs all KNOWN VALUES checks and achieves 100% PASS.
# Confirms that evaluation uses factory default parameters independently of any changes.
# ==============================================================================

import pytest
from selftest import run_all_self_tests
from models import get_model


def test_all_known_values_pass():
    """Verify that every single check in the self-test panel passes with status PASS."""
    results = run_all_self_tests()

    assert results['total'] >= 25
    assert results['all_passed'] is True
    assert results['failed'] == 0
    assert results['passed'] == results['total']

    # Ensure every single record has status PASS
    for record in results['records']:
        assert record['Status'] == "PASS", f"Check failed: {record}"


def test_selftest_evaluates_at_defaults_independently():
    """
    Verify that self-test strictly uses default parameters even if
    another caller passes modified parameters elsewhere.
    """
    model_a = get_model('A')
    # Temporarily evaluate with non-default params
    _ = model_a.evaluate_T(2.0, 2.0, {'T0': 10.0, 'T_edge': 15.0})

    # Run self test and verify it still evaluated at defaults (T=85.0 for A)
    results = run_all_self_tests()
    a_peak_record = next(r for r in results['records'] if r['Check Description'] == "T(2, 2) Hotspot Peak")
    assert a_peak_record['Actual'] == "85.00"
    assert a_peak_record['Status'] == "PASS"


def test_selftest_total_count_and_model_d_checks():
    """Verify total checks count is 37 and Model D saddle and peak are verified."""
    results = run_all_self_tests()
    assert results['total'] == 37
    descs = [r['Check Description'] for r in results['records']]
    assert "Saddle T(2, 2)" in descs
    assert "Saddle D(2, 2)" in descs
    assert "Peak T(1.267, 1.267)" in descs
