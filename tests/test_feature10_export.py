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
import pandas as pd
from models import get_model
from report import generate_text_report, generate_csv_report, generate_grid_csv


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
    # Confirm gap explanation maintains upper case for acronyms/terms inside the sentence
    assert "Explanation of Gap:" in content


def test_csv_report_generation(tmp_path):
    """Verify that CSV report is created via pandas and contains structured columns."""
    model_a = get_model('A')
    out_file = str(tmp_path / "test_report.csv")

    path = generate_csv_report(model_a, output_path=out_file)
    assert os.path.exists(path)

    df = pd.read_csv(path)
    assert list(df.columns) == ["Section", "Metric", "Value", "Units"]
    assert len(df) > 15
    metrics = list(df["Metric"])
    assert "Maximum Temperature" in metrics
    assert "Stored Thermal Energy" in metrics
    assert "Discriminant D" in metrics


def test_csv_report_model_d_dynamic_params(tmp_path):
    """Verify that CSV report for Model D correctly loops over Model D param_keys without hardcoded T_edge/T0."""
    model_d = get_model('D')
    out_file = str(tmp_path / "test_report_d.csv")

    path = generate_csv_report(model_d, output_path=out_file)
    assert os.path.exists(path)

    df = pd.read_csv(path)
    params_section = df[df["Section"] == "Parameters"]
    param_names = set(params_section["Metric"])
    assert "T1" in param_names
    assert "cx1" in param_names
    assert "s1" in param_names
    assert "T0" not in param_names


def test_grid_csv_generation(tmp_path):
    """Verify that grid CSV export produces a pandas DataFrame with x, y, T, Tx, Ty."""
    model_a = get_model('A')
    out_file = str(tmp_path / "test_grid.csv")

    path = generate_grid_csv(model_a, grid_res=21, output_path=out_file)
    assert os.path.exists(path)

    df = pd.read_csv(path)
    assert list(df.columns) == ["x", "y", "T", "Tx", "Ty"]
    assert len(df) == 21 * 21  # 441 points
    assert df["T"].max() > 80.0
