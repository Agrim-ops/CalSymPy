# ==============================================================================
# CalSymPy (Team 4, Delta-T) — benchmark.py
#
# Plain-English Summary:
# This module benchmarks the computational performance difference between:
# 1. Pure SymPy Symbolic Substitution:
#    Iterating across a grid and evaluating T(x, y) point-by-point via
#    expr.subs({x: xi, y: yj}).evalf().
# 2. Lambdified NumPy Compilation:
#    Evaluating T(X, Y) across the entire grid simultaneously using the
#    pre-compiled NumPy function.
#
# Educational Purpose (MAT 112 & Python):
# Demonstrates to students and faculty why symbolic work must be cached.
# SymPy is designed for analytical differentiation, algebra, and exact mathematics,
# whereas NumPy performs vectorized numerical array processing.
#
# Hard Constraint: Always measures real elapsed wall-clock seconds (time module).
# Never assumes or hardcodes benchmark numbers.
# ==============================================================================

import time
import numpy as np
from models import get_model


def run_benchmark(model=None, grid_res=25):
    """
    Measure real wall-clock seconds for evaluating T on an N x N grid.
    
    Parameters:
        model: ThermalModel instance (defaults to Model A if None)
        grid_res (int): Grid resolution along each axis (N). Default 25 (625 points).
        
    Returns:
        dict: Real measured seconds for SymPy, NumPy, and the speedup ratio.
    """
    if model is None:
        model = get_model('A')

    params = model.default_params
    L = float(params.get('L', 4.0))

    xs = np.linspace(0.0, L, grid_res)
    ys = np.linspace(0.0, L, grid_res)
    X, Y = np.meshgrid(xs, ys)

    # --------------------------------------------------------------------------
    # Benchmark 1: Pure SymPy Point-by-Point Symbolic Substitution
    # --------------------------------------------------------------------------
    # Substitute model parameter values into the symbolic expression once
    param_dict = {sym: params[key] for sym, key in zip(model.param_symbols, model.param_keys)}
    expr_subs = model.T_sym.subs(param_dict)

    sympy_grid = np.zeros((grid_res, grid_res), dtype=float)

    start_sympy = time.perf_counter()
    for i in range(grid_res):
        for j in range(grid_res):
            xi = float(xs[j])
            yj = float(ys[i])
            # Pure symbolic substitution and evaluation
            val = float(expr_subs.subs({model.x_sym: xi, model.y_sym: yj}).evalf())
            sympy_grid[i, j] = val
    end_sympy = time.perf_counter()
    sympy_duration = end_sympy - start_sympy

    # --------------------------------------------------------------------------
    # Benchmark 2: Pre-compiled Lambdified NumPy Function (Vectorized)
    # --------------------------------------------------------------------------
    start_numpy = time.perf_counter()
    numpy_grid = model.evaluate_T(X, Y, params)
    end_numpy = time.perf_counter()
    numpy_duration = end_numpy - start_numpy

    # Speedup ratio
    ratio = sympy_duration / max(numpy_duration, 1e-9)

    # Cross-check accuracy: verify both methods yielded identical values
    max_abs_diff = float(np.max(np.abs(sympy_grid - numpy_grid)))
    values_match = max_abs_diff < 1e-4

    summary_text = (
        f"Benchmark on {grid_res}x{grid_res} Grid ({grid_res * grid_res} points):\n"
        f"- Pure SymPy substitution: {sympy_duration:.4f} seconds\n"
        f"- Lambdified NumPy execution: {numpy_duration:.6f} seconds\n"
        f"- Speedup Ratio: {ratio:.1f}x faster with NumPy caching\n"
        f"- Accuracy verification: Max absolute difference = {max_abs_diff:.2e} (Passed: {values_match})"
    )

    return {
        "grid_resolution": grid_res,
        "total_points": grid_res * grid_res,
        "sympy_seconds": sympy_duration,
        "numpy_seconds": numpy_duration,
        "speedup_ratio": ratio,
        "max_abs_diff": max_abs_diff,
        "values_match": values_match,
        "summary_text": summary_text,
    }
