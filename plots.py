# ==============================================================================
# CalSymPy (Team 4, Delta-T) — plots.py
#
# Plain-English Summary:
# This module generates all visual plots for the CalSymPy tool using Matplotlib:
# 1. Overview Heat Map:
#    Displays the 2D temperature distribution T(x, y) with a fixed shared color scale
#    (20°C to 120°C) so that temperatures are directly comparable across models and
#    high-load conditions do not clip. Overlaid with contour lines, heat-flow direction
#    arrows (-∇T, hot -> cold), and a prominent marker at the hottest point(s).
# 2. Heat Flux Streamlines & Divergence:
#    Plots the heat flux vector field F = -k * ∇T using streamplot, and displays
#    the divergence field div F = -k * ∇²T (sources vs sinks).
# 3. Model Comparison Chart:
#    Multi-metric bar chart comparing Peak, Average, and Edge Gradient across models.
#
# Best Practice: All figures created here are returned to Gradio's gr.Plot and
# properly closed afterwards to prevent memory leaks.
# ==============================================================================

import numpy as np
import sys
import matplotlib
# Use non-interactive Agg backend for Gradio/server generation if not interactive
if 'ipykernel' not in sys.modules and matplotlib.get_backend().lower() != 'agg':
    try:
        matplotlib.use('Agg')
    except Exception:
        pass
import matplotlib.pyplot as plt

from features import find_hottest_points


# Fixed shared temperature scale across all heat maps (as required by specifications)
GLOBAL_VMIN = 20.0
GLOBAL_VMAX = 120.0


def plot_overview(model, params=None, grid_resolution=81):
    """
    Generate the primary overview plot:
    - 2D Temperature heat map (fixed scale 20°C to 120°C, 'inferno' colormap)
    - Isothermal contour lines
    - Heat flow arrows pointing along -∇T (hot -> cold)
    - Star marker(s) at peak location(s)
    
    Returns:
        matplotlib.figure.Figure: The constructed figure.
    """
    merged = model.default_params.copy()
    if params:
        merged.update(params)

    L = float(merged.get('L', 4.0))

    xs = np.linspace(0.0, L, grid_resolution)
    ys = np.linspace(0.0, L, grid_resolution)
    X, Y = np.meshgrid(xs, ys)

    # Evaluate temperature scalar field
    T_grid = model.evaluate_T(X, Y, merged)

    # Locate peaks for visual marking
    hottest_data = find_hottest_points(model, merged, grid_resolution=grid_resolution)
    peaks = hottest_data['peaks']

    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=100)

    # Heatmap with fixed global bounds [20, 120]
    im = ax.imshow(
        T_grid,
        origin='lower',
        extent=[0.0, L, 0.0, L],
        cmap='inferno',
        vmin=GLOBAL_VMIN,
        vmax=GLOBAL_VMAX,
        aspect='equal',
    )

    # Isothermal contour lines
    levels = np.linspace(GLOBAL_VMIN, GLOBAL_VMAX, 11)
    # Filter contour levels that actually fall within T_grid range
    valid_levels = [lvl for lvl in levels if T_grid.min() <= lvl <= T_grid.max()]
    if len(valid_levels) > 1:
        contours = ax.contour(X, Y, T_grid, levels=valid_levels, colors='white', alpha=0.4, linewidths=0.8)
        ax.clabel(contours, inline=True, fontsize=8, fmt='%.0f°C')

    # Heat flow direction arrows: -∇T (heat flows from hot to cold)
    # Downsample grid for legible quiver arrows
    step = max(1, grid_resolution // 12)
    X_q = X[::step, ::step]
    Y_q = Y[::step, ::step]
    Tx_q, Ty_q = model.evaluate_gradient(X_q, Y_q, merged)
    # Negative gradient: F = -k * ∇T
    flow_x = -Tx_q
    flow_y = -Ty_q
    norm = np.hypot(flow_x, flow_y)
    norm[norm == 0] = 1.0  # avoid division by zero
    # Normalized direction arrows
    ax.quiver(
        X_q, Y_q, flow_x / norm, flow_y / norm,
        color='cyan', alpha=0.6, scale=25, width=0.004,
        headwidth=3.5, headlength=4, label='Heat flow (-∇T)'
    )

    # Mark hottest point(s)
    for idx, p in enumerate(peaks):
        ax.plot(
            p['x'], p['y'], marker='*', color='yellow', markersize=14,
            markeredgecolor='red', markeredgewidth=1.5,
            label='Hottest Peak' if idx == 0 else ""
        )
        ax.annotate(
            f"Peak: {p['T']:.1f}°C\n({p['x']:.2f}, {p['y']:.2f})",
            xy=(p['x'], p['y']),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=9,
            fontweight='bold',
            color='white',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.75, edgecolor='yellow')
        )

    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_xlabel("x (cm) — Plate Coordinate", fontsize=10)
    ax.set_ylabel("y (cm) — Plate Coordinate", fontsize=10)
    ax.set_title(f"{model.name}\nPeak: {hottest_data['max_temperature']:.1f}°C", fontsize=11, fontweight='bold')

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Temperature (°C) [Fixed Scale: 20–120 °C]", fontsize=9)

    ax.legend(loc='upper right', fontsize=8, framealpha=0.8)
    fig.tight_layout()
    return fig


def plot_heat_flux_streamlines(model, params=None, k=0.29, grid_resolution=81):
    """
    Generate heat flux streamlines plot:
    Streamlines of F = -k * ∇T over the temperature colormap.
    """
    merged = model.default_params.copy()
    if params:
        merged.update(params)

    L = float(merged.get('L', 4.0))
    xs = np.linspace(0.0, L, grid_resolution)
    ys = np.linspace(0.0, L, grid_resolution)
    X, Y = np.meshgrid(xs, ys)

    T_grid = model.evaluate_T(X, Y, merged)
    Tx_grid, Ty_grid = model.evaluate_gradient(X, Y, merged)

    # Fourier's Law: Heat flux F = -k * ∇T
    Fx = -float(k) * Tx_grid
    Fy = -float(k) * Ty_grid

    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=100)

    im = ax.imshow(
        T_grid,
        origin='lower',
        extent=[0.0, L, 0.0, L],
        cmap='inferno',
        vmin=GLOBAL_VMIN,
        vmax=GLOBAL_VMAX,
        aspect='equal',
    )

    # Streamlines of heat flux
    speed = np.hypot(Fx, Fy)
    lw = 1.0 + 2.0 * (speed / (speed.max() + 1e-6))
    ax.streamplot(xs, ys, Fx, Fy, color='white', density=1.2, linewidth=lw, arrowsize=1.2)

    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_xlabel("x (cm)", fontsize=10)
    ax.set_ylabel("y (cm)", fontsize=10)
    ax.set_title(f"Heat Flux Streamlines (F = -k ∇T)\nk = {k:.2f} W/(m·K)", fontsize=11, fontweight='bold')

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Temperature (°C)", fontsize=9)
    fig.tight_layout()
    return fig


def plot_flux_divergence(model, params=None, k=0.29, grid_resolution=81):
    """
    Generate heat flux divergence plot:
    div F = -k * (Txx + Tyy) = -k * ∇²T.
    Colormap: Coolwarm centered at 0.
    - Positive (Red): Heat source (net heat outflow).
    - Negative (Blue): Heat sink (net heat absorption).
    """
    merged = model.default_params.copy()
    if params:
        merged.update(params)

    L = float(merged.get('L', 4.0))
    xs = np.linspace(0.0, L, grid_resolution)
    ys = np.linspace(0.0, L, grid_resolution)
    X, Y = np.meshgrid(xs, ys)

    Txx_grid, Tyy_grid, _ = model.evaluate_hessian(X, Y, merged)
    # div F = -k * (Txx + Tyy)
    div_F = -float(k) * (Txx_grid + Tyy_grid)

    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=100)

    # Center divergence around zero
    max_abs = max(float(np.max(np.abs(div_F))), 1e-4)

    im = ax.imshow(
        div_F,
        origin='lower',
        extent=[0.0, L, 0.0, L],
        cmap='bwr',
        vmin=-max_abs,
        vmax=max_abs,
        aspect='equal',
    )

    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_xlabel("x (cm)", fontsize=10)
    ax.set_ylabel("y (cm)", fontsize=10)
    ax.set_title(f"Divergence of Heat Flux (div F = -k ∇²T)\nPositive = Source, Negative = Sink", fontsize=11, fontweight='bold')

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("div F (W/m³)", fontsize=9)
    fig.tight_layout()
    return fig


def plot_model_comparison(comparison_df):
    """
    Generate a grouped bar chart comparing thermal metrics across all models.
    
    Parameters:
        comparison_df (pd.DataFrame): DataFrame with columns 'Model ID', 'Peak Temp (°C)',
                                       'Average Temp (°C)', 'Avg Edge |∇T| (°C/cm)'.
    Returns:
        matplotlib.figure.Figure: The comparison bar chart.
    """
    models = comparison_df['Model ID'].tolist()
    peaks = comparison_df['Peak Temp (°C)'].tolist()
    averages = comparison_df['Average Temp (°C)'].tolist()
    edge_grads = comparison_df['Avg Edge |∇T| (°C/cm)'].tolist()

    x = np.arange(len(models))
    width = 0.25

    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=100)

    rects1 = ax.bar(x - width, peaks, width, label='Peak Temp (°C)', color='#d9534f', alpha=0.9)
    rects2 = ax.bar(x, averages, width, label='Average Temp (°C)', color='#f0ad4e', alpha=0.9)
    rects3 = ax.bar(x + width, edge_grads, width, label='Avg Edge |∇T| (°C/cm)', color='#0275d8', alpha=0.9)

    ax.set_ylabel('Values (°C or °C/cm)', fontsize=10)
    ax.set_title('Cross-Model Calculus Comparison\n(Peak Temp, Area Average, Edge Dissipation Rate)', fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f"Model {m}" for m in models], fontsize=9)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    # Bar label values
    ax.bar_label(rects1, padding=3, fmt='%.1f', fontsize=8)
    ax.bar_label(rects2, padding=3, fmt='%.1f', fontsize=8)
    ax.bar_label(rects3, padding=3, fmt='%.1f', fontsize=8)

    fig.tight_layout()
    return fig


def plot_optimization_trajectory(model, sensor_pos, trajectory, params=None, L=4.0, grid_resolution=81):
    """
    Plot the gradient descent trajectory of the relocated heat source.
    Accepts user-specified parameters, falling back to model defaults.
    """
    merged_params = dict(model.default_params)
    if params:
        merged_params.update(params)
    xs = np.linspace(0.0, L, grid_resolution)
    ys = np.linspace(0.0, L, grid_resolution)
    X, Y = np.meshgrid(xs, ys)
    T_grid = model.evaluate_T(X, Y, merged_params)

    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=100)

    im = ax.imshow(
        T_grid, origin='lower', extent=[0.0, L, 0.0, L],
        cmap='inferno', vmin=GLOBAL_VMIN, vmax=GLOBAL_VMAX, aspect='equal'
    )

    # Plot sensor location
    ax.plot(sensor_pos[0], sensor_pos[1], marker='s', color='#33b5e5', markersize=11, label='Sensitive Sensor')

    # Plot trajectory
    traj_x = [p[0] for p in trajectory]
    traj_y = [p[1] for p in trajectory]
    ax.plot(traj_x, traj_y, color='lime', linestyle='--', linewidth=2.0, label='Descent Path (-∇T)')
    ax.plot(traj_x[0], traj_y[0], marker='o', color='orange', markersize=9, label='Initial Source')
    ax.plot(traj_x[-1], traj_y[-1], marker='*', color='yellow', markersize=14, markeredgecolor='green', label='Final Relocated Source')

    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_xlabel("x (cm)", fontsize=10)
    ax.set_ylabel("y (cm)", fontsize=10)
    ax.set_title("Gradient Descent: Heat Source Relocation", fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8, framealpha=0.85)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Temperature (°C)", fontsize=9)
    fig.tight_layout()
    return fig


def plot_lagrange_rail(model, a, b, c, optimal_pt, params=None, L=4.0, grid_resolution=81):
    """
    Plot the linear mounting rail ax + by = c and mark the hottest point.
    Accepts user-specified parameters, falling back to model defaults.
    Properly handles both standard (b != 0) and vertical (b == 0) rails.
    """
    merged_params = dict(model.default_params)
    if params:
        merged_params.update(params)
    xs = np.linspace(0.0, L, grid_resolution)
    ys = np.linspace(0.0, L, grid_resolution)
    X, Y = np.meshgrid(xs, ys)
    T_grid = model.evaluate_T(X, Y, merged_params)

    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=100)

    im = ax.imshow(
        T_grid, origin='lower', extent=[0.0, L, 0.0, L],
        cmap='inferno', vmin=GLOBAL_VMIN, vmax=GLOBAL_VMAX, aspect='equal'
    )

    # Plot line segment
    line_x = []
    line_y = []
    if abs(b) > 1e-6:
        for xi in np.linspace(0.0, L, 100):
            yi = (c - a * xi) / b
            if 0.0 <= yi <= L:
                line_x.append(xi)
                line_y.append(yi)
    else:
        # Vertical rail: a * x = c => x = c / a
        if abs(a) > 1e-6:
            x_val = c / a
            if 0.0 <= x_val <= L:
                line_x = [x_val, x_val]
                line_y = [0.0, L]

    if line_x:
        ax.plot(line_x, line_y, color='white', linestyle='-', linewidth=2.5, label=f'Rail: {a:.1f}x + {b:.1f}y = {c:.1f}')

    # Mark optimal point
    ax.plot(
        optimal_pt['x'], optimal_pt['y'], marker='D', color='cyan',
        markersize=10, markeredgecolor='black', label=f"Hottest Rail Point ({optimal_pt['T']:.1f}°C)"
    )

    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_xlabel("x (cm)", fontsize=10)
    ax.set_ylabel("y (cm)", fontsize=10)
    ax.set_title(f"Lagrange Multipliers Constrained Rail Extrema", fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8, framealpha=0.85)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Temperature (°C)", fontsize=9)
    fig.tight_layout()
    return fig
