# calculus.py - first-year calculus tools for temperature plate
import numpy as np

def gradient(plate, x, y):
    # Partial derivatives and gradient vector
    tx, ty = plate.get_grad(x, y)
    mag = np.sqrt(tx ** 2 + ty ** 2)
    return tx, ty, mag

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
    # Double integral using midpoint Riemann sum over [0, L] x [0, L]
    dx = plate.L / n_steps
    dy = plate.L / n_steps
    da = dx * dy
    total = 0.0
    for i in range(n_steps):
        x = (i + 0.5) * dx
        for j in range(n_steps):
            y = (j + 0.5) * dy
            total = total + plate.get_temp(x, y) * da
    area = plate.L * plate.L
    return total / area

def tangent_plane(plate, a, b, x, y):
    # Linearisation: L(x, y) = T(a, b) + Tx*(x-a) + Ty*(y-b)
    t_ab = plate.get_temp(a, b)
    tx, ty = plate.get_grad(a, b)
    return t_ab + tx * (x - a) + ty * (y - b)

def taylor_degree_2(plate, a, b, x, y):
    # Quadratic Taylor polynomial around (a, b)
    t_ab = plate.get_temp(a, b)
    tx, ty = plate.get_grad(a, b)
    txx, tyy, txy = plate.get_hessian(a, b)
    dx = x - a
    dy = y - b
    linear = t_ab + tx * dx + ty * dy
    quad = 0.5 * txx * (dx ** 2) + txy * dx * dy + 0.5 * tyy * (dy ** 2)
    return linear + quad

def gradient_descent(plate, start_x, start_y, step_size=0.08, steps=30):
    # Move chip away from heat source along negative gradient (-Tx, -Ty)
    curr_x = start_x
    curr_y = start_y
    path = []
    path.append((curr_x, curr_y))
    for step in range(steps):
        tx, ty = plate.get_grad(curr_x, curr_y)
        # Step in the cold direction (downhill)
        curr_x = curr_x - step_size * tx
        curr_y = curr_y - step_size * ty
        # Keep inside the physical plate margins
        if curr_x < 0.2:
            curr_x = 0.2
        if curr_x > plate.L - 0.2:
            curr_x = plate.L - 0.2
        if curr_y < 0.2:
            curr_y = 0.2
        if curr_y > plate.L - 0.2:
            curr_y = plate.L - 0.2
        path.append((curr_x, curr_y))
    final_temp = plate.get_temp(curr_x, curr_y)
    return path, final_temp

def find_hottest_point(plate, n_grid=50):
    # Search grid with two for loops to find highest temperature
    best_t = -1000.0
    best_x = 0.0
    best_y = 0.0
    dx = plate.L / n_grid
    for i in range(n_grid + 1):
        x = i * dx
        for j in range(n_grid + 1):
            y = j * dx
            t = plate.get_temp(x, y)
            if t > best_t:
                best_t = t
                best_x = x
                best_y = y
    return best_x, best_y, best_t

def get_risk_level(temp):
    # Thresholds are our own engineering choice informed by silicon limits
    if temp < 70.0:
        return "Low"
    elif temp <= 90.0:
        return "Medium"
    else:
        return "High"
