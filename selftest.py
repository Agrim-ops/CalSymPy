# ==============================================================================
# CalSymPy (Team 4, Delta-T) — selftest.py
#
# Plain-English Summary:
# This module provides a self-test panel that independently verifies all
# theoretical "KNOWN VALUES" specified by the engineering faculty.
#
# Important Design Rule:
# As instructed by the user, the self-test suite ALWAYS evaluates models strictly
# at their DEFAULT parameters, completely isolated from any current UI slider values.
#
# Checked Benchmark Quantities:
# 1. Model A:
#    - T(2,2) = 85.00 °C, Tx(2,2) = 0.00, Ty(2,2) = 0.00
#    - Txx(2,2) = -60.00, Tyy(2,2) = -60.00, Laplacian(2,2) = -120.00
#    - T(3,2) = 61.39 °C, Tx(3,2) = -36.39, Ty(3,2) = 0.00
#    - T(3,3) = 47.07 °C, Tx(3,3) = -22.07, Ty(3,3) = -22.07, |∇T|(3,3) = 31.22 °C/cm
# 2. Model B:
#    - Edge points = 20.00 °C, Centre (2,2) = 70.00 °C
#    - T(1,2) = 55.36 °C, Tx(1,2) = 27.77, Ty(1,2) = 0.00
# 3. Model C:
#    - Edge temperature = 40.00 °C, Normal derivatives = 0 on all 4 edges
# 4. Model C2:
#    - T(1,1) = 55.00 °C, Tx(1,1) = -11.78, Ty(1,1) = -11.78
#    - Insulated edges: Tx = 0 on x=0, 4; Ty = 0 on y=0, 4
#    - Tied corner peaks: (0,0) and (4,4) at 70.00 °C
# 5. Model D:
#    - Near (1.3, 1.3), temperature ≈ 71.7 °C (exact 71.64 °C)
# ==============================================================================

import math
import numpy as np
from models import get_model
from calculus import compute_gradient_magnitude, compute_laplacian, compute_discriminant
from features import find_hottest_points


def run_all_self_tests():
    """
    Execute all KNOWN VALUES verification tests using factory default parameters.
    
    Returns:
        dict: Contains:
              - 'records': list of dicts suitable for Gradio DataFrame or table display
              - 'total': total number of checks
              - 'passed': count of passing tests
              - 'failed': count of failing tests
              - 'all_passed': boolean flag
    """
    records = []

    def _record(model_id, check_name, expected_str, actual_val, expected_val, tol, note=""):
        diff = abs(actual_val - expected_val)
        passed = diff <= tol
        status = "PASS" if passed else "FAIL"
        records.append({
            "Model": f"Model {model_id}",
            "Check Description": check_name,
            "Expected": expected_str,
            "Actual": f"{actual_val:.2f}",
            "Difference": f"{diff:.4f}",
            "Status": status,
            "Notes": note,
        })
        return passed

    # ==========================================================================
    # Model A Checks (at defaults: T_edge=25, T0=60, s=2, cx=cy=2, L=4)
    # ==========================================================================
    mA = get_model('A')
    pA = mA.default_params

    # 1. T(2,2) = 85.0
    t_22 = float(mA.evaluate_T(2.0, 2.0, pA))
    _record('A', "T(2, 2) Hotspot Peak", "85.00 °C", t_22, 85.0, 1e-2, "Peak temperature")

    # 2. Tx(2,2)=0, Ty(2,2)=0
    tx_22, ty_22 = [float(v) for v in mA.evaluate_gradient(2.0, 2.0, pA)]
    _record('A', "Tx(2, 2)", "0.00", tx_22, 0.0, 1e-3, "First partial x")
    _record('A', "Ty(2, 2)", "0.00", ty_22, 0.0, 1e-3, "First partial y")

    # 3. Txx(2,2)=-60, Tyy(2,2)=-60, Laplacian=-120
    txx_22, tyy_22, _ = [float(v) for v in mA.evaluate_hessian(2.0, 2.0, pA)]
    _record('A', "Txx(2, 2)", "-60.00", txx_22, -60.0, 1e-2, "Second partial x")
    _record('A', "Tyy(2, 2)", "-60.00", tyy_22, -60.0, 1e-2, "Second partial y")
    lap_22 = txx_22 + tyy_22
    _record('A', "Laplacian ∇²T(2, 2)", "-120.00", lap_22, -120.0, 1e-2, "Concavity sum")

    # 4. Point (3, 2): T=61.39, Tx=-36.39, Ty=0
    t_32 = float(mA.evaluate_T(3.0, 2.0, pA))
    tx_32, ty_32 = [float(v) for v in mA.evaluate_gradient(3.0, 2.0, pA)]
    _record('A', "T(3, 2)", "61.39 °C", t_32, 61.39, 0.05, "1 cm right of peak")
    _record('A', "Tx(3, 2)", "-36.39", tx_32, -36.39, 0.05, "Negative gradient")
    _record('A', "Ty(3, 2)", "0.00", ty_32, 0.0, 1e-3, "Zero y-gradient on centerline")

    # 5. Point (3, 3): T=47.07, Tx=-22.07, Ty=-22.07, |∇T|=31.22
    t_33 = float(mA.evaluate_T(3.0, 3.0, pA))
    tx_33, ty_33 = [float(v) for v in mA.evaluate_gradient(3.0, 3.0, pA)]
    g_33 = float(np.hypot(tx_33, ty_33))
    _record('A', "T(3, 3)", "47.07 °C", t_33, 47.07, 0.05, "Diagonal point")
    _record('A', "Tx(3, 3)", "-22.07", tx_33, -22.07, 0.05, "Symmetric x-gradient")
    _record('A', "Ty(3, 3)", "-22.07", ty_33, -22.07, 0.05, "Symmetric y-gradient")
    _record('A', "|∇T|(3, 3)", "31.22 °C/cm", g_33, 31.22, 0.05, "Euclidean gradient magnitude")

    # ==========================================================================
    # Model B Checks (at defaults: T_edge=20, T0=50, L=4)
    # ==========================================================================
    mB = get_model('B')
    pB = mB.default_params

    # 1. Edges = 20.0
    t_b_edge_x = float(mB.evaluate_T(0.0, 2.0, pB))
    t_b_edge_y = float(mB.evaluate_T(2.0, 0.0, pB))
    _record('B', "Edge Point (0, 2)", "20.00 °C", t_b_edge_x, 20.0, 1e-3, "Left edge cold baseline")
    _record('B', "Edge Point (2, 0)", "20.00 °C", t_b_edge_y, 20.0, 1e-3, "Bottom edge cold baseline")

    # 2. Centre = 70.0
    t_b_centre = float(mB.evaluate_T(2.0, 2.0, pB))
    _record('B', "Centre (2, 2)", "70.00 °C", t_b_centre, 70.0, 1e-3, "Peak sinusoidal temperature")

    # 3. Point (1, 2): T=55.36, Tx=27.77, Ty=0
    t_b_12 = float(mB.evaluate_T(1.0, 2.0, pB))
    tx_b_12, ty_b_12 = [float(v) for v in mB.evaluate_gradient(1.0, 2.0, pB)]
    _record('B', "T(1, 2)", "55.36 °C", t_b_12, 55.36, 0.05, "Sinusoidal slope point")
    _record('B', "Tx(1, 2)", "27.77", tx_b_12, 27.77, 0.05, "Positive gradient toward center")
    _record('B', "Ty(1, 2)", "0.00", ty_b_12, 0.0, 1e-3, "Zero y-gradient at centerline")

    # ==========================================================================
    # Model C Checks (at defaults: T_edge=40, T0=30, L=4)
    # ==========================================================================
    mC = get_model('C')
    pC = mC.default_params

    # 1. Edge temperature = 40.0
    t_c_edge = float(mC.evaluate_T(0.0, 2.0, pC))
    _record('C', "Edge Temp T(0, 2)", "40.00 °C", t_c_edge, 40.0, 1e-3, "Sealed edge baseline")

    # 2. Normal derivatives = 0 on edges
    tx_c_0, _ = [float(v) for v in mC.evaluate_gradient(0.0, 2.0, pC)]
    tx_c_4, _ = [float(v) for v in mC.evaluate_gradient(4.0, 2.0, pC)]
    _, ty_c_0 = [float(v) for v in mC.evaluate_gradient(2.0, 0.0, pC)]
    _, ty_c_4 = [float(v) for v in mC.evaluate_gradient(2.0, 4.0, pC)]
    _record('C', "Normal Deriv Tx(0, 2)", "0.00", tx_c_0, 0.0, 1e-4, "Sealed boundary")
    _record('C', "Normal Deriv Tx(4, 2)", "0.00", tx_c_4, 0.0, 1e-4, "Sealed boundary")
    _record('C', "Normal Deriv Ty(2, 0)", "0.00", ty_c_0, 0.0, 1e-4, "Sealed boundary")
    _record('C', "Normal Deriv Ty(2, 4)", "0.00", ty_c_4, 0.0, 1e-4, "Sealed boundary")

    # ==========================================================================
    # Model C2 Checks (at defaults: T_edge=40, T0=30, L=4)
    # ==========================================================================
    mC2 = get_model('C2')
    pC2 = mC2.default_params

    # 1. T(1, 1) = 55.0, Tx=Ty=-11.78
    t_c2_11 = float(mC2.evaluate_T(1.0, 1.0, pC2))
    tx_c2_11, ty_c2_11 = [float(v) for v in mC2.evaluate_gradient(1.0, 1.0, pC2)]
    _record('C2', "T(1, 1)", "55.00 °C", t_c2_11, 55.0, 1e-3, "Cosine quarter-phase point")
    _record('C2', "Tx(1, 1)", "-11.78", tx_c2_11, -11.78, 0.05, "Insulated interior gradient x")
    _record('C2', "Ty(1, 1)", "-11.78", ty_c2_11, -11.78, 0.05, "Insulated interior gradient y")

    # 2. Normal derivatives Tx=0 on x=0, 4; Ty=0 on y=0, 4
    tx_c2_0, _ = [float(v) for v in mC2.evaluate_gradient(0.0, 2.5, pC2)]
    tx_c2_4, _ = [float(v) for v in mC2.evaluate_gradient(4.0, 2.5, pC2)]
    _, ty_c2_0 = [float(v) for v in mC2.evaluate_gradient(2.5, 0.0, pC2)]
    _, ty_c2_4 = [float(v) for v in mC2.evaluate_gradient(2.5, 4.0, pC2)]
    _record('C2', "Insulation Tx(0, 2.5)", "0.00", tx_c2_0, 0.0, 1e-5, "True Neumann ∂T/∂n=0")
    _record('C2', "Insulation Tx(4, 2.5)", "0.00", tx_c2_4, 0.0, 1e-5, "True Neumann ∂T/∂n=0")
    _record('C2', "Insulation Ty(2.5, 0)", "0.00", ty_c2_0, 0.0, 1e-5, "True Neumann ∂T/∂n=0")
    _record('C2', "Insulation Ty(2.5, 4)", "0.00", ty_c2_4, 0.0, 1e-5, "True Neumann ∂T/∂n=0")

    # 3. Tied corners (0,0) and (4,4) at 70.0
    t_c2_00 = float(mC2.evaluate_T(0.0, 0.0, pC2))
    t_c2_44 = float(mC2.evaluate_T(4.0, 4.0, pC2))
    _record('C2', "Tied Corner T(0, 0)", "70.00 °C", t_c2_00, 70.0, 1e-3, "First global maximum corner")
    _record('C2', "Tied Corner T(4, 4)", "70.00 °C", t_c2_44, 70.0, 1e-3, "Second global maximum corner")

    # ==========================================================================
    # Model D Checks (Dual Hotspots: 1.2, 1.2 and 2.8, 2.8)
    # ==========================================================================
    mD = get_model('D')
    pD = mD.default_params

    # Point (1.3, 1.3) ≈ 71.7 °C (exact 71.64 °C)
    t_d_13 = float(mD.evaluate_T(1.3, 1.3, pD))
    _record('D', "T(1.3, 1.3) Near Hotspot", "71.70 °C", t_d_13, 71.7, 0.15, "Near primary hotspot (exact 71.64 °C)")

    # Summarize overall results
    passed_count = sum(1 for r in records if r["Status"] == "PASS")
    total_count = len(records)
    failed_count = total_count - passed_count

    return {
        "records": records,
        "total": total_count,
        "passed": passed_count,
        "failed": failed_count,
        "all_passed": failed_count == 0,
    }
