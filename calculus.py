# calculus.py - first-year calculus tools for temperature plate
import numpy as np

def gradient(plate, x, y):
    # Gradient vector and magnitude
    tx, ty = plate.get_grad(x, y)
    return tx, ty, np.sqrt(tx ** 2 + ty ** 2)

def second_derivative_test(plate, x, y):
    # Hessian determinant D = Txx*Tyy - Txy^2
    txx, tyy, txy = plate.get_hessian(x, y)
    d = txx * tyy - (txy ** 2)
    if d > 0 and txx < 0:
        result = "Local Maximum"
    elif d > 0 and txx > 0:
        result = "Local Minimum"
    elif d < 0:
        result = "Saddle Point"
    else:
        result = "Inconclusive"
    return txx, tyy, txy, d, result

def average_temperature(plate, n_steps=80):
    # Midpoint Riemann sum double integral over [0, L] x [0, L]
    dx = plate.L / n_steps
    da, total = dx * dx, 0.0
    for i in range(n_steps):
        x = (i + 0.5) * dx
        for j in range(n_steps):
            total = total + plate.get_temp(x, (j + 0.5) * dx) * da
    return total / (plate.L * plate.L)

def tangent_plane(plate, a, b, x, y):
    # Linearisation L(x, y) = T(a, b) + Tx*(x-a) + Ty*(y-b)
    tx, ty = plate.get_grad(a, b)
    return plate.get_temp(a, b) + tx * (x - a) + ty * (y - b)

def taylor_degree_2(plate, a, b, x, y):
    # Quadratic Taylor polynomial around (a, b)
    tx, ty = plate.get_grad(a, b)
    txx, tyy, txy = plate.get_hessian(a, b)
    dx, dy = x - a, y - b
    linear = plate.get_temp(a, b) + tx * dx + ty * dy
    quad = 0.5 * txx * (dx ** 2) + txy * dx * dy + 0.5 * tyy * (dy ** 2)
    return linear + quad

def gradient_descent(plate, start_x, start_y, step_size=0.08, steps=30):
    # Downhill chip relocation along negative gradient
    curr_x, curr_y = start_x, start_y
    path = [(curr_x, curr_y)]
    for step in range(steps):
        tx, ty = plate.get_grad(curr_x, curr_y)
        curr_x = max(0.2, min(plate.L - 0.2, curr_x - step_size * tx))
        curr_y = max(0.2, min(plate.L - 0.2, curr_y - step_size * ty))
        path.append((curr_x, curr_y))
    return path, plate.get_temp(curr_x, curr_y)

def find_hottest_point(plate, n_grid=50):
    # Grid search for maximum temperature
    best_t, best_x, best_y = -1000.0, 0.0, 0.0
    dx = plate.L / n_grid
    for i in range(n_grid + 1):
        x = i * dx
        for j in range(n_grid + 1):
            y = j * dx
            t = plate.get_temp(x, y)
            if t > best_t:
                best_t, best_x, best_y = t, x, y
    return best_x, best_y, best_t

def get_risk_level(temp):
    # Thermal risk level thresholds
    if temp < 70.0:
        return "Low"
    elif temp <= 90.0:
        return "Medium"
    return "High"
