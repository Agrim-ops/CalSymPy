# calsympy.py - multivariable calculus and heat plate modeling
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sympy as sp

# --- models ---

# Calculates temperature for Model A (circular Gaussian hotspot).
# Inputs: coordinates x, y and hotspot parameters (t_edge, t0, s, cx, cy).
# Output: temperature value T in degrees C.
# Formula: T = t_edge + t0 * exp(-((x - cx)^2 + (y - cy)^2) / s).
def temp_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):  # Calculates Model A Gaussian hotspot temperature
    return t_edge + t0 * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / s)

# Computes analytical first partial derivatives Tx and Ty for Model A.
# Inputs: coordinates x, y and hotspot parameters.
# Output: tuple (Tx, Ty) representing the gradient vector.
# Uses chain rule on exp(-r^2/s) where r^2 = (x - cx)^2 + (y - cy)^2.
def grad_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):  # Computes first partial derivatives (Tx, Ty) for Model A
    # Chain rule on exp(-u): d/dx [r2/s] = 2*(x-cx)/s -> Tx = -2*T0*(x-cx)/s * exp(-r2/s)
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    factor = t0 * np.exp(-r2 / s) * (-2.0 / s)
    return factor * (x - cx), factor * (y - cy)

# Computes analytical second partial derivatives Txx, Tyy, and Txy for Model A.
# Inputs: coordinates x, y and hotspot parameters.
# Output: tuple (Txx, Tyy, Txy) for the Hessian matrix and D-test.
# Uses product rule on Tx and Ty to get second derivatives.
def hessian_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):  # Computes second partial derivatives (Txx, Tyy, Txy) for Model A
    # Product rule on Tx: d/dx [factor * (x-cx)] -> Txx = e*(4*(x-cx)^2/s^2 - 2/s)
    # Mixed partial: d/dy Tx -> Txy = e*(4*(x-cx)*(y-cy)/s^2)
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    e = t0 * np.exp(-r2 / s)
    txx = e * (4.0 * ((x - cx) ** 2) / (s ** 2) - 2.0 / s)
    tyy = e * (4.0 * ((y - cy) ** 2) / (s ** 2) - 2.0 / s)
    txy = e * (4.0 * (x - cx) * (y - cy) / (s ** 2))
    return txx, tyy, txy

# Calculates temperature for Model B (sinusoidal standing wave).
# Inputs: coordinates x, y and parameters t_edge, t0, and plate size L.
# Output: temperature value T in degrees C.
# Formula: T = t_edge + t0 * sin(pi * x / L) * sin(pi * y / L).
def temp_b(x, y, t_edge=20.0, t0=50.0, L=4.0):  # Calculates Model B sine plate temperature
    return t_edge + t0 * np.sin(np.pi * x / L) * np.sin(np.pi * y / L)

# Computes analytical first partial derivatives Tx and Ty for Model B.
# Inputs: coordinates x, y and plate parameters (t_edge, t0, L).
# Output: tuple (Tx, Ty) giving the gradient vector components.
# Uses chain rule: d/dx sin(pi*x/L) = (pi/L)*cos(pi*x/L).
def grad_b(x, y, t_edge=20.0, t0=50.0, L=4.0):  # Computes first partial derivatives (Tx, Ty) for Model B
    # Chain rule: d/dx sin(pi*x/L) = (pi/L)*cos(pi*x/L)
    u, v = np.pi * x / L, np.pi * y / L
    scale = t0 * (np.pi / L)
    return scale * np.cos(u) * np.sin(v), scale * np.sin(u) * np.cos(v)

# Computes analytical second partial derivatives Txx, Tyy, and Txy for Model B.
# Inputs: coordinates x, y and plate parameters (t_edge, t0, L).
# Output: tuple (Txx, Tyy, Txy) for curvature and discriminant D.
# Differentiates Tx and Ty with respect to x and y.
def hessian_b(x, y, t_edge=20.0, t0=50.0, L=4.0):  # Computes second partial derivatives (Txx, Tyy, Txy) for Model B
    # Second derivative: d/dx cos(pi*x/L) = -(pi/L)*sin(pi*x/L)
    u, v = np.pi * x / L, np.pi * y / L
    factor = t0 * ((np.pi / L) ** 2)
    txx = -factor * np.sin(u) * np.sin(v)
    return txx, txx, factor * np.cos(u) * np.cos(v)

# Plate object holding parameters and dispatching model formulas
class Plate:
    # Initializes the square plate instance with default dimensions and model.
    # Inputs: model name string ("A" or "B").
    # Sets default plate size L=4.0 cm and delegates to set_model().
    def __init__(self, model="A"):  # Initializes plate with default dimensions and model type
        self.L, self.s, self.cx, self.cy = 4.0, 2.0, 2.0, 2.0
        self.set_model(model)

    # Configures the active model type and restores default model parameters.
    # Inputs: model name string ("A" for hotspot, "B" for sine plate).
    # Updates plate attributes (t_edge, t0, and s, cx, cy for Model A).
    def set_model(self, model):  # Sets active model ('A' or 'B') and updates default parameters
        self.model = model
        if model == "A":
            self.t_edge, self.t0, self.s, self.cx, self.cy = 25.0, 60.0, 2.0, 2.0, 2.0
        else:
            self.t_edge, self.t0 = 20.0, 50.0

    # Evaluates plate surface temperature at the specified coordinates.
    # Inputs: x and y coordinates on the plate.
    # Output: temperature T in degrees C dispatched from the active model.
    def get_temp(self, x, y):  # Evaluates temperature at (x, y) using active model
        if self.model == "A":
            return temp_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return temp_b(x, y, self.t_edge, self.t0, self.L)

    # Evaluates the gradient vector components at given coordinates.
    # Inputs: x and y coordinates on the plate.
    # Output: tuple (Tx, Ty) dispatched from the active model.
    def get_grad(self, x, y):  # Evaluates gradient vector (Tx, Ty) at (x, y) using active model
        if self.model == "A":
            return grad_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return grad_b(x, y, self.t_edge, self.t0, self.L)

    # Evaluates second partial derivatives at given coordinates.
    # Inputs: x and y coordinates on the plate.
    # Output: tuple (Txx, Tyy, Txy) dispatched from the active model.
    def get_hessian(self, x, y):  # Evaluates second partials (Txx, Tyy, Txy) at (x, y) using active model
        if self.model == "A":
            return hessian_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return hessian_b(x, y, self.t_edge, self.t0, self.L)

# --- calculus ---

# Computes the gradient vector and total slope magnitude at a point.
# Inputs: plate object and point coordinates (x, y).
# Outputs: tuple (Tx, Ty, magnitude) where magnitude = sqrt(Tx^2 + Ty^2).
# The gradient points in the direction of steepest temperature increase.
def gradient(plate, x, y):  # Computes gradient vector and magnitude sqrt(Tx^2 + Ty^2)
    tx, ty = plate.get_grad(x, y)
    return tx, ty, np.sqrt(tx ** 2 + ty ** 2)

# Performs the second derivative test to classify surface curvature at (x, y).
# Inputs: plate object and coordinates (x, y).
# Outputs: tuple (Txx, Tyy, Txy, D, classification).
# Uses discriminant D = Txx * Tyy - Txy^2 to find peaks, valleys, or saddles.
def second_derivative_test(plate, x, y):  # Classifies critical point curvature using discriminant D = Txx*Tyy - Txy^2
    txx, tyy, txy = plate.get_hessian(x, y)
    d = txx * tyy - (txy ** 2)
    if abs(d) < 1e-6:
        return txx, tyy, txy, d, "Inconclusive"
    if d > 0 and txx < 0:
        return txx, tyy, txy, d, "Local Maximum"
    if d > 0 and txx > 0:
        return txx, tyy, txy, d, "Local Minimum"
    return txx, tyy, txy, d, "Saddle Point"

# Calculates the average plate temperature using a double integral.
# Inputs: plate object and number of subdivision steps along each axis.
# Output: average temperature in degrees C over the area [0, L] x [0, L].
# Approximates (1 / Area) * double_integral(T dA) using a 2D midpoint Riemann sum.
def average_temperature(plate, n_steps=80):  # Computes average plate temperature via 2D midpoint Riemann sum
    dx = plate.L / n_steps
    da, total = dx * dx, 0.0
    for i in range(n_steps):
        x = (i + 0.5) * dx
        for j in range(n_steps):
            total += plate.get_temp(x, (j + 0.5) * dx) * da
    return total / (plate.L * plate.L)

# Computes the tangent plane linear approximation of temperature near (a, b).
# Inputs: plate object, base point (a, b), and evaluation point (x, y).
# Output: linear approximation temperature L(x, y) in degrees C.
# Formula: L(x, y) = T(a, b) + Tx * (x - a) + Ty * (y - b).
def tangent_plane(plate, a, b, x, y):  # Computes linear approximation L(x, y) near base point (a, b)
    tx, ty = plate.get_grad(a, b)
    return plate.get_temp(a, b) + tx * (x - a) + ty * (y - b)

# Computes the second-degree Taylor polynomial approximation around (a, b).
# Inputs: plate object, base point (a, b), and evaluation point (x, y).
# Output: quadratic temperature estimate including surface curvature.
# Adds second partial derivative terms 0.5*Txx*dx^2 + Txy*dx*dy + 0.5*Tyy*dy^2.
def taylor_degree_2(plate, a, b, x, y):  # Computes quadratic Taylor polynomial approximation near (a, b)
    tx, ty = plate.get_grad(a, b)
    txx, tyy, txy = plate.get_hessian(a, b)
    dx, dy = x - a, y - b
    linear = plate.get_temp(a, b) + tx * dx + ty * dy
    return linear + 0.5 * txx * (dx ** 2) + txy * dx * dy + 0.5 * tyy * (dy ** 2)

# Simulates moving a heat-sensitive chip downhill to a cooler spot.
# Inputs: plate object, starting coordinates, step size, and step count.
# Outputs: tuple (path list, final temperature).
# Moves along the unit downhill direction (-Tx/mag, -Ty/mag) with boundary clamping.
def gradient_descent(plate, start_x, start_y, step_size=0.1, steps=40):  # Moves chip downhill along unit -grad direction
    curr_x = start_x
    curr_y = start_y
    path = [(curr_x, curr_y)]
    for _ in range(steps):
        tx, ty = plate.get_grad(curr_x, curr_y)
        mag = np.sqrt(tx ** 2 + ty ** 2)
        if mag > 0.0:
            curr_x = curr_x - step_size * (tx / mag)
            curr_y = curr_y - step_size * (ty / mag)
        curr_x = max(0.2, min(plate.L - 0.2, curr_x))
        curr_y = max(0.2, min(plate.L - 0.2, curr_y))
        path.append((curr_x, curr_y))
    return path, plate.get_temp(curr_x, curr_y)

# Searches the plate surface on a regular grid to locate the maximum temperature.
# Inputs: plate object and number of grid divisions n_grid.
# Outputs: tuple (best_x, best_y, peak_temperature).
# Scans coordinates from 0 to L with step dx = L / n_grid to find the peak.
def find_hottest_point(plate, n_grid=50):  # Scans grid to locate maximum temperature and coordinates
    best_t, best_x, best_y = -1000.0, 0.0, 0.0
    dx = plate.L / n_grid
    for i in range(n_grid + 1):
        for j in range(n_grid + 1):
            x, y = i * dx, j * dx
            t = plate.get_temp(x, y)
            if t > best_t:
                best_t, best_x, best_y = t, x, y
    return best_x, best_y, best_t

# Categorizes operational thermal risk based on peak temperature.
# Inputs: temperature value temp in degrees C.
# Output: risk category string ("Low", "Medium", or "High").
# Thresholds: Low < 70 C, Medium 70 to 90 C, High > 90 C.
def get_risk_level(temp):  # Returns thermal risk level: Low (<70 C), Medium (70-90 C), High (>90 C)
    if temp < 70.0:
        return "Low"
    if temp <= 90.0:
        return "Medium"
    return "High"

# Generates practical cooling recommendations based on peak temperature risk.
# Inputs: peak temperature value peak_temp in degrees C.
# Output: list of short recommendation strings for cooling.
# Calculates needed drop to reach 69.9 C and suggests T0, T_edge, or fan options.
def cooling_suggestions(peak_temp):  # Returns practical cooling recommendations based on peak temperature
    risk = get_risk_level(peak_temp)
    tips = []
    if risk == "Low":
        tips.append("Temperature is safe; no action needed.")
    else:
        drop = round(peak_temp - 69.9, 1)
        tips.append("Peak temperature must fall by at least " + str(drop) + " deg C to reach Low risk.")
        tips.append("Option 1: Reduce chip heating T0 by " + str(drop) + " deg C.")
        tips.append("Option 2: Cool plate edges and surroundings T_edge by " + str(drop) + " deg C.")
        if risk == "High":
            tips.append("Add a heat sink or fan to improve heat dissipation.")
            tips.append("Move heat-sensitive parts away from the hotspot using gradient descent.")
    return tips

# Finds the closest position to the start where temperature is below a limit.
# Inputs: plate object, start coordinates (start_x, start_y), limit, grid count.
# Outputs: tuple (x, y, temp, dist) or None if no safe spot exists.
# Scans inside margins [0.2, L - 0.2] for the nearest point below the threshold.
def find_best_placement(plate, start_x, start_y, limit=70.0, n_grid=60):  # Finds closest safe spot (<limit C) inside margins
    start_t = plate.get_temp(start_x, start_y)
    if start_t < limit:
        return start_x, start_y, start_t, 0.0
    best_res = None
    best_dist = 1e9
    step = (plate.L - 0.4) / n_grid
    for i in range(n_grid + 1):
        x = 0.2 + i * step
        for j in range(n_grid + 1):
            y = 0.2 + j * step
            t = plate.get_temp(x, y)
            if t < limit:
                dist = np.sqrt((x - start_x) ** 2 + (y - start_y) ** 2)
                if dist < best_dist:
                    best_dist = dist
                    best_res = (x, y, t, dist)
    return best_res

# --- plots ---

# Draws a 2D color heatmap and contour lines of the temperature distribution.
# Inputs: plate object, grid resolution n_grid, and boolean flag show.
# Output: Matplotlib Figure object displaying the heat map.
# Uses imshow with inferno colormap and overlays white contour lines.
def plot_heatmap(plate, n_grid=50, show=True):  # Generates 2D thermal heatmap with contour overlays
    xs = np.linspace(0.0, plate.L, n_grid)
    x_grid, y_grid = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(6, 5))
    im = plt.imshow(plate.get_temp(x_grid, y_grid), origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    plt.colorbar(im, label="Temperature (deg C)")
    plt.contour(x_grid, y_grid, plate.get_temp(x_grid, y_grid), colors="white", linewidths=0.5)
    plt.title("Temperature Map: Model " + plate.model)
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    plt.tight_layout()
    if show:
        plt.show()
    return fig

# Overlays the downhill gradient descent trajectory on the temperature map.
# Inputs: plate object, path coordinate list, grid resolution n_grid, and show flag.
# Output: Matplotlib Figure object with the path and start/end markers.
# Draws the background temperature surface and marks path steps from hot to cool.
def plot_descent_path(plate, path, n_grid=50, show=True, best_point=None):  # Plots downhill cooling path on thermal heatmap
    xs = np.linspace(0.0, plate.L, n_grid)
    x_grid, y_grid = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(6, 5))
    plt.imshow(plate.get_temp(x_grid, y_grid), origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    px, py = [], []
    for pt in path:
        px.append(pt[0])
        py.append(pt[1])
    plt.plot(px, py, "w--", linewidth=2, label="Descent Path")
    plt.plot(px[0], py[0], "go", markersize=8, label="Start")
    plt.plot(px[-1], py[-1], "co", markersize=8, label="End (Cooler)")
    if best_point is not None:
        plt.plot(best_point[0], best_point[1], "y*", markersize=12, label="Best Placement")
    plt.title("Gradient Descent: Chip Relocation")
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
    return fig

# --- checks ---

# Verifies hand-derived partial derivatives against SymPy for both models.
# Inputs: none.
# Outputs: none (raises AssertionError if values mismatch).
# Compares symbolic calculus with hand formulas at off-axis points.
def check_sympy():  # Verifies hand-derived partial derivatives against SymPy exact calculus
    x, y, te, t0, s, cx, cy, L = sp.symbols("x y te t0 s cx cy L", real=True)
    ta = te + t0 * sp.exp(-((x - cx) ** 2 + (y - cy) ** 2) / s)
    va = {te: 25.0, t0: 60.0, s: 2.0, cx: 2.0, cy: 2.0, x: 3.0, y: 2.5}
    assert abs(float(ta.subs(va).evalf()) - temp_a(3.0, 2.5)) < 1e-5
    assert abs(float(sp.diff(ta, x).subs(va).evalf()) - grad_a(3.0, 2.5)[0]) < 1e-5
    assert abs(float(sp.diff(ta, y).subs(va).evalf()) - grad_a(3.0, 2.5)[1]) < 1e-5
    assert abs(float(sp.diff(ta, x, 2).subs(va).evalf()) - hessian_a(3.0, 2.5)[0]) < 1e-5
    assert abs(float(sp.diff(ta, y, 2).subs(va).evalf()) - hessian_a(3.0, 2.5)[1]) < 1e-5
    assert abs(float(sp.diff(ta, x, y).subs(va).evalf()) - hessian_a(3.0, 2.5)[2]) < 1e-5
    print("Model A at (3.0, 2.5): MATCH")
    tb = te + t0 * sp.sin(sp.pi * x / L) * sp.sin(sp.pi * y / L)
    vb = {te: 20.0, t0: 50.0, L: 4.0, x: 1.0, y: 1.5}
    assert abs(float(tb.subs(vb).evalf()) - temp_b(1.0, 1.5)) < 1e-5
    assert abs(float(sp.diff(tb, x).subs(vb).evalf()) - grad_b(1.0, 1.5)[0]) < 1e-5
    assert abs(float(sp.diff(tb, y).subs(vb).evalf()) - grad_b(1.0, 1.5)[1]) < 1e-5
    assert abs(float(sp.diff(tb, x, 2).subs(vb).evalf()) - hessian_b(1.0, 1.5)[0]) < 1e-5
    assert abs(float(sp.diff(tb, y, 2).subs(vb).evalf()) - hessian_b(1.0, 1.5)[1]) < 1e-5
    assert abs(float(sp.diff(tb, x, y).subs(vb).evalf()) - hessian_b(1.0, 1.5)[2]) < 1e-5
    print("Model B at (1.0, 1.5): MATCH")

# Verifies analytical temperature models and calculus assertions.
# Inputs: none.
# Outputs: none (raises AssertionError if check fails).
# Tests peak temperatures, gradients, Hessian tests, and Taylor polynomial.
def check_plate_calculus():  # Runs unit tests asserting model values, gradients, D-test, and Taylor polynomials
    pa, pb = Plate("A"), Plate("B")
    assert abs(pa.get_temp(2.0, 2.0) - 85.0) < 1e-4
    tx, ty, mag = gradient(pa, 2.0, 2.0)
    assert abs(tx) < 1e-4 and abs(ty) < 1e-4
    txx, tyy, txy, d, classification = second_derivative_test(pa, 2.0, 2.0)
    assert abs(txx - (-60.0)) < 1e-4 and abs(tyy - (-60.0)) < 1e-4
    assert abs(txy) < 1e-4 and abs(d - 3600.0) < 1e-4 and classification == "Local Maximum"
    assert abs(pa.get_temp(3.0, 2.0) - 61.39) < 0.01
    assert abs(pb.get_temp(2.0, 2.0) - 70.0) < 1e-4
    _, _, _, _, res_b11 = second_derivative_test(pb, 1.0, 1.0)
    assert res_b11 == "Inconclusive"
    assert 45.0 < average_temperature(pa, n_steps=60) < 48.0
    assert abs(tangent_plane(pa, 2.0, 2.0, 2.05, 2.05) - 85.0) < 1e-4
    exp_tan = pa.get_temp(3.0, 2.0) + pa.get_grad(3.0, 2.0)[0] * 0.05
    assert abs(tangent_plane(pa, 3.0, 2.0, 3.05, 2.0) - exp_tan) < 1e-5
    assert abs(taylor_degree_2(pa, 2.0, 2.0, 2.1, 2.1) - pa.get_temp(2.1, 2.1)) < 0.01

# Verifies gradient descent, hottest point, risk levels, and placement search.
# Inputs: none.
# Outputs: none (raises AssertionError if check fails).
# Tests path descent, peak search, risk classification, and cooling advice.
def check_optimization():  # Runs unit tests asserting gradient descent, peak search, and cooling logic
    pa = Plate("A")
    path, final_t = gradient_descent(pa, 1.5, 1.5)
    assert final_t < pa.get_temp(1.5, 1.5)
    step1 = ((path[1][0] - path[0][0]) ** 2 + (path[1][1] - path[0][1]) ** 2) ** 0.5
    assert step1 < 0.15
    hx, hy, ht = find_hottest_point(pa, n_grid=40)
    assert abs(hx - 2.0) < 0.15 and abs(hy - 2.0) < 0.15 and abs(ht - 85.0) < 0.2
    assert get_risk_level(50.0) == "Low" and get_risk_level(75.0) == "Medium" and get_risk_level(95.0) == "High"
    assert "no action" in " ".join(cooling_suggestions(50.0)).lower()
    assert "15.1" in " ".join(cooling_suggestions(85.0))
    assert "heat sink or fan" in " ".join(cooling_suggestions(100.0)).lower()
    best_15 = find_best_placement(pa, 1.5, 1.5)
    assert best_15 is not None and best_15[2] < 70.0 and best_15[3] > 0.0
    best_03 = find_best_placement(pa, 0.3, 0.3)
    assert best_03 is not None and abs(best_03[3]) < 1e-5
    assert find_best_placement(pa, 1.5, 1.5, limit=10.0) is None

# Runs all automated checks including unit assertions and SymPy checks.
# Inputs: none.
# Outputs: none (raises AssertionError if any test fails).
# Executes assertions across models, calculus, optimization, and SymPy comparisons.
def run_checks():  # Master test runner executing calculus assertions and SymPy checks
    print("Running calculus assertions...")
    check_plate_calculus()
    check_optimization()
    print("Checking models with SymPy...")
    check_sympy()
    print("All checks passed")

# --- console ---

# Prints the numbered options menu for the interactive console.
# Inputs: none.
# Outputs: none (prints menu list to terminal).
# Displays choices 0 to 8 for all available program features.
def show_menu():  # Displays the numbered menu choices (0 to 8) in the terminal
    print("\n--- CalSymPy Menu ---")
    print("1. Model & params\n2. Heat map\n3. Point lookup\n4. Hottest point\n5. Average temp\n6. Gradient descent\n7. Save report\n8. Self-check (SymPy and asserts)\n0. Quit")

# Prompts user for a numerical parameter and validates positive bounds.
# Inputs: parameter name string and current default value.
# Output: updated float value, or current value if input is empty/invalid.
# Enforces strictly positive values for plate size L and hotspot width s.
def ask_param(name, current_val):  # Safely prompts for numeric parameter with positive bounds validation
    val = input("Enter " + name + " (current " + str(current_val) + "): ").strip()
    if val == "":
        return current_val
    try:
        num = float(val)
        if name in ["L", "s"] and num <= 0.0:
            print(name + " must be positive. Keeping " + str(current_val))
            return current_val
        return num
    except ValueError:
        print("Invalid number. Keeping " + str(current_val))
        return current_val

# Handles menu option 1 to switch thermal models and modify parameters.
# Inputs: active plate object.
# Outputs: none (modifies plate attributes in place).
# Lets user switch between Model A and Model B and update parameters.
def option_choose_model(plate):  # Console Option 1: switch model type and adjust parameters
    print("\nCurrent model is:", plate.model)
    m = input("Choose model (A: single hotspot, B: sine plate): ").strip().upper()
    if m in ["A", "B"]:
        plate.set_model(m)
        print("Model switched to:", m)
    if input("Do you want to change parameters? (y/n): ").strip().lower() == "y":
        plate.t_edge = ask_param("T_edge", plate.t_edge)
        plate.t0 = ask_param("T0", plate.t0)
        if plate.model == "A":
            plate.s = ask_param("s", plate.s)
            plate.cx = ask_param("cx", plate.cx)
            plate.cy = ask_param("cy", plate.cy)
        plate.L = ask_param("L", plate.L)

# Handles menu option 3 to look up temperature and derivatives at a point.
# Inputs: active plate object.
# Outputs: none (prints point metrics and D-test classification).
# Validates bounds (0 to L) and computes T, gradient, Hessian, and D.
def option_lookup(plate):  # Console Option 3: evaluate point temperature, gradient, and second partials
    try:
        x_in = float(input("Enter x coordinate (0 to " + str(plate.L) + "): ").strip())
        y_in = float(input("Enter y coordinate (0 to " + str(plate.L) + "): ").strip())
    except ValueError:
        print("Invalid input coordinates.")
        return
    if x_in < 0.0 or x_in > plate.L or y_in < 0.0 or y_in > plate.L:
        print("Coordinates must be between 0 and " + str(plate.L))
        return
    t = plate.get_temp(x_in, y_in)
    tx, ty, mag = gradient(plate, x_in, y_in)
    txx, tyy, txy, d, result = second_derivative_test(plate, x_in, y_in)
    print("\nResults at (" + str(x_in) + ", " + str(y_in) + "):")
    print("Temperature: " + str(round(t, 2)) + " deg C")
    print("Gradient: Tx = " + str(round(tx, 3)) + ", Ty = " + str(round(ty, 3)) + " (mag = " + str(round(mag, 3)) + " deg C/cm)")
    print("Second partials: Txx = " + str(round(txx, 3)) + ", Tyy = " + str(round(tyy, 3)) + ", Txy = " + str(round(txy, 3)))
    if mag > 0.01:
        print("Discriminant D: " + str(round(d, 2)))
        print("Not a critical point (the gradient is not zero), so the second derivative test does not apply here.")
    else:
        print("Discriminant D: " + str(round(d, 2)) + " (" + result + ")")

# Handles menu option 4 to find the peak temperature and cooling suggestions.
# Inputs: active plate object.
# Outputs: none (prints peak coordinates, risk level, and suggestions).
# Uses grid search to find the hotspot and outputs rules-of-thumb advice.
def option_hottest(plate):  # Console Option 4: find hottest point, risk level, and cooling suggestions
    print("\nSearching grid for hottest point...")
    hx, hy, ht = find_hottest_point(plate, n_grid=60)
    print("Hottest point is at x = " + str(round(hx, 2)) + " cm, y = " + str(round(hy, 2)) + " cm")
    print("Peak temperature: " + str(round(ht, 2)) + " deg C (" + get_risk_level(ht) + " risk)")
    print("\nCooling suggestions:")
    for tip in cooling_suggestions(ht):
        print("- " + tip)
    print("These are simple rules of thumb, not engineering advice.")

# Handles menu option 5 to calculate average plate temperature.
# Inputs: active plate object.
# Outputs: none (prints estimated average temperature).
# Evaluates a 2D midpoint Riemann sum over [0, L] x [0, L].
def option_average(plate):  # Console Option 5: calculate average plate temperature via Riemann sum
    print("\nCalculating double integral Riemann sum...")
    avg = average_temperature(plate, n_steps=80)
    print("Average plate temperature: " + str(round(avg, 2)) + " deg C")

# Handles menu option 6 to simulate downhill chip cooling relocation.
# Inputs: active plate object.
# Outputs: none (prints trajectory and optionally plots path).
# Compares unit-step gradient descent against the closest safe placement.
def option_descent(plate):  # Console Option 6: simulate chip relocation via gradient descent and best placement
    try:
        val_x = input("Enter initial chip x (default 1.5): ").strip()
        val_y = input("Enter initial chip y (default 1.5): ").strip()
        sx = 1.5 if val_x == "" else float(val_x)
        sy = 1.5 if val_y == "" else float(val_y)
    except ValueError:
        print("Invalid input coordinates.")
        return
    if sx < 0.0 or sx > plate.L or sy < 0.0 or sy > plate.L:
        print("Coordinates must be between 0 and " + str(plate.L))
        return
    start_t = plate.get_temp(sx, sy)
    path, final_t = gradient_descent(plate, sx, sy)
    best = find_best_placement(plate, sx, sy)
    print("\nInitial at (" + str(sx) + ", " + str(sy) + "): " + str(round(start_t, 2)) + " deg C")
    print("Gradient descent end: (" + str(round(path[-1][0], 2)) + ", " + str(round(path[-1][1], 2)) + ") at " + str(round(final_t, 2)) + " deg C")
    if best is not None:
        print("Best placement (< 70 C): (" + str(round(best[0], 2)) + ", " + str(round(best[1], 2)) + ") at " + str(round(best[2], 2)) + " deg C (moved " + str(round(best[3], 2)) + " cm)")
    else:
        print("Best placement (< 70 C): No safe position found on the plate.")
    if input("Show descent path plot? (y/n): ").strip().lower() == "y":
        b_pt = (best[0], best[1]) if best else None
        plot_descent_path(plate, path, best_point=b_pt)

# Handles menu option 7 to export summary plate metrics to a file.
# Inputs: active plate object.
# Outputs: none (writes a CSV or text file to local disk).
# Exports peak coordinates, risk level, and average temperature with error handling.
def option_save_report(plate):  # Console Option 7: export plate metrics to CSV or text file
    hx, hy, ht = find_hottest_point(plate, n_grid=50)
    avg_t = average_temperature(plate, n_steps=60)
    metrics = ["Model", "Peak_X", "Peak_Y", "Peak_Temp", "Risk_Level", "Average_Temp"]
    values = [plate.model, round(hx, 2), round(hy, 2), round(ht, 2), get_risk_level(ht), round(avg_t, 2)]
    fmt = input("Save format (1 for .csv, 2 for .txt): ").strip()
    filename = "report_" + plate.model + (".csv" if fmt == "1" else ".txt")
    try:
        if fmt == "1":
            pd.DataFrame({"Metric": metrics, "Value": values}).to_csv(filename, index=False)
        else:
            with open(filename, "w") as f:
                for i in range(len(metrics)):
                    f.write(str(metrics[i]) + ": " + str(values[i]) + "\n")
        print("Saved report to " + filename)
    except (IOError, OSError):
        print("Error: Could not save report to " + filename)

# Main execution loop displaying the menu and dispatching user choices.
# Inputs: none.
# Outputs: none (runs interactive loop until choice 0 is entered).
# Initializes a Plate object and routes commands to option functions.
def main():  # Main interactive loop running the console application until quit
    plate = Plate("A")
    print("Welcome to CalSymPy (MAT 112 Engineering Mathematics & Python)")
    choice = ""
    while choice != "0":
        show_menu()
        choice = input("Enter choice (0-8): ").strip()
        if choice == "1": option_choose_model(plate)
        elif choice == "2": plot_heatmap(plate)
        elif choice == "3": option_lookup(plate)
        elif choice == "4": option_hottest(plate)
        elif choice == "5": option_average(plate)
        elif choice == "6": option_descent(plate)
        elif choice == "7": option_save_report(plate)
        elif choice == "8": run_checks()
        elif choice != "0": print("Invalid option. Please choose 0 to 8.")
    print("Exiting CalSymPy. Goodbye!")

if __name__ == "__main__":
    main()
