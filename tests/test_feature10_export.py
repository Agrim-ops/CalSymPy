# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature10_export.py
#
# Plain-English Summary:
# Unit tests for Feature 10: Report Export (Text and CSV).
# Verifies that:
# 1. generate_text_report creates a valid text file containing all required sections.
# 2. generate_csv_report creates a valid CSV file containing key-value metrics.
# 3. Model parameters, hottest point, D-test, risk, exact average, energy,
#    and self-test results are all present in the output files.
# ==============================================================================

import os
import pytest
from models import get_model
from report import generate_text_report, generate_csv_report


def test_text_report_generation(tmp_path):
    """Verify that text report contains all required metrics and sections."""
    model_a = get_model('A')
    out_file = str(tmp_path / "test_report.txt")

    path = generate_text_report(model_a, output_path=out_file)
    assert os.path.exists(path)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "CALCULUS THERMAL ANALYSIS REPORT" in content
    assert "Model A" in content
    assert "HOTTEST POINT & SECOND DERIVATIVE TEST" in content
    assert "85.00 °C" in content
    assert "True Maximum" in content
    assert "RISK ASSESSMENT" in content
    assert "DOUBLE INTEGRAL & THERMAL ENERGY" in content
    assert "THEORETICAL SELF-TEST MATRIX" in content
    assert "PASS" in content


def test_csv_report_generation(tmp_path):
    """Verify that CSV report is created and contains tabular rows."""
    model_a = get_model('A')
    out_file = str(tmp_path / "test_report.csv")

    path = generate_csv_report(model_a, output_path=out_file)
    assert os.path.exists(path)

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) > 20
    joined = "".join(lines)
    assert "Maximum Temperature" in joined
    assert "Stored Thermal Energy" in joined
    assert "Discriminant D" in joined
