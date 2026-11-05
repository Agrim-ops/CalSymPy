# ==============================================================================
# CalSymPy (Team 4, Delta-T) — report.py
#
# Plain-English Summary:
# This module generates exportable report files (both human-readable plain text
# and structured CSV format) containing:
# 1. Model name, formula, and active parameter values.
# 2. Hottest point analysis and second derivative test (D-test) classification.
# 3. Semiconductor thermal risk assessment (plain-English and technical).
# 4. Double integral exact average temperature, trapezoid average, and stored energy (J).
# 5. Theoretical self-test verification matrix results (PASS/FAIL).
# 6. Coordinate grid export of temperature and gradient vector fields.
#
# Educational Purpose (MAT 112 & Python):
# Uses pandas DataFrame for clean tabular export and CSV generation.
# ==============================================================================

import os
import tempfile
import numpy as np
import pandas as pd
from models import get_model
from features import find_hottest_points, compute_thermal_load
from risk import classify_risk
from selftest import run_all_self_tests


def generate_text_report(model, params=None, material_key="FR-4", output_path=None):
    """
    Generate a formatted text report summarizing all analytical calculus results.
    
    Returns:
        str: Absolute path to the generated text report file.
    """
    merged = model.default_params.copy()
    if params:
        merged.update(params)

    # 1. Hottest point analysis
    hottest = find_hottest_points(model, merged)
    max_t = hottest['max_temperature']
    p0 = hottest['peaks'][0]

    # 2. Risk classification
    risk_info = classify_risk(max_t)

    # 3. Double integral & energy
    load = compute_thermal_load(model, merged, material_key=material_key)

    # 4. Self-test results
    selftest_res = run_all_self_tests()

    if output_path is None:
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"CalSymPy_Report_{model.model_id}.txt")

    # Format gap explanation preserving the rest of the sentence capitalization
    gap_exp = load.get('gap_explanation', '')
    gap_formatted = (gap_exp[0].upper() + gap_exp[1:]) if gap_exp else ""

    lines = [
        "=" * 78,
        "CALCULUS THERMAL ANALYSIS REPORT — CALSYMPY",
        "Team 4, Delta-T | MAT 112 Engineering Mathematics & Python",
        "=" * 78,
        "",
        "1. MODEL SPECIFICATION",
        f"   - Model ID: {model.model_id}",
        f"   - Model Name: {model.name}",
        f"   - Description: {model.description}",
        f"   - Formula: {model.formula_latex}",
        f"   - Plate Side Length L: {merged.get('L', 4.0)} cm",
        "",
        "2. ACTIVE PARAMETER VALUES",
    ]

    for k in model.param_keys:
        lines.append(f"   - {k}: {merged.get(k)}")

    lines.extend([
        "",
        "3. HOTTEST POINT & SECOND DERIVATIVE TEST (MAT 112)",
        f"   - Maximum Temperature: {max_t:.2f} °C",
        f"   - Peak Coordinates: ({p0['x']:.2f}, {p0['y']:.2f}) cm",
        f"   - First Partial Tx (∂T/∂x): {p0['Tx']:.4f} °C/cm",
        f"   - First Partial Ty (∂T/∂y): {p0['Ty']:.4f} °C/cm",
        f"   - Second Partial Txx (∂²T/∂x²): {p0['Txx']:.4f}",
        f"   - Second Partial Tyy (∂²T/∂y²): {p0['Tyy']:.4f}",
        f"   - Mixed Partial Txy (∂²T/∂x∂y): {p0['Txy']:.4f}",
        f"   - Discriminant D = Txx*Tyy - Txy²: {p0['D']:.4f}",
        f"   - Critical Point Classification: {p0['classification']}",
        f"   - Explanation: {p0['explanation']}",
        "",
        "4. RISK ASSESSMENT (Intel/AMD TjMax ~95-105 °C, 15 °C guardband)",
        f"   - Risk Classification: {risk_info['level']}",
        f"   - Risk Badge: {risk_info['badge']}",
        f"   - Plain-English (for HR / Management):",
        f"     \"{risk_info['plain_english']}\"",
        f"   - Technical Engineering Statement:",
        f"     \"{risk_info['technical']}\"",
        "",
        "5. DOUBLE INTEGRAL & THERMAL ENERGY (scipy.integrate.dblquad)",
        f"   - Plate Area: {load['area_cm2']:.1f} cm² ({load['area_m2']:.6f} m²)",
        f"   - Exact Average Temperature (Continuous Integral): {load['exact_average']:.2f} °C",
        f"   - Discrete Grid Mean: {load['grid_average']:.2f} °C",
        f"   - Trapezoid-Rule Grid Average (np.trapezoid): {load['trapz_average']:.2f} °C",
        f"   - Explanation of Gap: {gap_formatted}",
        f"   - Material: {load['material_name']}",
        f"   - Stored Thermal Energy relative to {load['T_ambient']:.1f} °C ambient: {load['stored_energy_joules']:.2f} Joules",
        f"   - Material Specific Heat: cp = {load['cp']} J/(kg·K) " + ("(Approximate)" if load['cp_approx'] else ""),
        "",
        "6. THEORETICAL SELF-TEST MATRIX (Evaluated at Factory Defaults)",
        f"   - Overall Result: {selftest_res['passed']} / {selftest_res['total']} Checks Passed "
        f"({'ALL PASSED' if selftest_res['all_passed'] else 'FAILURES'})",
        "-" * 78,
        f"{'Model':<10} | {'Check Description':<30} | {'Expected':<12} | {'Actual':<10} | {'Status'}",
        "-" * 78,
    ])

    for r in selftest_res['records']:
        lines.append(
            f"{r['Model']:<10} | {r['Check Description']:<30} | {r['Expected']:<12} | {r['Actual']:<10} | {r['Status']}"
        )

    lines.extend([
        "-" * 78,
        "",
        "NOTE: Educational tool for first-year engineering students. Model is idealized",
        "(uniform isotropic flat plate, steady-state position-only distribution, no time PDEs).",
        "=" * 78,
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


def generate_csv_report(model, params=None, material_key="FR-4", output_path=None):
    """
    Generate a structured CSV report using a pandas DataFrame.
    Dynamically loops over model.param_keys to handle all models cleanly.
    
    Columns: Section, Metric, Value, Units
    
    Returns:
        str: Absolute path to the generated CSV file.
    """
    merged = model.default_params.copy()
    if params:
        merged.update(params)

    hottest = find_hottest_points(model, merged)
    max_t = hottest['max_temperature']
    p0 = hottest['peaks'][0]
    risk_info = classify_risk(max_t)
    load = compute_thermal_load(model, merged, material_key=material_key)
    selftest_res = run_all_self_tests()

    if output_path is None:
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"CalSymPy_Report_{model.model_id}.csv")

    records = [
        {"Section": "Model", "Metric": "Model ID", "Value": model.model_id, "Units": ""},
        {"Section": "Model", "Metric": "Model Name", "Value": model.name, "Units": ""},
    ]

    # Dynamically log all active model parameters
    param_units = {
        'L': 'cm', 'T_edge': '°C', 'T0': '°C', 'T1': '°C', 'T2': '°C',
        's': 'cm²', 's1': 'cm²', 's2': 'cm²',
        'cx': 'cm', 'cy': 'cm', 'cx1': 'cm', 'cy1': 'cm', 'cx2': 'cm', 'cy2': 'cm'
    }
    for k in model.param_keys:
        records.append({
            "Section": "Parameters",
            "Metric": k,
            "Value": str(merged.get(k)),
            "Units": param_units.get(k, "")
        })

    # Calculus metrics
    records.extend([
        {"Section": "Hottest Point", "Metric": "Maximum Temperature", "Value": f"{max_t:.2f}", "Units": "°C"},
        {"Section": "Hottest Point", "Metric": "Peak X", "Value": f"{p0['x']:.2f}", "Units": "cm"},
        {"Section": "Hottest Point", "Metric": "Peak Y", "Value": f"{p0['y']:.2f}", "Units": "cm"},
        {"Section": "Hessian D-Test", "Metric": "Tx", "Value": f"{p0['Tx']:.4f}", "Units": "°C/cm"},
        {"Section": "Hessian D-Test", "Metric": "Ty", "Value": f"{p0['Ty']:.4f}", "Units": "°C/cm"},
        {"Section": "Hessian D-Test", "Metric": "Txx", "Value": f"{p0['Txx']:.4f}", "Units": ""},
        {"Section": "Hessian D-Test", "Metric": "Tyy", "Value": f"{p0['Tyy']:.4f}", "Units": ""},
        {"Section": "Hessian D-Test", "Metric": "Txy", "Value": f"{p0['Txy']:.4f}", "Units": ""},
        {"Section": "Hessian D-Test", "Metric": "Discriminant D", "Value": f"{p0['D']:.4f}", "Units": ""},
        {"Section": "Hessian D-Test", "Metric": "Classification", "Value": p0['classification'], "Units": ""},
        {"Section": "Risk", "Metric": "Risk Level", "Value": risk_info['level'], "Units": ""},
        {"Section": "Risk", "Metric": "Plain-English Assessment", "Value": risk_info['plain_english'], "Units": "For Stakeholders"},
        {"Section": "Risk", "Metric": "Technical Assessment", "Value": risk_info['technical'], "Units": "TjMax Margin"},
        {"Section": "Thermal Load", "Metric": "Exact Average Temperature", "Value": f"{load['exact_average']:.2f}", "Units": "°C (via dblquad)"},
        {"Section": "Thermal Load", "Metric": "Discrete Grid Mean", "Value": f"{load['grid_average']:.2f}", "Units": "°C"},
        {"Section": "Thermal Load", "Metric": "Trapezoid Grid Average", "Value": f"{load['trapz_average']:.2f}", "Units": "°C (np.trapezoid)"},
        {"Section": "Thermal Load", "Metric": "Stored Thermal Energy", "Value": f"{load['stored_energy_joules']:.2f}", "Units": "Joules"},
        {"Section": "Thermal Load", "Metric": "Material", "Value": load['material_name'], "Units": ""},
        {"Section": "Self-Test", "Metric": "Total Checks", "Value": str(selftest_res['total']), "Units": ""},
        {"Section": "Self-Test", "Metric": "Passed Checks", "Value": str(selftest_res['passed']), "Units": ""},
        {"Section": "Self-Test", "Metric": "Overall Status", "Value": "PASS" if selftest_res['all_passed'] else "FAIL", "Units": "Evaluated at Defaults"},
    ])

    # Rebuild using a pandas DataFrame
    df = pd.DataFrame(records, columns=["Section", "Metric", "Value", "Units"])
    df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path


def generate_grid_csv(model, params=None, grid_res=41, output_path=None):
    """
    Export discrete plate coordinate grid data (x, y, T, Tx, Ty) to a CSV file
    using a pandas DataFrame.
    
    Parameters:
        model: ThermalModel instance
        params (dict, optional): Parameter dictionary
        grid_res (int): Grid resolution along each axis (default 41x41 = 1681 points)
        output_path (str, optional): Target file path
        
    Returns:
        str: Absolute path to the generated CSV file.
    """
    merged = model.default_params.copy()
    if params:
        merged.update(params)

    L = float(merged.get('L', 4.0))
    xs = np.linspace(0.0, L, grid_res)
    ys = np.linspace(0.0, L, grid_res)
    X, Y = np.meshgrid(xs, ys)

    # Vectorized numerical evaluation via compiled NumPy functions
    T_grid = model.evaluate_T(X, Y, merged)
    Tx_grid, Ty_grid = model.evaluate_gradient(X, Y, merged)

    data = {
        'x': np.round(X.ravel(), 4),
        'y': np.round(Y.ravel(), 4),
        'T': np.round(T_grid.ravel(), 4),
        'Tx': np.round(Tx_grid.ravel(), 4),
        'Ty': np.round(Ty_grid.ravel(), 4),
    }
    df = pd.DataFrame(data)

    if output_path is None:
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"CalSymPy_Grid_{model.model_id}.csv")

    df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path
