# ==============================================================================
# CalSymPy (Team 4, Delta-T) — report.py
#
# Plain-English Summary:
# This module generates exportable report files (both human-readable plain text
# and structured CSV format) containing:
# 1. Model name, formula, and active parameter values.
# 2. Hottest point analysis and second derivative test (D-test) classification.
# 3. Semiconductor thermal risk assessment (plain-English and technical).
# 4. Double integral exact average temperature and stored thermal energy (J).
# 5. Theoretical self-test verification matrix results (PASS/FAIL).
#
# The exported file is downloadable directly from Gradio via gr.File.
# ==============================================================================

import os
import csv
import tempfile
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
        f"   - Explanation of Gap: {load['gap_explanation'].capitalize()}",
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
    Generate a structured CSV report for spreadsheet logging.
    
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

    rows = [
        ["Section", "Metric", "Value", "Units / Notes"],
        ["Model", "Model ID", model.model_id, ""],
        ["Model", "Model Name", model.name, ""],
        ["Parameters", "L", merged.get('L', 4.0), "cm"],
        ["Parameters", "T_edge", merged.get('T_edge', 25.0), "°C"],
        ["Parameters", "T0", merged.get('T0', 60.0), "°C"],
        ["Hottest Point", "Maximum Temperature", f"{max_t:.2f}", "°C"],
        ["Hottest Point", "Peak X", f"{p0['x']:.2f}", "cm"],
        ["Hottest Point", "Peak Y", f"{p0['y']:.2f}", "cm"],
        ["Hessian D-Test", "Tx", f"{p0['Tx']:.4f}", "°C/cm"],
        ["Hessian D-Test", "Ty", f"{p0['Ty']:.4f}", "°C/cm"],
        ["Hessian D-Test", "Txx", f"{p0['Txx']:.4f}", ""],
        ["Hessian D-Test", "Tyy", f"{p0['Tyy']:.4f}", ""],
        ["Hessian D-Test", "Txy", f"{p0['Txy']:.4f}", ""],
        ["Hessian D-Test", "Discriminant D", f"{p0['D']:.4f}", ""],
        ["Hessian D-Test", "Classification", p0['classification'], ""],
        ["Risk", "Risk Level", risk_info['level'], ""],
        ["Risk", "Plain-English Assessment", risk_info['plain_english'], "For Non-Technical Stakeholders"],
        ["Risk", "Technical Assessment", risk_info['technical'], "TjMax Margin"],
        ["Thermal Load", "Exact Average Temperature", f"{load['exact_average']:.2f}", "°C (via dblquad)"],
        ["Thermal Load", "Discrete Grid Mean", f"{load['grid_average']:.2f}", "°C"],
        ["Thermal Load", "Stored Thermal Energy", f"{load['stored_energy_joules']:.2f}", "Joules"],
        ["Thermal Load", "Material", load['material_name'], ""],
        ["Self-Test", "Total Checks", selftest_res['total'], ""],
        ["Self-Test", "Passed Checks", selftest_res['passed'], ""],
        ["Self-Test", "Overall Status", "PASS" if selftest_res['all_passed'] else "FAIL", "Evaluated at Defaults"],
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return output_path
