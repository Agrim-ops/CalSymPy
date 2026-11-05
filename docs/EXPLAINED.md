# CalSymPy — Architectural & Calculus Code Explanation (EXPLAINED.md)
**Project**: CalSymPy (Team 4, Delta-T) — MAT 112 Engineering Mathematics & Python  
**Purpose**: Comprehensive guide explaining every Python file, key functions, underlying multivariable calculus theory, and where each feature surfaces in the interactive user interface.

---

## 1. `models.py` (Thermal Model Architecture & Compilation)
- **What it does**: Defines the analytical temperature distributions $T(x, y)$ for all 5 benchmark plates (Models A, B, C, C2, and D). Uses SymPy to formulate symbolic equations and perform symbolic partial differentiation once at startup, compiling formulas into high-speed vectorized NumPy functions via `sp.lambdify`.
- **Key Functions / Classes**:
  - `class ThermalModel`: Object encapsulating symbolic expressions (`T_sym`, `Tx_sym`, `Ty_sym`, `Txx_sym`, `Tyy_sym`, `Txy_sym`) and compiled numerical evaluators (`evaluate_T`, `evaluate_gradient`, `evaluate_hessian`).
  - `_build_model_A`, `_build_model_B`, `_build_model_C`, `_build_model_C2`, `_build_model_D`: Analytical mathematical formulas for each plate model.
  - `get_model(model_id)`: Registry accessor returning the requested model.
- **Calculus Idea**: 
  - Partial derivatives: $\frac{\partial T}{\partial x}$, $\frac{\partial T}{\partial y}$ (first-order spatial rates of temperature change).
  - Second partial derivatives: $\frac{\partial^2 T}{\partial x^2}$, $\frac{\partial^2 T}{\partial y^2}$, and $\frac{\partial^2 T}{\partial x \partial y}$ (surface curvature and concavity).
  - Clairaut’s Theorem: Mixed second partial derivatives commute ($T_{xy} = T_{yx}$) because all thermal models are twice continuously differentiable ($C^2$) across the plate domain.
- **Where it appears in the app**: Powers the sidebar model selection dropdown and provides the mathematical evaluations for every single tab.

---

## 2. `calculus.py` (Core Multivariable Calculus Engine)
- **What it does**: Implements pure mathematical functions for critical point testing, gradient magnitude, Hessian determinant calculation, and vector flux divergence.
- **Key Functions**:
  - `compute_gradient_magnitude(Tx, Ty)`: Computes $|\nabla T| = \sqrt{T_x^2 + T_y^2}$.
  - `compute_discriminant(Txx, Tyy, Txy)`: Calculates Hessian determinant $D = T_{xx} T_{yy} - (T_{xy})^2$.
  - `classify_critical_point(Txx, Tyy, Txy, Tx, Ty)`: Executes the Second Derivative Test ($D > 0$ with $T_{xx} < 0 \implies$ local max; $D > 0$ with $T_{xx} > 0 \implies$ local min; $D < 0 \implies$ saddle; $D = 0 \implies$ inconclusive).
  - `compute_laplacian(Txx, Tyy)`: Evaluates $\nabla^2 T = T_{xx} + T_{yy}$.
  - `compute_flux_divergence(Txx, Tyy, k)`: Computes $\operatorname{div} \mathbf{F} = -k \nabla^2 T$ scaled to $\text{W/m}^3$.
  - `is_critical_point(Tx, Ty, tolerance)`: Tests whether $|\nabla T| \approx 0$.
- **Calculus Idea**: Multivariable second derivative test, scalar Laplacian operator, vector field divergence, and Fourier's Law of thermal conduction.
- **Where it appears in the app**: Drives Tab 1 (Overview D-test classification), Tab 2 (Inspector D-test), Tab 7 (Multi-Spot D-test), and Tab 8 (Flux Divergence heatmap).

---

## 3. `features.py` (Analytical Features & Optimization Routines)
- **What it does**: Bridges multivariable calculus with engineering applications: multi-peak finding with Newton-Raphson refinement, continuous coordinate inspection, cross-model comparison, double-integral thermal load, gradient descent source relocation, and Lagrange multiplier rail extrema.
- **Key Functions**:
  - `find_hottest_points(model, params, grid_resolution, tie_tolerance)`: Locates absolute peaks, clusters tied maxima, and refines peak coordinates via 2D Newton-Raphson.
  - `point_lookup(model, px, py, params, k)`: Evaluates continuous exact $T$, $\nabla T$, Hessian, Laplacian, and flux vector $\mathbf{F} = -k\nabla T$ at any arbitrary $(x, y)$.
  - `compute_model_comparison(models_dict)`: Evaluates peak, mean, and boundary edge gradients across all 5 models.
  - `compute_thermal_load(model, params, material_key, T_ambient)`: Performs continuous double integration via `scipy.integrate.dblquad` to determine exact average temperature and stored thermal energy in Joules; also computes discrete grid mean and `np.trapezoid` average.
  - `run_gradient_descent_optimization(...)`: Moves a heat source along $-\nabla_{\mathbf{c}} T_{\text{sensor}}$ to cool a sensitive board component.
  - `solve_lagrange_rail_constraint(...)`: Solves $\nabla T = \lambda \nabla g$ along rail $ax + by = c$ analytically with SymPy and cross-checks with a 1D line search.
- **Calculus Idea**: 
  - Newton-Raphson vector root finding on $\nabla T = \mathbf{0}$.
  - Double integrals: $\iint_R T(x, y)\,dA$ and average value $\frac{1}{\text{Area}}\iint_R T\,dA$.
  - Gradient descent along the path of steepest decrease ($-\nabla T$).
  - Constrained optimization using the method of Lagrange Multipliers.
- **Where it appears in the app**: Powers Tabs 1, 2, 4, 6, 7, 8, 11 (Gradient Descent), and 12 (Lagrange Rail).

---

## 4. `risk.py` (Semiconductor Thermal Risk Assessment)
- **What it does**: Translates temperatures into standard operational risk categories informed by commercial silicon junction thermal limits ($T_{j\text{Max}} \approx 95\text{--}105\,^\circ\text{C}$).
- **Key Functions**:
  - `classify_risk(temperature)`: Rounds temperature to 1 decimal place and assigns Low ($< 70.0\,^\circ\text{C}$), Moderate ($70.0\text{--}90.0\,^\circ\text{C}$), or High ($> 90.0\,^\circ\text{C}$).
  - Returns colored risk badges (🟢, 🟡, 🔴), non-technical explanations for non-engineers, and technical engineering margins.
- **Calculus Idea**: Threshold-based scalar field classification and guardband safety analysis.
- **Where it appears in the app**: Appears prominently in the header risk badge across Tabs 1, 3 (Risk Assessment tab), 4 (Compare table), and exported reports.

---

## 5. `selftest.py` (Theoretical Known Values Verification Suite)
- **What it does**: Independently verifies all 37 theoretical benchmark values specified by course faculty at factory default parameters, isolated completely from UI sliders.
- **Key Functions**:
  - `run_all_self_tests()`: Executes all 37 verification checks across Models A, B, C, C2, and D.
- **Calculus Idea**: 
  - Verifies exact peak coordinates, critical gradients ($\nabla T = \mathbf{0}$ at peaks), negative concavity ($T_{xx} < 0$), insulated boundary derivatives ($\frac{\partial T}{\partial n} = 0$), saddle points ($D < 0$), and analytical integration benchmarks.
- **Where it appears in the app**: Powers Tab 5 (Self-Test Panel) with an automated pass/fail matrix and overall verification status.

---

## 6. `benchmark.py` (Symbolic vs Numerical Performance Benchmark)
- **What it does**: Measures real elapsed wall-clock time comparing pure SymPy analytical substitution (`expr.subs().evalf()`) against vectorized compiled NumPy execution across an $N \times N$ plate grid.
- **Key Functions**:
  - `run_benchmark(model, grid_res)`: Times both execution methods, verifies numerical agreement to within $10^{-10}$, and calculates the real-time speedup ratio.
- **Calculus Idea**: Vectorized numerical evaluation of multivariable expressions vs point-by-point algebraic graph substitution.
- **Where it appears in the app**: Powers Tab 9 (Benchmark tab), explaining to faculty why caching with `sp.lambdify` is essential for real-time interactive calculus exploration.

---

## 7. `plots.py` (Matplotlib Visualization Suite)
- **What it does**: Generates publication-quality, colorblind-safe 2D heatmaps, vector streamline plots, divergence maps, optimization trajectories, and comparative bar charts.
- **Key Functions**:
  - `plot_overview(...)`: Generates temperature surface heatmap with fixed 20–120 °C scale and marks critical points.
  - `plot_heat_flux_streamlines(...)`: Plots Fourier heat flux vectors $\mathbf{F} = -k\nabla T$ as continuous streamlines.
  - `plot_flux_divergence(...)`: Plots $\operatorname{div} \mathbf{F} = -k\nabla^2 T$ with a diverging blue-white-red colorbar.
  - `plot_model_comparison(df)`: Generates grouped bar charts comparing peak, average, and boundary edge gradients across models.
  - `plot_optimization_trajectory(...)`: Plots the heat source relocation path taken by gradient descent.
  - `plot_lagrange_rail(...)`: Draws the linear mounting rail $ax + by = c$ and highlights the hottest constrained point.
- **Calculus Idea**: Visualizing scalar fields $T(x, y)$, 2D vector fields $\nabla T$ and $\mathbf{F}$, divergence scalar fields $\nabla \cdot \mathbf{F}$, and 1D constraint curves $g(x, y) = 0$.
- **Where it appears in the app**: Provides visual figures displayed in Tabs 1, 4, 8, 11, and 12.

---

## 8. `report.py` (Exportable Documentation & Data Engine)
- **What it does**: Generates downloadable engineering reports in structured plain text and CSV formats using pandas DataFrames.
- **Key Functions**:
  - `generate_text_report(...)`: Creates a comprehensive technical report including model equations, D-test classification, risk analysis, double-integral energy calculations, and self-test audit tables.
  - `generate_csv_report(...)`: Builds a 4-column structured pandas DataFrame (`Section`, `Metric`, `Value`, `Units`) and saves it to CSV.
  - `generate_grid_csv(...)`: Computes and exports a full $41 \times 41$ coordinate mesh grid ($x, y, T, T_x, T_y$) via pandas.
- **Calculus Idea**: Tabular serialization of scalar fields, vector gradients, and integral quantities.
- **Where it appears in the app**: Powers Tab 10 (Export tab) with downloadable `.txt` and `.csv` files.

---

## 9. `app.py` (Gradio Web User Interface & Reactive State Controller)
- **What it does**: Assembles the complete interactive 10-tab application using native Gradio Blocks components. Connects UI controls (model selection, scenario presets, parameter sliders) to reactive calculus update handlers.
- **Key Functions**:
  - `on_model_change(model_id)`: Resets sliders to model factory defaults.
  - `on_scenario_change(scenario, model_id)`: Sets model load preset (Idle/Normal/Heavy) to demonstrate Low, Moderate, and High risk.
  - `update_main_views(...)`: Central event handler recalculating all active tabs simultaneously on slider movements.
  - `build_app()`: Builds the tabbed web interface.
- **Calculus Idea**: Interactive parametric exploration of multivariable functions in real time.
- **Where it appears in the app**: Main application entry point launched by `python app.py`.
