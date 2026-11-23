# app.py - CalSymPy: heat distribution on a square plate (calculations + Streamlit page)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


# ---------- Part 1: the plate models (SymPy finds the derivatives) ----------
# SymPy does the algebra: it differentiates T(x, y) and turns each result into a fast function.
X, Y, TE, T0, S, CX, CY, SIDE = sp.symbols("x y t_edge t0 s cx cy L")
MODEL_A = TE + T0 * sp.exp(-((X - CX) ** 2 + (Y - CY) ** 2) / S)
MODEL_B = TE + T0 * sp.sin(sp.pi * X / SIDE) * sp.sin(sp.pi * Y / SIDE)


# Returns [T, Tx, Ty, Txx, Tyy, Txy] as functions of (x, y, t_edge, t0, s, cx, cy, L).
def compile_model(T):
    parts = [T, sp.diff(T, X), sp.diff(T, Y), sp.diff(T, X, 2), sp.diff(T, Y, 2), sp.diff(T, X, Y)]
    return [sp.lambdify((X, Y, TE, T0, S, CX, CY, SIDE), p, "numpy") for p in parts]


# Compile once and remember it, so SymPy does not redo the algebra on every click.
if "funcs" not in st.session_state:
    st.session_state["funcs"] = {"A": compile_model(MODEL_A), "B": compile_model(MODEL_B)}


class Plate:
    # Square plate [0, L] x [0, L]. Model A = one hotspot, Model B = sine plate.
    def __init__(self, model="A", t_edge=None, t0=None, s=2.0, cx=2.0, cy=2.0, L=4.0):
        self.model, self.s, self.cx, self.cy, self.L = model, s, cx, cy, L
        self.t_edge = t_edge if t_edge is not None else (25.0 if model == "A" else 20.0)
        self.t0 = t0 if t0 is not None else (60.0 if model == "A" else 50.0)
        self.f = st.session_state["funcs"][model]

    # Temperature T(x, y).
    def temp(self, x, y):
        return self.f[0](x, y, self.t_edge, self.t0, self.s, self.cx, self.cy, self.L)

    # First partials (Tx, Ty).
    def grad(self, x, y):
        a = (x, y, self.t_edge, self.t0, self.s, self.cx, self.cy, self.L)
        return self.f[1](*a), self.f[2](*a)

    # Second partials (Txx, Tyy, Txy).
    def hessian(self, x, y):
        a = (x, y, self.t_edge, self.t0, self.s, self.cx, self.cy, self.L)
        return self.f[3](*a), self.f[4](*a), self.f[5](*a)


# ---------- Part 2: calculus functions ----------
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


# ---------- Part 3: the web page ----------
# Heat map of the plate. If a path is given, draw it too (start, end and best placement).
def draw_map(plate, path=None, best=None):
    xs = np.linspace(0, plate.L, 60)
    gx, gy = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(6, 5))
    plt.imshow(plate.temp(gx, gy), origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    plt.colorbar(label="Temperature (C)")
    if path:
        plt.plot([p[0] for p in path], [p[1] for p in path], "w--", label="Descent path")
        plt.plot(*path[0], "go", label="Start")
        plt.plot(*path[-1], "co", label="End")
        if best:
            plt.plot(best[0], best[1], "y*", markersize=12, label="Best placement")
        plt.legend()
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    st.pyplot(fig)
    plt.close(fig)


st.title("CalSymPy - Plate Heat Map")
with st.expander("About the models"):
    st.write("Model A: one circular hotspot at (cx, cy).")
    st.latex(r"T = T_{edge} + T_0\, e^{-\frac{(x-c_x)^2+(y-c_y)^2}{s}}")
    st.write("Model B: sine plate with cold edges.")
    st.latex(r"T = T_{edge} + T_0 \sin\left(\frac{\pi x}{L}\right)\sin\left(\frac{\pi y}{L}\right)")
    st.write("These are idealised shapes we chose, not solutions of the heat equation.")

model = st.sidebar.selectbox("Model", ["A", "B"])
L = st.sidebar.slider("Plate size L (cm)", 1.0, 10.0, 4.0, 0.5)
t_edge = st.sidebar.slider("Edge temperature T_edge (C)", 0.0, 50.0, 25.0 if model == "A" else 20.0, 1.0)
t0 = st.sidebar.slider("Heating T0 (C)", 0.0, 150.0, 60.0 if model == "A" else 50.0, 1.0)
s = st.sidebar.slider("Hotspot width s", 0.1, 10.0, 2.0, 0.1) if model == "A" else 2.0
cx = st.sidebar.slider("Hotspot x", 0.0, L, min(2.0, L), 0.1) if model == "A" else 2.0
cy = st.sidebar.slider("Hotspot y", 0.0, L, min(2.0, L), 0.1) if model == "A" else 2.0
plate = Plate(model, t_edge, t0, s, cx, cy, L)

draw_map(plate)
hx, hy, ht = find_hottest_point(plate)
avg = average_temperature(plate)
st.write("Hottest point: (" + str(round(hx, 2)) + ", " + str(round(hy, 2)) + ") at " + str(round(ht, 2)) + " C, " + get_risk_level(ht) + " risk")
st.write("Average temperature: " + str(round(avg, 2)) + " C")
for tip in cooling_suggestions(ht):
    st.write("- " + tip)
st.caption("Simple rules of thumb, not engineering advice.")

st.subheader("Check a point")
px = st.number_input("x (cm)", value=2.0)
py = st.number_input("y (cm)", value=2.0)
if 0 <= px <= L and 0 <= py <= L:
    tx, ty, mag = gradient(plate, px, py)
    d, kind = second_derivative_test(plate, px, py)
    st.write("T = " + str(round(plate.temp(px, py), 2)) + " C, gradient = (" + str(round(tx, 3) + 0.0) + ", " + str(round(ty, 3) + 0.0) + "), |grad| = " + str(round(mag, 3)))
    st.write("D = " + str(round(d, 2)) + (" -> " + kind if mag < 0.01 else " (not a critical point, so the D test does not apply)"))
else:
    st.warning("That point is outside the plate.")

st.subheader("Cool down a chip")
x0 = st.number_input("Chip x (cm)", value=1.5)
y0 = st.number_input("Chip y (cm)", value=1.5)
if st.button("Move chip"):
    if 0 <= x0 <= L and 0 <= y0 <= L:
        path, end_t = gradient_descent(plate, x0, y0)
        best = find_best_placement(plate, x0, y0)
        st.write("Gradient descent ends at (" + str(round(path[-1][0], 2)) + ", " + str(round(path[-1][1], 2)) + ") at " + str(round(end_t, 2)) + " C")
        if best:
            st.write("Best placement below 70 C: (" + str(round(best[0], 2)) + ", " + str(round(best[1], 2)) + ") at " + str(round(best[2], 2)) + " C, moved " + str(round(best[3], 2)) + " cm")
        else:
            st.write("Best placement below 70 C: none on this plate")
        draw_map(plate, path, best)
    else:
        st.warning("The chip must start on the plate.")

report = pd.DataFrame({"Metric": ["Model", "Hottest x", "Hottest y", "Peak", "Risk", "Average"], "Value": [model, hx, hy, ht, get_risk_level(ht), avg]})
st.download_button("Download report (CSV)", report.to_csv(index=False), "report.csv")
