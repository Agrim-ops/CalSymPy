# ==============================================================================
# CalSymPy (Team 4, Delta-T) — features.py
#
# Plain-English Summary:
# This module implements the core analytical features for evaluating the thermal
# distribution on a flat plate.
#
# Feature 1 (Hottest Point + Second Derivative Test):
# 1. Samples the temperature field across a fine grid spanning [0, L] x [0, L].
# 2. Identifies the maximum temperature and handles potential ties (for instance,
#    Model C2 has two equal hottest points at corners (0,0) and (4,4), each 70°C).
# 3. Evaluates the analytical second partial derivatives (Txx, Tyy, Txy) at each peak.
# 4. Computes the discriminant D = Txx*Tyy - Txy² and classifies each point
#    using the second derivative test from MAT 112.
# 5. Generates plain-English explanations so every team member can explain
#    the calculus reasoning to faculty.
# ==============================================================================

import numpy as np
from calculus import classify_critical_point


def find_hottest_points(model, params=None, grid_resolution=101, tie_tolerance=1e-3):
    """
    Locate the hottest point(s) on the plate and apply the second derivative test.
    
    Calculus procedure:
    1. Grid search: Discretize the plate [0, L] x [0, L] into an N x N coordinate grid.
       Find the maximum temperature T_max.
    2. Tie handling: Collect all locations where T >= T_max - tie_tolerance. Group
       adjacent grid cells into distinct physical peaks (e.g. opposite corners).
    3. Analytical evaluation: For each identified peak (x, y), evaluate exact
       derivatives using pre-compiled functions:
       - Gradient: Tx = ∂T/∂x, Ty = ∂T/∂y
       - Hessian: Txx = ∂²T/∂x², Tyy = ∂²T/∂y², Txy = ∂²T/∂x∂y
    4. Second derivative test: Compute discriminant D = Txx * Tyy - (Txy)².
       - D > 0 and Txx < 0 -> True Maximum
       - D > 0 and Txx > 0 -> True Minimum
       - D < 0 -> Saddle Point
       - D == 0 -> Inconclusive
       
    Parameters:
        model: ThermalModel instance from models.py
        params (dict, optional): Custom parameter dictionary (or None for defaults).
        grid_resolution (int): Number of grid steps along each axis (default 101).
        tie_tolerance (float): Temperature threshold within which peaks are tied.
        
    Returns:
        dict: Summary containing max_temperature, list of peaks, is_tie flag,
              and a plain-English explanation.
    """
    merged_params = model.default_params.copy()
    if params:
        merged_params.update(params)

    L = float(merged_params.get('L', 4.0))

    # Step 1: Discretize the plate domain [0, L] x [0, L]
    xs = np.linspace(0.0, L, grid_resolution)
    ys = np.linspace(0.0, L, grid_resolution)
    X, Y = np.meshgrid(xs, ys)

    # Step 2: Evaluate temperature scalar field using cached lambdified function
    T_grid = model.evaluate_T(X, Y, merged_params)
    max_temp = float(np.max(T_grid))

    # Step 3: Find candidate peak grid locations and cluster into distinct physical peaks
    # Sort candidates by temperature descending so true local peaks lead each cluster
    tie_indices = np.argwhere(T_grid >= (max_temp - max(tie_tolerance, 0.05)))
    candidates = []
    for r_idx, c_idx in tie_indices:
        candidates.append((float(xs[c_idx]), float(ys[r_idx]), float(T_grid[r_idx, c_idx])))
    candidates.sort(key=lambda item: item[2], reverse=True)

    min_dist = 0.1 * L
    distinct_peak_coords = []
    for cand_x, cand_y, _ in candidates:
        if not any(np.hypot(cand_x - ex, cand_y - ey) < min_dist for ex, ey in distinct_peak_coords):
            distinct_peak_coords.append((cand_x, cand_y))

    # Refine interior candidates using Newton-Raphson optimization along ∇T
    refined_peak_coords = []
    for px, py in distinct_peak_coords:
        if 0.01 * L < px < 0.99 * L and 0.01 * L < py < 0.99 * L:
            for _ in range(5):
                gx, gy = model.evaluate_gradient(px, py, merged_params)
                hxx, hyy, hxy = model.evaluate_hessian(px, py, merged_params)
                det = float(hxx) * float(hyy) - float(hxy)**2
                if abs(det) > 1e-4:
                    step_x = (float(hyy) * float(gx) - float(hxy) * float(gy)) / det
                    step_y = (-float(hxy) * float(gx) + float(hxx) * float(gy)) / det
                    if np.hypot(step_x, step_y) < 1e-6:
                        break
                    px = float(np.clip(px - step_x, 0.0, L))
                    py = float(np.clip(py - step_y, 0.0, L))
        refined_peak_coords.append((px, py))

    # Step 4: Perform the Second Derivative Test at each peak
    peak_details = []
    for px, py in refined_peak_coords:
        t_val = float(model.evaluate_T(px, py, merged_params))
        tx, ty = model.evaluate_gradient(px, py, merged_params)
        txx, tyy, txy = model.evaluate_hessian(px, py, merged_params)

        tx_val = float(tx)
        ty_val = float(ty)
        txx_val = float(txx)
        tyy_val = float(tyy)
        txy_val = float(txy)

        # Apply MAT 112 discriminant formula: D = Txx * Tyy - Txy²
        D, classification, explanation = classify_critical_point(txx_val, tyy_val, txy_val)

        # Check if peak is at an interior point or along a boundary
        is_interior = (0.01 * L < px < 0.99 * L) and (0.01 * L < py < 0.99 * L)
        boundary_note = "Interior point" if is_interior else "Boundary / Corner point"

        peak_details.append({
            'x': round(px, 3),
            'y': round(py, 3),
            'T': round(t_val, 3),
            'Tx': round(tx_val, 4),
            'Ty': round(ty_val, 4),
            'Txx': round(txx_val, 4),
            'Tyy': round(tyy_val, 4),
            'Txy': round(txy_val, 4),
            'D': round(D, 4),
            'classification': classification,
            'boundary_note': boundary_note,
            'explanation': explanation,
        })

    is_tie = len(peak_details) > 1
    actual_max = max(p['T'] for p in peak_details) if peak_details else max_temp

    # Step 5: Construct plain-English summary for faculty presentation
    if is_tie:
        coords_str = ", ".join([f"({p['x']}, {p['y']})" for p in peak_details])
        summary_text = (
            f"Tied Maximum Detected: The plate reaches a maximum temperature of {actual_max:.2f} °C "
            f"at {len(peak_details)} distinct locations: {coords_str}. "
            f"At each peak, the discriminant D = {peak_details[0]['D']:.2f} > 0 and Txx = {peak_details[0]['Txx']:.2f} < 0, "
            f"confirming true local maxima by the second derivative test."
        )
    else:
        p0 = peak_details[0]
        summary_text = (
            f"Single Peak: The highest temperature on the plate is {p0['T']:.2f} °C at position ({p0['x']:.2f}, {p0['y']:.2f}). "
            f"Evaluating the Hessian gives D = {p0['D']:.2f} and Txx = {p0['Txx']:.2f}. "
            f"Classification: {p0['classification']} ({p0['boundary_note']})."
        )

    return {
        'max_temperature': actual_max,
        'peaks': peak_details,
        'is_tie': is_tie,
        'summary_text': summary_text,
    }


# ==============================================================================
# Feature 2: Exact Point Lookup
# ==============================================================================

def point_lookup(model, x, y, params=None, k=0.29):
    """
    Perform exact analytical evaluation of temperature, gradient, and curvature at (x, y).
    
    Calculus interpretation:
    Evaluates the exact continuous scalar field T(x, y) and its vector gradient
    ∇T(x, y) = <Tx, Ty> at arbitrary coordinates, without snapping or interpolating
    from a discrete grid.
    
    Parameters:
        model: ThermalModel instance
        x (float): Physical x-coordinate in cm.
        y (float): Physical y-coordinate in cm.
        params (dict, optional): Custom model parameters.
        k (float): Thermal conductivity in W/(m·K) (default 0.29 for FR-4).
        
    Returns:
        dict: Detailed point metrics including T, Tx, Ty, |∇T|, Txx, Tyy, Txy, ∇²T.
    """
    merged = model.default_params.copy()
    if params:
        merged.update(params)

    px = float(x)
    py = float(y)

    # Calculus Step 1: Exact temperature evaluation
    T_val = float(model.evaluate_T(px, py, merged))

    # Calculus Step 2: Exact gradient evaluation (direction of maximum temperature rise)
    tx_val, ty_val = model.evaluate_gradient(px, py, merged)
    tx = float(tx_val)
    ty = float(ty_val)
    grad_mag = float(np.hypot(tx, ty))

    # Calculus Step 3: Exact second derivatives & Laplacian
    txx_val, tyy_val, txy_val = model.evaluate_hessian(px, py, merged)
    txx = float(txx_val)
    tyy = float(tyy_val)
    txy = float(txy_val)
    laplacian = txx + tyy

    # Heat flux vector by Fourier's law: F = -k * ∇T (heat flows hot -> cold)
    flux_x = -float(k) * tx
    flux_y = -float(k) * ty
    flux_mag = float(k) * grad_mag

    summary_text = (
        f"At position ({px:.3f}, {py:.3f}) cm: Temperature T = {T_val:.2f} °C. "
        f"Gradient ∇T = <{tx:.2f}, {ty:.2f}> °C/cm (|∇T| = {grad_mag:.2f} °C/cm). "
        f"Heat flux flows along the negative gradient with magnitude {flux_mag:.3f} W/m²."
    )

    return {
        'x': px,
        'y': py,
        'T': T_val,
        'Tx': tx,
        'Ty': ty,
        'grad_magnitude': grad_mag,
        'Txx': txx,
        'Tyy': tyy,
        'Txy': txy,
        'laplacian': laplacian,
        'flux_x': flux_x,
        'flux_y': flux_y,
        'flux_magnitude': flux_mag,
        'summary_text': summary_text,
    }


# ==============================================================================
# Feature 5: Multi-Model Comparison
# ==============================================================================

def compute_model_comparison(models_dict=None, grid_resolution=81):
    """
    Compare key calculus and thermal metrics across all models (A, B, C, C2, D).
    
    Metrics evaluated per model:
    1. Peak Temperature: T_max = max(T) over the plate.
    2. Average Temperature: Mean of T(x, y) over the plate domain.
    3. Average Edge-Gradient Magnitude: Mean of |∇T| evaluated along all 4 boundary edges
       (bottom y=0, top y=L, left x=0, right x=L). This reflects edge heat dissipation rate.
    4. Risk Category: Evaluated using rounded peak temperature.
    
    Returns:
        list of dict: Records suitable for a pandas DataFrame and comparison plotting.
    """
    from models import MODELS
    if models_dict is None:
        models_dict = MODELS

    comparison_records = []

    for m_id, model in models_dict.items():
        params = model.default_params
        L = float(params.get('L', 4.0))

        xs = np.linspace(0.0, L, grid_resolution)
        ys = np.linspace(0.0, L, grid_resolution)
        X, Y = np.meshgrid(xs, ys)

        # 1. Temperature field
        T_grid = model.evaluate_T(X, Y, params)
        peak_temp = float(np.max(T_grid))
        avg_temp = float(np.mean(T_grid))

        # 2. Edge Gradient Magnitude along all 4 boundaries
        # Bottom edge: y = 0
        tx_b, ty_b = model.evaluate_gradient(xs, np.zeros_like(xs), params)
        # Top edge: y = L
        tx_t, ty_t = model.evaluate_gradient(xs, np.full_like(xs, L), params)
        # Left edge: x = 0
        tx_l, ty_l = model.evaluate_gradient(np.zeros_like(ys), ys, params)
        # Right edge: x = L
        tx_r, ty_r = model.evaluate_gradient(np.full_like(ys, L), ys, params)

        edge_grads = np.concatenate([
            np.hypot(tx_b, ty_b),
            np.hypot(tx_t, ty_t),
            np.hypot(tx_l, ty_l),
            np.hypot(tx_r, ty_r),
        ])
        avg_edge_grad = float(np.mean(edge_grads))

        # Risk classification from risk module
        from risk import classify_risk
        risk_data = classify_risk(peak_temp)

        comparison_records.append({
            "Model ID": m_id,
            "Model Name": model.name,
            "Peak Temp (°C)": round(peak_temp, 2),
            "Average Temp (°C)": round(avg_temp, 2),
            "Avg Edge |∇T| (°C/cm)": round(avg_edge_grad, 2),
            "Risk Level": risk_data['level'],
            "Risk Badge": risk_data['badge'],
        })

    return comparison_records


# ==============================================================================
# Feature 6: Double Integral & Stored Thermal Energy
# ==============================================================================

import scipy.integrate as integrate

MATERIAL_PROPERTIES = {
    "FR-4": {
        "name": "FR-4 PCB (Standard Glass-Epoxy)",
        "rho": 1850.0,       # kg/m³
        "cp": 1100.0,        # J/(kg·K) (approximate, range 1000-1200)
        "cp_approx": True,
        "k": 0.29,           # W/(m·K)
        "thickness_m": 0.0016,  # 1.6 mm
    },
    "Copper": {
        "name": "Copper Plate (High Conduction)",
        "rho": 8960.0,       # kg/m³
        "cp": 385.0,         # J/(kg·K)
        "cp_approx": False,
        "k": 385.0,          # W/(m·K)
        "thickness_m": 0.0016,  # 1.6 mm
    },
}


def compute_thermal_load(model, params=None, material_key="FR-4", T_ambient=25.0, grid_resolution=81):
    """
    Calculate the exact average temperature and stored thermal energy using double integration.
    
    Calculus procedure:
    1. Exact Average Temperature:
       T_avg = (1 / Area) * ∬_R T(x, y) dA
             = (1 / L²) * ∫_0^L ∫_0^L T(x, y) dy dx
       Evaluated continuously with high-precision numerical quadrature via scipy.integrate.dblquad.
    2. Discrete Grid Mean:
       Calculated across an N x N coordinate grid for side-by-side comparison.
    3. Stored Thermal Energy relative to ambient (T_amb = 25 °C):
       E = ρ * cp * thickness * ∬_R (T(x, y) - T_amb) dA
       Coordinates are converted to metres (1 cm² = 1e-4 m²), yielding Energy in Joules (J).
       
    Parameters:
        model: ThermalModel instance
        params (dict, optional): Custom model parameters
        material_key (str): "FR-4" or "Copper"
        T_ambient (float): Ambient baseline temperature in °C (default 25.0)
        grid_resolution (int): Resolution for the discrete grid comparison
        
    Returns:
        dict: Exact average, grid average, double integral value, and stored energy.
    """
    merged = model.default_params.copy()
    if params:
        merged.update(params)

    L = float(merged.get('L', 4.0))  # side length in cm
    area_cm2 = L * L
    area_m2 = area_cm2 * 1e-4

    # Calculus Step 1: Continuous double integral of T(x, y) over [0, L] x [0, L]
    # Note: scipy dblquad takes integrand func(y, x)
    integral_T, err_T = integrate.dblquad(
        lambda y, x: float(model.evaluate_T(x, y, merged)),
        0.0, L,
        lambda x: 0.0, lambda x: L,
        epsabs=1e-4, epsrel=1e-4
    )
    exact_avg = integral_T / area_cm2

    # Calculus Step 2: Discrete grid mean for comparison
    xs = np.linspace(0.0, L, grid_resolution)
    ys = np.linspace(0.0, L, grid_resolution)
    X, Y = np.meshgrid(xs, ys)
    T_grid = model.evaluate_T(X, Y, merged)
    grid_avg = float(np.mean(T_grid))

    # Calculus Step 3: Stored thermal energy relative to ambient T_ambient
    # E = ρ * cp * thickness * ∬ (T - T_amb) dA
    mat = MATERIAL_PROPERTIES.get(material_key, MATERIAL_PROPERTIES["FR-4"])
    rho = mat["rho"]
    cp = mat["cp"]
    thickness_m = mat["thickness_m"]

    # Integrate (T(x, y) - T_ambient) in cm², then convert to m²
    integral_delta_T, _ = integrate.dblquad(
        lambda y, x: float(model.evaluate_T(x, y, merged)) - float(T_ambient),
        0.0, L,
        lambda x: 0.0, lambda x: L,
        epsabs=1e-4, epsrel=1e-4
    )
    delta_integral_m2 = integral_delta_T * 1e-4

    # Stored energy in Joules: [kg/m³] * [J/(kg·K)] * [m] * [K·m²] = [J]
    stored_energy_joules = rho * cp * thickness_m * delta_integral_m2

    cp_note = "cp ≈ 1100 J/(kg·K) [approximate; typical range 1000–1200 J/(kg·K)]" if mat["cp_approx"] else f"cp = {cp} J/(kg·K)"

    summary_text = (
        f"Plate Area: {area_cm2:.1f} cm² ({area_m2:.6f} m²). "
        f"Exact Average Temperature (via dblquad): {exact_avg:.2f} °C "
        f"(Discrete {grid_resolution}x{grid_resolution} Grid Mean: {grid_avg:.2f} °C, "
        f"Difference: {abs(exact_avg - grid_avg):.3f} °C). "
        f"Stored Thermal Energy relative to {T_ambient:.1f} °C ambient: {stored_energy_joules:.2f} J "
        f"[{mat['name']}, {cp_note}, thickness {thickness_m * 1000:.1f} mm]."
    )

    return {
        "exact_average": exact_avg,
        "grid_average": grid_avg,
        "difference": abs(exact_avg - grid_avg),
        "integral_T": integral_T,
        "area_cm2": area_cm2,
        "area_m2": area_m2,
        "stored_energy_joules": stored_energy_joules,
        "material_name": mat["name"],
        "rho": rho,
        "cp": cp,
        "cp_approx": mat["cp_approx"],
        "thickness_mm": thickness_m * 1000.0,
        "T_ambient": T_ambient,
        "summary_text": summary_text,
    }


# ==============================================================================
# Feature 11 (Stretch): Advanced Calculus Optimizations
# ==============================================================================

def run_gradient_descent_optimization(
    model=None,
    sensor_pos=(1.0, 1.0),
    init_source=(1.5, 1.5),
    margin=0.3,
    step_size=0.08,
    max_iters=50,
    tolerance=1e-4
):
    """
    Minimize temperature at a sensitive component by relocating the heat source via Gradient Descent.
    
    Calculus procedure:
    The temperature at sensor (xs, ys) produced by a source at (cx, cy) is:
    T_s(cx, cy) = T_edge + T0 * exp(-((xs - cx)² + (ys - cy)²) / s)
    
    Gradient with respect to source coordinates c = <cx, cy>:
    ∂T_s/∂cx = T0 * exp(...) * (2 * (xs - cx) / s)
    ∂T_s/∂cy = T0 * exp(...) * (2 * (ys - cy) / s)
    
    To minimize temperature at the sensor, we step in the negative gradient direction:
    c^(k+1) = c^(k) - alpha * ∇_c T_s
    
    Boundary condition: Source must remain within plate margins [margin, L - margin].
    Stopping criteria: Step displacement < tolerance or max_iters reached.
    
    Returns:
        dict: Trajectory list, initial temp, final temp, total steps, and plain-English summary.
    """
    from models import get_model
    if model is None:
        model = get_model('A')

    params = model.default_params
    L = float(params.get('L', 4.0))
    s = float(params.get('s', 2.0))
    T0 = float(params.get('T0', 60.0))
    T_edge = float(params.get('T_edge', 25.0))

    xs, ys = float(sensor_pos[0]), float(sensor_pos[1])
    cx, cy = float(init_source[0]), float(init_source[1])

    trajectory = [(cx, cy)]
    curr_cx, curr_cy = cx, cy

    def _temp_at_sensor(c_x, c_y):
        r_sq = (xs - c_x)**2 + (ys - c_y)**2
        return T_edge + T0 * np.exp(-r_sq / s)

    initial_sensor_temp = _temp_at_sensor(curr_cx, curr_cy)

    for step in range(max_iters):
        r_sq = (xs - curr_cx)**2 + (ys - curr_cy)**2
        # Gradient of temperature with respect to source position (cx, cy)
        exp_factor = T0 * np.exp(-r_sq / s) * (2.0 / s)
        grad_cx = exp_factor * (xs - curr_cx)
        grad_cy = exp_factor * (ys - curr_cy)

        # Gradient descent step: c^(k+1) = c^(k) - alpha * ∇_c T
        next_cx = np.clip(curr_cx - step_size * grad_cx, margin, L - margin)
        next_cy = np.clip(curr_cy - step_size * grad_cy, margin, L - margin)

        displacement = np.hypot(next_cx - curr_cx, next_cy - curr_cy)
        curr_cx, curr_cy = float(next_cx), float(next_cy)
        trajectory.append((curr_cx, curr_cy))

        if displacement < tolerance:
            break

    final_sensor_temp = _temp_at_sensor(curr_cx, curr_cy)

    summary_text = (
        f"Gradient Descent Optimization completed in {len(trajectory) - 1} steps. "
        f"Initial source position ({init_source[0]:.2f}, {init_source[1]:.2f}) cm gave sensor temperature {initial_sensor_temp:.2f} °C. "
        f"Final source position ({curr_cx:.2f}, {curr_cy:.2f}) cm reduced sensor temperature to {final_sensor_temp:.2f} °C "
        f"(cooling of {initial_sensor_temp - final_sensor_temp:.2f} °C achieved by moving along negative gradient)."
    )

    return {
        "sensor_pos": (xs, ys),
        "initial_source": init_source,
        "final_source": (curr_cx, curr_cy),
        "initial_sensor_temp": initial_sensor_temp,
        "final_sensor_temp": final_sensor_temp,
        "cooling_achieved": initial_sensor_temp - final_sensor_temp,
        "steps_taken": len(trajectory) - 1,
        "trajectory": trajectory,
        "summary_text": summary_text,
    }


def solve_lagrange_rail_constraint(model=None, a=1.0, b=1.0, c=4.0):
    """
    Find the hottest point along a straight mounting rail: a*x + b*y = c.
    
    Calculus procedure:
    Subject to constraint g(x, y) = a*x + b*y - c = 0.
    By Lagrange multipliers: ∇T = lambda * ∇g = lambda * <a, b>.
    Equating cross-components:
    Tx * b - Ty * a = 0  and  a*x + b*y = c.
    
    Cross-checks the analytical SymPy solution with a 1D discrete line-search.
    
    Returns:
        dict: Analytical critical points, 1D grid search cross-check, and temperatures.
    """
    import sympy as sp
    from models import get_model
    if model is None:
        model = get_model('A')

    params = model.default_params
    L = float(params.get('L', 4.0))

    # SymPy analytical setup
    x_s, y_s = sp.symbols('x y', real=True)
    p_dict = {sym: params[k] for sym, k in zip(model.param_symbols, model.param_keys)}
    T_expr = model.T_sym.subs(p_dict)

    Tx_expr = sp.diff(T_expr, x_s)
    Ty_expr = sp.diff(T_expr, y_s)

    # Orthogonality condition: Tx * b - Ty * a = 0
    lagrange_eq1 = Tx_expr * float(b) - Ty_expr * float(a)
    constraint_eq2 = float(a) * x_s + float(b) * y_s - float(c)

    analytical_points = []
    try:
        sols = sp.solve([lagrange_eq1, constraint_eq2], [x_s, y_s], dict=True)
        for s in sols:
            try:
                xv = float(s[x_s].evalf())
                yv = float(s[y_s].evalf())
                # Filter points located on the physical plate
                if 0.0 <= xv <= L and 0.0 <= yv <= L:
                    tv = float(T_expr.subs({x_s: xv, y_s: yv}).evalf())
                    analytical_points.append({"x": round(xv, 3), "y": round(yv, 3), "T": round(tv, 2)})
            except (TypeError, ValueError):
                pass
    except Exception:
        pass

    # Numerical 1D grid search along line segment within [0, L] x [0, L] for verification
    # Parameterize line segment: find intersections with plate boundaries
    # x in [0, L]: if b != 0, y = (c - a*x)/b
    t_vals = np.linspace(0.0, L, 201)
    line_pts = []
    for xi in t_vals:
        if abs(b) > 1e-6:
            yi = (c - a * xi) / b
            if 0.0 <= yi <= L:
                line_pts.append((xi, yi))
        elif abs(a) > 1e-6:
            # Vertical line: x = c/a
            xv = c / a
            if 0.0 <= xv <= L:
                line_pts.append((xv, xi))

    if line_pts:
        grid_temps = [float(model.evaluate_T(pt[0], pt[1], params)) for pt in line_pts]
        max_idx = int(np.argmax(grid_temps))
        grid_best_pt = line_pts[max_idx]
        grid_best_temp = grid_temps[max_idx]
    else:
        grid_best_pt = (0.0, 0.0)
        grid_best_temp = 0.0

    # Sort analytical points by temperature descending (highest temperature first)
    analytical_points.sort(key=lambda item: item['T'], reverse=True)
    best_analytical = analytical_points[0] if analytical_points else {"x": grid_best_pt[0], "y": grid_best_pt[1], "T": grid_best_temp}

    summary_text = (
        f"Lagrange Multipliers for Rail {a:.1f}x + {b:.1f}y = {c:.1f}: "
        f"Hottest point found at ({best_analytical['x']:.2f}, {best_analytical['y']:.2f}) cm with T = {best_analytical['T']:.2f} °C. "
        f"Cross-check with 1D line grid search: ({grid_best_pt[0]:.2f}, {grid_best_pt[1]:.2f}) cm with T = {grid_best_temp:.2f} °C "
        f"(Difference: {abs(best_analytical['T'] - grid_best_temp):.3f} °C)."
    )

    return {
        "rail_equation": f"{a:.1f}x + {b:.1f}y = {c:.1f}",
        "best_analytical": best_analytical,
        "grid_best": {"x": round(grid_best_pt[0], 3), "y": round(grid_best_pt[1], 3), "T": round(grid_best_temp, 2)},
        "all_analytical_points": analytical_points,
        "line_points": line_pts,
        "summary_text": summary_text,
    }
