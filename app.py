# app.py - Streamlit page for CalSymPy (shows the results of calsympy.py)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from calsympy import *


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
    st.write("T = " + str(round(plate.temp(px, py), 2)) + " C, gradient = (" + str(round(tx, 3)) + ", " + str(round(ty, 3)) + "), |grad| = " + str(round(mag, 3)))
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
        st.write("Best placement below 70 C: " + (str([round(v, 2) for v in best]) if best else "none on this plate"))
        draw_map(plate, path, best)
    else:
        st.warning("The chip must start on the plate.")

report = pd.DataFrame({"Metric": ["Model", "Hottest x", "Hottest y", "Peak", "Risk", "Average"], "Value": [model, hx, hy, ht, get_risk_level(ht), avg]})
st.download_button("Download report (CSV)", report.to_csv(index=False), "report.csv")
