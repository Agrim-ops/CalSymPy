# calsympy.py - heat distribution on a square plate (calculations only)
import numpy as np


class Plate:
    # Square plate [0, L] x [0, L]. Model A = one hotspot, Model B = sine plate.
    def __init__(self, model="A", t_edge=None, t0=None, s=2.0, cx=2.0, cy=2.0, L=4.0):
        self.model, self.s, self.cx, self.cy, self.L = model, s, cx, cy, L
        self.t_edge = t_edge if t_edge is not None else (25.0 if model == "A" else 20.0)
        self.t0 = t0 if t0 is not None else (60.0 if model == "A" else 50.0)

    # Temperature T(x, y). A: T_edge + T0*exp(-r^2/s). B: T_edge + T0*sin(pi x/L)*sin(pi y/L).
    def temp(self, x, y):
        if self.model == "A":
            return self.t_edge + self.t0 * np.exp(-((x - self.cx) ** 2 + (y - self.cy) ** 2) / self.s)
        k = np.pi / self.L
        return self.t_edge + self.t0 * np.sin(k * x) * np.sin(k * y)

    # First partials (Tx, Ty), worked out by hand with the chain rule.
    def grad(self, x, y):
        if self.model == "A":
            e = (self.temp(x, y) - self.t_edge) * (-2.0 / self.s)  # temp - t_edge = T0*exp(-r^2/s)
            return e * (x - self.cx), e * (y - self.cy)
        k = np.pi / self.L
        return self.t0 * k * np.cos(k * x) * np.sin(k * y), self.t0 * k * np.sin(k * x) * np.cos(k * y)

    # Second partials (Txx, Tyy, Txy), worked out by hand with the product rule.
    def hessian(self, x, y):
        if self.model == "A":
            e, dx, dy, s = self.temp(x, y) - self.t_edge, x - self.cx, y - self.cy, self.s
            return e * (4 * dx ** 2 / s ** 2 - 2 / s), e * (4 * dy ** 2 / s ** 2 - 2 / s), e * 4 * dx * dy / s ** 2
        k = np.pi / self.L
        txx = -self.t0 * k ** 2 * np.sin(k * x) * np.sin(k * y)
        return txx, txx, self.t0 * k ** 2 * np.cos(k * x) * np.cos(k * y)


# Gradient (Tx, Ty) and its size |grad T| = sqrt(Tx^2 + Ty^2). It points to the steepest rise.
def gradient(plate, x, y):
    tx, ty = plate.grad(x, y)
    return tx, ty, np.sqrt(tx ** 2 + ty ** 2)


# Second derivative test with D = Txx*Tyy - Txy^2 (meant for points where the gradient is 0).
def second_derivative_test(plate, x, y):
    txx, tyy, txy = plate.hessian(x, y)
    d = txx * tyy - txy ** 2
    if abs(d) < 1e-6:
        return d, "Inconclusive"
    if d < 0:
        return d, "Saddle Point"
    return d, "Local Maximum" if txx < 0 else "Local Minimum"


# Average temperature = (1/Area) * double integral of T, using a midpoint Riemann sum.
def average_temperature(plate, n=80):
    dx, total = plate.L / n, 0.0
    for i in range(n):
        for j in range(n):
            total += plate.temp((i + 0.5) * dx, (j + 0.5) * dx) * dx * dx
    return total / plate.L ** 2


# Tangent plane at (a, b): T + Tx*(x-a) + Ty*(y-b). Taylor 2 adds the curvature terms.
def tangent_plane(plate, a, b, x, y):
    tx, ty = plate.grad(a, b)
    return plate.temp(a, b) + tx * (x - a) + ty * (y - b)


def taylor_degree_2(plate, a, b, x, y):
    txx, tyy, txy = plate.hessian(a, b)
    dx, dy = x - a, y - b
    return tangent_plane(plate, a, b, x, y) + 0.5 * txx * dx ** 2 + txy * dx * dy + 0.5 * tyy * dy ** 2


# Gradient descent: move the chip downhill (along -grad T) in steps of 0.1 cm, staying on the plate.
def gradient_descent(plate, x, y, step=0.1, steps=40):
    path = [(x, y)]
    for _ in range(steps):
        tx, ty, mag = gradient(plate, x, y)
        if mag > 0:
            x, y = x - step * tx / mag, y - step * ty / mag
        x, y = max(0.2, min(plate.L - 0.2, x)), max(0.2, min(plate.L - 0.2, y))
        path.append((x, y))
    return path, plate.temp(x, y)


# Hottest point: check every point of an n x n grid and keep the highest temperature.
def find_hottest_point(plate, n=50):
    best = (0.0, 0.0, -1000.0)
    for i in range(n + 1):
        for j in range(n + 1):
            x, y = i * plate.L / n, j * plate.L / n
            if plate.temp(x, y) > best[2]:
                best = (x, y, plate.temp(x, y))
    return best


# Risk level from the peak temperature. The limits 70 and 90 are our own rule of thumb.
def get_risk_level(t):
    return "Low" if t < 70 else ("Medium" if t <= 90 else "High")


# Simple cooling advice: how many degrees the peak must fall to get below 70 C.
def cooling_suggestions(peak):
    if peak < 70:
        return ["Temperature is safe; no action needed."]
    drop = round(peak - 69.9, 1)
    tips = ["Peak must fall by " + str(drop) + " C to reach Low risk.",
            "Option 1: reduce the chip heating T0 by " + str(drop) + " C.",
            "Option 2: cool the plate edges (T_edge) by " + str(drop) + " C."]
    if peak > 90:
        tips.append("Add a heat sink or fan, or move heat-sensitive parts away from the hotspot.")
    return tips


# Best placement: the closest point to the start where the temperature is below the limit.
def find_best_placement(plate, x0, y0, limit=70.0, n=60):
    if plate.temp(x0, y0) < limit:
        return x0, y0, plate.temp(x0, y0), 0.0
    best, step = None, (plate.L - 0.4) / n
    for i in range(n + 1):
        for j in range(n + 1):
            x, y = 0.2 + i * step, 0.2 + j * step
            dist = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
            if plate.temp(x, y) < limit and (best is None or dist < best[3]):
                best = (x, y, plate.temp(x, y), dist)
    return best


if __name__ == "__main__":
    a = Plate("A")
    hx, hy, ht = find_hottest_point(a)
    print("Hottest point:", round(hx, 2), round(hy, 2), "at", round(ht, 2), "C -", get_risk_level(ht), "risk")
    print("Average temperature:", round(average_temperature(a), 2), "C")
    d, kind = second_derivative_test(a, 2, 2)
    print("At (2, 2): D =", round(d, 1), "->", kind)
    path, end_t = gradient_descent(a, 1.5, 1.5)
    print("Chip from (1.5, 1.5): ends at", [round(v, 2) for v in path[-1]], "at", round(end_t, 2), "C")
