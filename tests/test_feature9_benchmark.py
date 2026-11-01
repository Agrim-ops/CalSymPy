# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature9_benchmark.py
#
# Plain-English Summary:
# Unit tests for Feature 9: Benchmark (Pure SymPy vs Lambdified NumPy).
# Verifies that:
# 1. Real execution times are measured using time.perf_counter().
# 2. Both SymPy and NumPy yield numerically equivalent temperature grids.
# 3. Vectorized NumPy execution achieves significant speedup over pure SymPy substitution.
# ==============================================================================

import pytest
from benchmark import run_benchmark


def test_benchmark_execution_and_accuracy():
    """Verify that benchmark measures real positive seconds and values agree."""
    # Use a compact 15x15 grid for fast unit test execution (~225 points)
    results = run_benchmark(grid_res=15)

    assert results['grid_resolution'] == 15
    assert results['total_points'] == 225

    # Measured seconds must be real positive numbers
    assert results['sympy_seconds'] > 0.0
    assert results['numpy_seconds'] > 0.0

    # Values must match within numerical floating-point precision
    assert results['values_match'] is True
    assert results['max_abs_diff'] < 1e-4

    # NumPy must be faster than pure SymPy (no fixed speedup number asserted)
    assert results['numpy_seconds'] < results['sympy_seconds']
    assert results['speedup_ratio'] > 1.0
