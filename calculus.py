# calculus.py - first-year calculus tools for temperature plate
import numpy as np

# Computes the gradient vector and total slope magnitude at a point.
# Inputs: plate object and point coordinates (x, y).
# Outputs: tuple (Tx, Ty, magnitude) where magnitude = sqrt(Tx^2 + Ty^2).
# The gradient points in the direction of steepest temperature increase.
def gradient(plate, x, y):
    tx, ty = plate.get_grad(x, y)
    return tx, ty, np.sqrt(tx ** 2 + ty ** 2)

# Performs the second derivative test to classify surface curvature at (x, y).
# Inputs: plate object and coordinates (x, y).
# Outputs: tuple (Txx, Tyy, Txy, D, classification).
# Uses discriminant D = Txx * Tyy - Txy^2 to find peaks, valleys, or saddles.
def second_derivative_test(plate, x, y):
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
def average_temperature(plate, n_steps=80):
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
def tangent_plane(plate, a, b, x, y):
    tx, ty = plate.get_grad(a, b)
    return plate.get_temp(a, b) + tx * (x - a) + ty * (y - b)

# Computes the second-degree Taylor polynomial approximation around (a, b).
# Inputs: plate object, base point (a, b), and evaluation point (x, y).
# Output: quadratic temperature estimate including surface curvature.
# Adds second partial derivative terms 0.5*Txx*dx^2 + Txy*dx*dy + 0.5*Tyy*dy^2.
def taylor_degree_2(plate, a, b, x, y):
    tx, ty = plate.get_grad(a, b)
    txx, tyy, txy = plate.get_hessian(a, b)
    dx, dy = x - a, y - b
    linear = plate.get_temp(a, b) + tx * dx + ty * dy
    return linear + 0.5 * txx * (dx ** 2) + txy * dx * dy + 0.5 * tyy * (dy ** 2)

# Simulates moving a heat-sensitive chip downhill to a cooler spot.
# Inputs: plate object, starting coordinates, step size, and step count.
# Outputs: tuple (path list, final temperature).
# Moves along the unit downhill direction (-Tx/mag, -Ty/mag) with boundary clamping.
def gradient_descent(plate, start_x, start_y, step_size=0.1, steps=40):
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
def find_hottest_point(plate, n_grid=50):
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
def get_risk_level(temp):
    if temp < 70.0:
        return "Low"
    if temp <= 90.0:
        return "Medium"
    return "High"

# Generates practical cooling recommendations based on peak temperature risk.
# Inputs: peak temperature value peak_temp in degrees C.
# Output: list of short recommendation strings for cooling.
# Calculates needed drop to reach 69.9 C and suggests T0, T_edge, or fan options.
def cooling_suggestions(peak_temp):
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
def find_best_placement(plate, start_x, start_y, limit=70.0, n_grid=60):
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
