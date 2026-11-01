# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature5_compare.py
#
# Plain-English Summary:
# Unit tests for Feature 5: Multi-Model Comparison.
# Verifies that:
# 1. Comparison table evaluates all 5 models (A, B, C, C2, D).
# 2. Peak temperatures, average temperatures, and average edge gradients are computed.
# 3. Model C has an average edge gradient of exactly 0.00 °C/cm (sealed boundary).
# 4. Model B exhibits high edge gradient dissipation rate (~24.7 °C/cm).
# 5. Model comparison plot generates cleanly as a Matplotlib Figure.
# ==============================================================================

import pytest
import pandas as pd
import matplotlib.pyplot as plt

from features import compute_model_comparison
from plots import plot_model_comparison


def test_model_comparison_structure():
    """Verify that all 5 models are present with required metrics."""
    records = compute_model_comparison()
    assert len(records) == 5

    model_ids = [r['Model ID'] for r in records]
    assert model_ids == ['A', 'B', 'C', 'C2', 'D']

    for r in records:
        assert 'Peak Temp (°C)' in r
        assert 'Average Temp (°C)' in r
        assert 'Avg Edge |∇T| (°C/cm)' in r
        assert 'Risk Level' in r
        assert 'Risk Badge' in r


def test_model_comparison_exact_values():
    """Verify specific numerical values across models."""
    records = compute_model_comparison()
    by_id = {r['Model ID']: r for r in records}

    # Model A: Peak = 85.0
    assert pytest.approx(by_id['A']['Peak Temp (°C)'], abs=0.1) == 85.0
    assert pytest.approx(by_id['A']['Average Temp (°C)'], abs=0.5) == 46.1

    # Model B: Peak = 70.0
    assert pytest.approx(by_id['B']['Peak Temp (°C)'], abs=0.1) == 70.0
    assert pytest.approx(by_id['B']['Average Temp (°C)'], abs=0.5) == 39.8
    assert by_id['B']['Avg Edge |∇T| (°C/cm)'] > 20.0

    # Model C: Peak = 70.0, Sealed edges => Avg Edge Grad == 0.00
    assert pytest.approx(by_id['C']['Peak Temp (°C)'], abs=0.1) == 70.0
    assert pytest.approx(by_id['C']['Avg Edge |∇T| (°C/cm)'], abs=1e-3) == 0.00

    # Model C2: Peak = 70.0, Average = 40.0
    assert pytest.approx(by_id['C2']['Peak Temp (°C)'], abs=0.1) == 70.0
    assert pytest.approx(by_id['C2']['Average Temp (°C)'], abs=0.2) == 40.0

    # Model D: Peak ≈ 71.7
    assert pytest.approx(by_id['D']['Peak Temp (°C)'], abs=0.2) == 71.7


def test_model_comparison_plot():
    """Verify that plot_model_comparison generates a valid figure without error."""
    records = compute_model_comparison()
    df = pd.DataFrame(records)
    fig = plot_model_comparison(df)

    assert fig is not None
    assert isinstance(fig, plt.Figure)
    plt.close(fig)
