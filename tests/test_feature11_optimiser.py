# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature11_optimiser.py
#
# Plain-English Summary:
# Unit tests for Feature 11 (Stretch): Advanced Calculus Optimizations.
# Verifies:
# 1. 2D Gradient Descent moves a heat source away from a sensitive component,
#    cooling the component while respecting boundary margins.
# 2. Lagrange Multipliers solves for the hottest point along a straight line (mounting rail)
#    and cross-checks successfully against a 1D numerical grid search.
# 3. Optimization and Lagrange plots generate cleanly.
# ==============================================================================

import pytest
import matplotlib.pyplot as plt
from models import get_model
from features import run_gradient_descent_optimization, solve_lagrange_rail_constraint
from plots import plot_optimization_trajectory, plot_lagrange_rail


def test_gradient_descent_minimization():
    """Verify that Gradient Descent cools the sensitive sensor by relocating the heat source."""
    model_a = get_model('A')
    res = run_gradient_descent_optimization(
        model=model_a,
        sensor_pos=(1.0, 1.0),
        init_source=(1.5, 1.5),
        margin=0.3,
        step_size=0.08,
        max_iters=50,
    )

    # Must take iterative steps
    assert res['steps_taken'] > 0
    assert len(res['trajectory']) > 1

    # Final temperature at sensor must be strictly lower than initial
    assert res['final_sensor_temp'] < res['initial_sensor_temp']
    assert res['cooling_achieved'] > 20.0  # Cools by more than 20 °C

    # Final source position must remain within plate margins [0.3, 3.7]
    fx, fy = res['final_source']
    assert 0.3 <= fx <= 3.7
    assert 0.3 <= fy <= 3.7


def test_lagrange_multipliers_mounting_rail():
    """
    Verify Lagrange Multipliers for straight rail x + y = 4 on Model A.
    The center of the hotspot is at (2, 2), which lies directly on the line x + y = 4!
    Therefore, the hottest point on the rail must be exactly (2.0, 2.0) with T = 85.0 °C.
    """
    model_a = get_model('A')
    res = solve_lagrange_rail_constraint(model=model_a, a=1.0, b=1.0, c=4.0)

    # Analytical solution
    opt = res['best_analytical']
    assert pytest.approx(opt['x'], abs=0.05) == 2.0
    assert pytest.approx(opt['y'], abs=0.05) == 2.0
    assert pytest.approx(opt['T'], abs=0.1) == 85.0

    # Cross-check with 1D line grid search
    grid_opt = res['grid_best']
    assert pytest.approx(grid_opt['x'], abs=0.05) == 2.0
    assert pytest.approx(grid_opt['y'], abs=0.05) == 2.0
    assert pytest.approx(grid_opt['T'], abs=0.1) == 85.0


def test_optimiser_plots():
    """Verify that optimization and Lagrange plots render valid figures."""
    model_a = get_model('A')
    res_gd = run_gradient_descent_optimization(model_a)
    fig_gd = plot_optimization_trajectory(model_a, res_gd['sensor_pos'], res_gd['trajectory'])
    assert isinstance(fig_gd, plt.Figure)
    plt.close(fig_gd)

    res_lm = solve_lagrange_rail_constraint(model_a)
    fig_lm = plot_lagrange_rail(model_a, 1.0, 1.0, 4.0, res_lm['best_analytical'])
    assert isinstance(fig_lm, plt.Figure)
    plt.close(fig_lm)


def test_optimiser_plots_with_custom_params_and_vertical_rail():
    """Verify that plots accept custom slider params and vertical rails (b=0) render cleanly."""
    model_a = get_model('A')
    res_gd = run_gradient_descent_optimization(model_a)
    custom_params = {'T_edge': 20.0, 'T0': 50.0, 's': 2.0, 'cx': 2.0, 'cy': 2.0, 'L': 4.0}

    # Custom params on trajectory plot
    fig_gd = plot_optimization_trajectory(
        model_a, res_gd['sensor_pos'], res_gd['trajectory'], params=custom_params
    )
    assert isinstance(fig_gd, plt.Figure)
    plt.close(fig_gd)

    # Vertical rail (b=0, 1*x + 0*y = 2 => x=2)
    dummy_opt = {'x': 2.0, 'y': 2.0, 'T': 85.0}
    fig_vert = plot_lagrange_rail(
        model_a, a=1.0, b=0.0, c=2.0, optimal_pt=dummy_opt, params=custom_params
    )
    assert isinstance(fig_vert, plt.Figure)
    plt.close(fig_vert)
