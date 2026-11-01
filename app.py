# ==============================================================================
# CalSymPy (Team 4, Delta-T) — app.py
#
# Plain-English Summary:
# Main Gradio application for CalSymPy: an interactive analytical multivariable
# calculus tool for first-year engineering students (MAT 112).
#
# UI Structure:
# - Left Sidebar:
#   * Model selector (Models A, B, C, C2, D)
#   * Operating Scenario Presets (Idle: LOW, Normal: MODERATE, Heavy: HIGH)
#   * Parameter sliders (T0 from 10 to 100, T_edge from 15 to 50, s, cx, cy, L)
#   * Material conductivity selector (FR-4 PCB vs Copper Plate)
#   * Interactive point lookup coordinates (x, y)
#
# - Main Tab Panel (10 Dedicated Calculus Tabs):
#   1. Overview: Heat map with shared scale (20–120 °C), contours, heat-flow arrows (-∇T), marked peak(s).
#   2. Risk: Coloured status badge, side-by-side technical and plain-English evaluations.
#   3. Calculus Checks: Hottest point analysis + Second derivative test (D-test) + Point lookup.
#   4. Compare: Bar chart + Tabular dataframe comparing peak, area average, and edge gradient across all models.
#   5. Heat Load: Exact continuous average (scipy dblquad) vs grid mean, and stored thermal energy (J).
#   6. Heat Flow: Heat flux streamlines (F = -k ∇T) and vector divergence (div F = -k ∇²T, sources vs sinks).
#   7. Optimiser: 2D Gradient Descent for heat source relocation + Lagrange Multipliers for linear mounting rails.
#   8. Self-Test: Live verification of theoretical KNOWN VALUES evaluated at factory defaults.
#   9. Benchmark: Live wall-clock stopwatch comparing pure SymPy substitution vs lambdified NumPy execution.
#   10. Export: One-click export generating downloadable text and CSV reports.
#
# Hard Constraints:
# - MAT 112 syllabus only (no PDEs, no time stepping).
# - Pure built-in Gradio components (no custom HTML, CSS, or JavaScript).
# - Matplotlib figures returned to gr.Plot and closed immediately.
# ==============================================================================

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gradio as gr
import pandas as pd
import numpy as np

from models import MODELS, get_model
from calculus import classify_critical_point
from features import (
    find_hottest_points,
    point_lookup,
    compute_model_comparison,
    compute_thermal_load,
    run_gradient_descent_optimization,
    solve_lagrange_rail_constraint,
)
from risk import classify_risk
from selftest import run_all_self_tests
from benchmark import run_benchmark
from report import generate_text_report, generate_csv_report
from plots import (
    plot_overview,
    plot_heat_flux_streamlines,
    plot_flux_divergence,
    plot_model_comparison,
    plot_optimization_trajectory,
    plot_lagrange_rail,
)


MATERIALS = {
    "FR-4 PCB (k = 0.29 W/(m·K))": {"k": 0.29, "key": "FR-4"},
    "Copper Plate (k = 385.0 W/(m·K))": {"k": 385.0, "key": "Copper"},
}


MODEL_PRESETS = {
    'A':  {'Idle': 30.0, 'Normal': 55.0, 'Heavy': 75.0},
    'B':  {'Idle': 35.0, 'Normal': 60.0, 'Heavy': 80.0},
    'C':  {'Idle': 15.0, 'Normal': 40.0, 'Heavy': 60.0},
    'C2': {'Idle': 15.0, 'Normal': 40.0, 'Heavy': 60.0},
    'D':  {'Idle': 29.0, 'Normal': 53.0, 'Heavy': 72.3},
}


def on_scenario_change(scenario_name, model_id):
    """
    Update T0 based on selected preset tailored to the specific model's baseline
    so Idle produces ~55 °C (LOW), Normal produces ~80 °C (MODERATE), and Heavy produces ~100 °C (HIGH).
    """
    presets = MODEL_PRESETS.get(model_id, MODEL_PRESETS['A'])
    if "Idle" in scenario_name:
        return presets['Idle']
    elif "Normal" in scenario_name:
        return presets['Normal']
    else:  # Heavy Load
        return presets['Heavy']


def on_model_change(model_id):
    """
    Update slider values to the selected model's factory defaults.
    """
    model = get_model(model_id)
    defaults = model.default_params
    t_edge = defaults.get('T_edge', 25.0)
    t0 = defaults.get('T0', defaults.get('T1', 60.0))
    s = defaults.get('s', defaults.get('s1', 2.0))
    cx = defaults.get('cx', defaults.get('cx1', 2.0))
    cy = defaults.get('cy', defaults.get('cy1', 2.0))
    L = defaults.get('L', 4.0)
    return t_edge, t0, s, cx, cy, L


def update_main_views(model_id, t_edge, t0, s, cx, cy, L, material_choice, lookup_x, lookup_y):
    """
    Reactive updater for Overview, Risk, Calculus Checks, Heat Load, and Heat Flow tabs.
    """
    model = get_model(model_id)
    mat_info = MATERIALS.get(material_choice, MATERIALS["FR-4 PCB (k = 0.29 W/(m·K))"])
    k = mat_info["k"]
    mat_key = mat_info["key"]

    params = {
        'T_edge': float(t_edge),
        'T0': float(t0),
        's': float(s),
        'cx': float(cx),
        'cy': float(cy),
        'L': float(L),
        # Model D dual hotspot support
        'T1': float(t0),
        's1': float(s),
        'cx1': 1.2,
        'cy1': 1.2,
        'T2': float(t0),
        's2': float(s),
        'cx2': 2.8,
        'cy2': 2.8,
    }

    # 1. Hottest point & risk
    hottest = find_hottest_points(model, params)
    max_t = hottest['max_temperature']
    p0 = hottest['peaks'][0]
    risk_info = classify_risk(max_t)

    # 2. Figures
    fig_overview = plot_overview(model, params)
    plt.close(fig_overview)

    fig_stream = plot_heat_flux_streamlines(model, params, k=k)
    plt.close(fig_stream)

    fig_div = plot_flux_divergence(model, params, k=k)
    plt.close(fig_div)

    # 3. Reports
    risk_badge = f"## {risk_info['badge']}"
    risk_plain = (
        f"### Non-Technical Stakeholder Summary (e.g. HR / Management)\n\n"
        f"> **\"{risk_info['plain_english']}\"**\n\n"
        f"- **Peak Surface Temperature**: {max_t:.1f} °C\n"
        f"- **Component Status**: Operational within {risk_info['level']} thermal limits."
    )
    risk_tech = (
        f"### Technical Engineering Thermal Analysis\n\n"
        f"> {risk_info['technical']}\n\n"
        f"- **TjMax Junction Reference**: ~95–105 °C (Commercial Silicon)\n"
        f"- **Operating Headroom Margin**: {max(0.0, 95.0 - max_t):.1f} °C below TjMax threshold."
    )

    hottest_report = (
        f"### Hottest Point Analysis & Second Derivative Test (MAT 112)\n\n"
        f"- **Maximum Plate Temperature**: **{max_t:.2f} °C**\n"
        f"- **Peak Coordinates**: ({p0['x']:.2f}, {p0['y']:.2f}) cm [{p0['boundary_note']}]\n"
        f"- **Gradient at Peak**: Tx = {p0['Tx']:.4f} °C/cm, Ty = {p0['Ty']:.4f} °C/cm\n"
        f"- **Hessian Curvatures**: Txx = {p0['Txx']:.4f}, Tyy = {p0['Tyy']:.4f}, Txy = {p0['Txy']:.4f}\n"
        f"- **Discriminant (D = Txx*Tyy - Txy²)**: **{p0['D']:.4f}**\n"
        f"- **Calculus Classification**: **{p0['classification']}**\n\n"
        f"*{hottest['summary_text']}*"
    )

    pt = point_lookup(model, float(lookup_x), float(lookup_y), params, k=k)
    lookup_report = (
        f"### Continuous Point Lookup at ({pt['x']:.3f}, {pt['y']:.3f}) cm\n\n"
        f"- **Local Temperature T(x, y)**: **{pt['T']:.2f} °C**\n"
        f"- **Gradient Vector ∇T**: <{pt['Tx']:.3f}, {pt['Ty']:.3f}> °C/cm\n"
        f"- **Gradient Magnitude |∇T|**: {pt['grad_magnitude']:.3f} °C/cm\n"
        f"- **Heat Flux Vector (Fourier's Law: F = -k ∇T)**: <{pt['flux_x']:.3f}, {pt['flux_y']:.3f}> W/m²\n"
        f"- **Flux Magnitude |F|**: {pt['flux_magnitude']:.3f} W/m²\n"
        f"- **Laplacian ∇²T (Txx + Tyy)**: {pt['laplacian']:.3f}\n\n"
        f"*{pt['summary_text']}*"
    )

    # 4. Thermal load
    load = compute_thermal_load(model, params, material_key=mat_key, T_ambient=25.0)
    load_report = (
        f"### Double Integral Thermal Energy Analysis (scipy.integrate.dblquad)\n\n"
        f"- **Plate Area**: {load['area_cm2']:.1f} cm² ({load['area_m2']:.6f} m²)\n"
        f"- **Exact Continuous Average Temperature (scipy.integrate.dblquad)**: **{load['exact_average']:.2f} °C**  \n"
        f"  *Evaluated via $T_{{\\text{{avg}}}} = \\frac{{1}}{{\\text{{Area}}}} \\iint_R T(x, y)\\,dA$*\n"
        f"- **Discrete Grid Mean (81x81)**: {load['grid_average']:.2f} °C\n"
        f"- **Trapezoid-Rule Grid Average (np.trapezoid)**: **{load['trapz_average']:.2f} °C**\n\n"
        f"**Explanation of the gap**:\n"
        f"The plain mean counts the cooler edge points as full cells, while integration and the trapezoid rule count them as half cells.\n\n"
        f"- **Selected Material**: {load['material_name']}\n"
        f"- **Density ρ**: {load['rho']} kg/m³ | **Thickness**: {load['thickness_mm']:.1f} mm\n"
        f"- **Specific Heat Capacity cp**: {load['cp']} J/(kg·K) " + ("*(approximate, typical range 1000–1200)*" if load['cp_approx'] else "") + "\n"
        f"- **Stored Thermal Energy relative to 25.0 °C ambient**: **{load['stored_energy_joules']:.2f} Joules**\n\n"
        f"*{load['summary_text']}*"
    )

    return (
        fig_overview,
        risk_badge, risk_plain, risk_tech,
        hottest_report, lookup_report,
        load_report,
        fig_stream, fig_div,
    )


def update_comparison_tab():
    """Generate model comparison dataframe and bar chart."""
    records = compute_model_comparison()
    df = pd.DataFrame(records)
    fig_comp = plot_model_comparison(df)
    plt.close(fig_comp)
    return fig_comp, df


def run_gradient_descent_action(sensor_x, sensor_y, init_cx, init_cy, step_size):
    """Execute gradient descent source relocation and plot path."""
    model_a = get_model('A')
    res = run_gradient_descent_optimization(
        model=model_a,
        sensor_pos=(float(sensor_x), float(sensor_y)),
        init_source=(float(init_cx), float(init_cy)),
        margin=0.3,
        step_size=float(step_size),
        max_iters=50,
    )
    fig_gd = plot_optimization_trajectory(model_a, res['sensor_pos'], res['trajectory'])
    plt.close(fig_gd)
    text = (
        f"### Gradient Descent Results\n\n"
        f"- **Sensor Position**: ({sensor_x:.2f}, {sensor_y:.2f}) cm\n"
        f"- **Initial Source Position**: ({init_cx:.2f}, {init_cy:.2f}) cm -> Initial Temp: **{res['initial_sensor_temp']:.2f} °C**\n"
        f"- **Relocated Source Position**: ({res['final_source'][0]:.2f}, {res['final_source'][1]:.2f}) cm -> Final Temp: **{res['final_sensor_temp']:.2f} °C**\n"
        f"- **Net Component Cooling Achieved**: **{res['cooling_achieved']:.2f} °C** ({res['steps_taken']} descent steps along $-\\nabla T$)\n\n"
        f"*{res['summary_text']}*"
    )
    return fig_gd, text


def run_lagrange_action(rail_a, rail_b, rail_c):
    """Solve constrained extrema along rail ax + by = c and plot."""
    model_a = get_model('A')
    res = solve_lagrange_rail_constraint(
        model=model_a,
        a=float(rail_a),
        b=float(rail_b),
        c=float(rail_c),
    )
    fig_lm = plot_lagrange_rail(model_a, float(rail_a), float(rail_b), float(rail_c), res['best_analytical'])
    plt.close(fig_lm)
    text = (
        f"### Lagrange Multipliers Rail Constrained Extrema\n\n"
        f"- **Rail Equation**: ${rail_a:.1f}x + {rail_b:.1f}y = {rail_c:.1f}$\n"
        f"- **Hottest Point on Rail (Analytical SymPy)**: ({res['best_analytical']['x']:.2f}, {res['best_analytical']['y']:.2f}) cm\n"
        f"- **Maximum Temperature along Rail**: **{res['best_analytical']['T']:.2f} °C**\n"
        f"- **1D Line Grid Search Cross-Check**: ({res['grid_best']['x']:.2f}, {res['grid_best']['y']:.2f}) cm with T = {res['grid_best']['T']:.2f} °C\n\n"
        f"*{res['summary_text']}*"
    )
    return fig_lm, text


def run_selftest_tab():
    """Run self-test suite at default parameters."""
    res = run_all_self_tests()
    df = pd.DataFrame(res['records'])
    summary = (
        f"### Self-Test Suite: {res['passed']} / {res['total']} Checks Passed "
        f"({'ALL THEORETICAL KNOWN VALUES PASSED ✅' if res['all_passed'] else 'FAILURES ❌'})\n\n"
        f"*Crucial Verification Note: The self-test panel evaluates models strictly at their "
        f"factory DEFAULT parameters, completely independent of current UI slider settings.*"
    )
    return summary, df


def run_benchmark_action(grid_n):
    """Execute live SymPy vs NumPy benchmark."""
    model_a = get_model('A')
    res = run_benchmark(model=model_a, grid_res=int(grid_n))
    text = (
        f"### Live Benchmark Execution ({res['grid_resolution']}x{res['grid_resolution']} Grid = {res['total_points']} points)\n\n"
        f"- **Pure SymPy Symbolic Substitution**: **{res['sympy_seconds']:.4f} seconds**\n"
        f"- **Vectorized Lambdified NumPy Function**: **{res['numpy_seconds']:.6f} seconds**\n"
        f"- **Speedup Factor**: **{res['speedup_ratio']:.1f}x faster**\n"
        f"- **Numerical Agreement**: Max absolute difference = {res['max_abs_diff']:.2e} (Passed: {res['values_match']})\n\n"
        f"*{res['summary_text']}*"
    )
    return text


def export_report_action(model_id, t_edge, t0, s, cx, cy, L, material_choice, format_choice):
    """Generate downloadable report file."""
    model = get_model(model_id)
    mat_info = MATERIALS.get(material_choice, MATERIALS["FR-4 PCB (k = 0.29 W/(m·K))"])
    mat_key = mat_info["key"]

    params = {
        'T_edge': float(t_edge),
        'T0': float(t0),
        's': float(s),
        'cx': float(cx),
        'cy': float(cy),
        'L': float(L),
    }

    if "CSV" in format_choice:
        file_path = generate_csv_report(model, params, material_key=mat_key)
    else:
        file_path = generate_text_report(model, params, material_key=mat_key)

    msg = f"Report successfully generated: `{os.path.basename(file_path)}`"
    return file_path, msg


def build_app():
    """Build the comprehensive Gradio application."""
    with gr.Blocks(title="CalSymPy — Flat Plate Thermal Calculus") as demo:
        gr.Markdown(
            "# CalSymPy: Flat Plate Thermal Distribution & Calculus Analysis\n"
            "**Team 4, Delta-T — MAT 112 Engineering Mathematics & Python**\n\n"
            "An analytical educational tool modeling steady-state temperature $T(x, y)$ "
            "on a flat plate ($L = 4\\text{ cm}$) using multivariable differential and integral calculus."
        )

        with gr.Row():
            # Left Sidebar: Model & Parameters
            with gr.Column(scale=1):
                gr.Markdown("### Thermal Model & Load Controls")
                model_dropdown = gr.Dropdown(
                    choices=[
                        ("Model A: Single Hotspot", "A"),
                        ("Model B: Fixed Cold Edges", "B"),
                        ("Model C: Sealed Edges", "C"),
                        ("Model C2: True Insulated Edges", "C2"),
                        ("Model D: Two Hotspots", "D"),
                    ],
                    value="A",
                    label="Thermal Model",
                )

                scenario_dropdown = gr.Dropdown(
                    choices=[
                        "Preset: Idle (LOW)",
                        "Preset: Normal Load (MODERATE)",
                        "Preset: Heavy Load (HIGH)",
                    ],
                    value="Preset: Normal Load (MODERATE)",
                    label="Operating Scenario Preset",
                )

                t_edge_slider = gr.Slider(
                    minimum=15.0, maximum=50.0, value=25.0, step=1.0,
                    label="T_edge: Baseline Edge Temperature (°C)"
                )
                t0_slider = gr.Slider(
                    minimum=10.0, maximum=100.0, value=60.0, step=1.0,
                    label="T0: Thermal Amplitude (°C)"
                )
                s_slider = gr.Slider(
                    minimum=0.5, maximum=5.0, value=2.0, step=0.1,
                    label="s: Hotspot Dispersion Parameter (cm²)"
                )
                cx_slider = gr.Slider(
                    minimum=0.5, maximum=3.5, value=2.0, step=0.1,
                    label="cx: Hotspot Center X (cm)"
                )
                cy_slider = gr.Slider(
                    minimum=0.5, maximum=3.5, value=2.0, step=0.1,
                    label="cy: Hotspot Center Y (cm)"
                )
                L_slider = gr.Slider(
                    minimum=2.0, maximum=10.0, value=4.0, step=0.5,
                    label="L: Plate Side Length (cm)"
                )

                material_dropdown = gr.Dropdown(
                    choices=list(MATERIALS.keys()),
                    value="FR-4 PCB (k = 0.29 W/(m·K))",
                    label="Plate Material Conductivity",
                )

                gr.Markdown("### Interactive Point Lookup (cm)")
                with gr.Row():
                    lookup_x = gr.Number(value=2.0, label="Lookup X")
                    lookup_y = gr.Number(value=2.0, label="Lookup Y")

            # Right Main Dashboard Tabs
            with gr.Column(scale=2):
                with gr.Tabs():
                    # Tab 1: Overview
                    with gr.Tab("Overview"):
                        overview_plot = gr.Plot(label="2D Temperature Map & Heat Flow")

                    # Tab 2: Risk
                    with gr.Tab("Risk"):
                        risk_badge_md = gr.Markdown("## 🟡 MODERATE RISK")
                        with gr.Row():
                            with gr.Column():
                                risk_plain_md = gr.Markdown()
                            with gr.Column():
                                risk_tech_md = gr.Markdown()

                    # Tab 3: Calculus Checks
                    with gr.Tab("Calculus Checks"):
                        hottest_md = gr.Markdown()
                        lookup_md = gr.Markdown()

                    # Tab 4: Compare
                    with gr.Tab("Compare"):
                        compare_btn = gr.Button("Refresh Cross-Model Comparison", variant="primary")
                        compare_plot = gr.Plot(label="Model Comparison Bar Chart")
                        compare_table = gr.Dataframe(label="Comparative Calculus Metrics")

                    # Tab 5: Heat Load
                    with gr.Tab("Heat Load"):
                        heatload_md = gr.Markdown()

                    # Tab 6: Heat Flow
                    with gr.Tab("Heat Flow"):
                        stream_plot = gr.Plot(label="Heat Flux Streamlines (F = -k ∇T)")
                        div_plot = gr.Plot(label="Heat Flux Divergence (div F = -k ∇²T)")

                    # Tab 7: Optimiser
                    with gr.Tab("Optimiser"):
                        gr.Markdown("### 1. Gradient Descent: Component Heat Minimization")
                        with gr.Row():
                            sensor_x = gr.Number(value=1.0, label="Sensor X (cm)")
                            sensor_y = gr.Number(value=1.0, label="Sensor Y (cm)")
                            init_cx = gr.Number(value=1.5, label="Initial Source X (cm)")
                            init_cy = gr.Number(value=1.5, label="Initial Source Y (cm)")
                            step_size = gr.Slider(minimum=0.01, maximum=0.2, value=0.08, step=0.01, label="Step Size (alpha)")
                        gd_btn = gr.Button("Run Gradient Descent Relocation", variant="primary")
                        gd_plot = gr.Plot(label="Descent Trajectory Map")
                        gd_md = gr.Markdown()

                        gr.Markdown("---")
                        gr.Markdown("### 2. Lagrange Multipliers: Linear Mounting Rail Extrema")
                        with gr.Row():
                            rail_a = gr.Number(value=1.0, label="Rail Coefficient a (ax + by = c)")
                            rail_b = gr.Number(value=1.0, label="Rail Coefficient b")
                            rail_c = gr.Number(value=4.0, label="Rail Constant c")
                        lm_btn = gr.Button("Solve Lagrange Extrema", variant="primary")
                        lm_plot = gr.Plot(label="Rail Extrema Map")
                        lm_md = gr.Markdown()

                    # Tab 8: Self-Test
                    with gr.Tab("Self-Test"):
                        gr.Markdown(
                            "### Automated Factory Defaults Verification Matrix\n"
                            "Click the button below to verify all theoretical KNOWN VALUES against SymPy. "
                            "This test is completely independent of the current slider positions."
                        )
                        selftest_btn = gr.Button("Run Self-Test Verification", variant="primary")
                        selftest_summary = gr.Markdown()
                        selftest_table = gr.Dataframe(label="Self-Test Verification Matrix")

                    # Tab 9: Benchmark
                    with gr.Tab("Benchmark"):
                        gr.Markdown("### Symbolic Caching Benchmark (SymPy vs Lambdified NumPy)")
                        bench_grid_slider = gr.Slider(minimum=10, maximum=40, value=25, step=5, label="Grid Resolution N (N x N points)")
                        bench_btn = gr.Button("Run Live Benchmark", variant="primary")
                        bench_md = gr.Markdown()

                    # Tab 10: Export
                    with gr.Tab("Export"):
                        gr.Markdown("### Export Analytical Calculus Report")
                        export_fmt = gr.Radio(choices=["Text Document (.txt)", "CSV Spreadsheet (.csv)"], value="Text Document (.txt)", label="Export Format")
                        export_btn = gr.Button("Generate and Download Report", variant="primary")
                        export_status = gr.Markdown()
                        export_file = gr.File(label="Download Generated Report")

        # Interactive Event Connections
        all_main_inputs = [
            model_dropdown, t_edge_slider, t0_slider, s_slider,
            cx_slider, cy_slider, L_slider, material_dropdown,
            lookup_x, lookup_y
        ]
        all_main_outputs = [
            overview_plot,
            risk_badge_md, risk_plain_md, risk_tech_md,
            hottest_md, lookup_md,
            heatload_md,
            stream_plot, div_plot,
        ]

        # Model dropdown updates sliders to model defaults
        model_dropdown.change(
            fn=on_model_change,
            inputs=[model_dropdown],
            outputs=[t_edge_slider, t0_slider, s_slider, cx_slider, cy_slider, L_slider],
        )

        # Scenario dropdown updates T0 slider
        scenario_dropdown.change(
            fn=on_scenario_change,
            inputs=[scenario_dropdown, model_dropdown],
            outputs=[t0_slider]
        )

        # Reactive dashboard update on any slider/dropdown change
        for control in all_main_inputs:
            if hasattr(control, 'change'):
                control.change(fn=update_main_views, inputs=all_main_inputs, outputs=all_main_outputs)

        # Run main dashboard once on app load
        demo.load(fn=update_main_views, inputs=all_main_inputs, outputs=all_main_outputs)

        # Tab button actions
        compare_btn.click(fn=update_comparison_tab, inputs=[], outputs=[compare_plot, compare_table])
        gd_btn.click(fn=run_gradient_descent_action, inputs=[sensor_x, sensor_y, init_cx, init_cy, step_size], outputs=[gd_plot, gd_md])
        lm_btn.click(fn=run_lagrange_action, inputs=[rail_a, rail_b, rail_c], outputs=[lm_plot, lm_md])
        selftest_btn.click(fn=run_selftest_tab, inputs=[], outputs=[selftest_summary, selftest_table])
        bench_btn.click(fn=run_benchmark_action, inputs=[bench_grid_slider], outputs=[bench_md])
        export_btn.click(
            fn=export_report_action,
            inputs=[model_dropdown, t_edge_slider, t0_slider, s_slider, cx_slider, cy_slider, L_slider, material_dropdown, export_fmt],
            outputs=[export_file, export_status]
        )

        # Footer note
        gr.Markdown(
            "---\n"
            "**CalSymPy (Team 4, Delta-T) — MAT 112 Engineering Mathematics & Python**  \n"
            "*Educational Note: This model is idealized (simple square plate, uniform isotropic material, "
            "steady-state position-only distribution, no active chip geometries or PDE time-stepping).*"
        )

    return demo


if __name__ == "__main__":
    app = build_app()
    app.launch()
