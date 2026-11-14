# app.py - Streamlit web app for CalSymPy heat distribution
import streamlit as st
import pandas as pd
import models
import calculus
import plots

st.title("CalSymPy - Plate Heat Map")
st.write("Check temperatures, slopes, and cooling paths on a square plate.")

with st.expander("About the models"):
    st.write("Model A (Gaussian Hotspot): T = T_edge + T0 * exp(-((x-cx)^2 + (y-cy)^2)/s) models a circular hotspot centered at (cx, cy).")
    st.write("Model B (Sine Plate): T = T_edge + T0 * sin(pi*x/L) * sin(pi*y/L) models a standing wave pinned to T_edge at edges.")
    st.write("These formulas are idealised shapes we chose, not derived from the heat equation.")

# Sidebar model and parameter controls
st.sidebar.header("Plate Settings")
model = st.sidebar.selectbox("Choose Model", ["A", "B"])
plate = models.Plate(model)

plate.L = st.sidebar.slider("Plate size L", min_value=1.0, max_value=10.0, value=4.0, step=0.5)
plate.t_edge = st.sidebar.slider("Edge temp T_edge", min_value=0.0, max_value=50.0, value=15.0, step=1.0)
plate.t0 = st.sidebar.slider("Hotspot heat T0", min_value=0.0, max_value=150.0, value=60.0 if model == "A" else 50.0, step=1.0)
if model == "A":
    plate.s = st.sidebar.slider("Hotspot width s", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
    plate.cx = st.sidebar.slider("Hotspot center x", min_value=0.0, max_value=plate.L, value=2.0, step=0.1)
    plate.cy = st.sidebar.slider("Hotspot center y", min_value=0.0, max_value=plate.L, value=2.0, step=0.1)

# Heat map display
st.subheader("Plate Heat Map")
fig = plots.plot_heatmap(plate, show=False)
st.pyplot(fig)

# Plate summary metrics and cooling suggestions
st.subheader("Plate Summary")
hx, hy, ht = calculus.find_hottest_point(plate)
risk = calculus.get_risk_level(ht)
avg_t = calculus.average_temperature(plate)
st.write("Hottest point: (" + str(round(hx, 2)) + ", " + str(round(hy, 2)) + ") at " + str(round(ht, 2)) + " C (" + risk + " risk)")
st.write("Average plate temperature: " + str(round(avg_t, 2)) + " C")

st.subheader("Cooling Suggestions")
for tip in calculus.cooling_suggestions(ht):
    st.write("- " + tip)
st.write("These are simple rules of thumb, not engineering advice.")

# Point lookup and second derivative test
st.subheader("Check a Point")
px = st.number_input("x position (cm)", value=2.0)
py = st.number_input("y position (cm)", value=2.0)
if px < 0.0 or px > plate.L or py < 0.0 or py > plate.L:
    st.warning("That point is outside the plate (0 to " + str(plate.L) + ")!")
else:
    t = plate.get_temp(px, py)
    tx, ty, mag = calculus.gradient(plate, px, py)
    txx, tyy, txy, d, res = calculus.second_derivative_test(plate, px, py)
    st.write("Temperature: " + str(round(t, 2)) + " C")
    st.write("Gradient: Tx = " + str(round(tx, 3)) + ", Ty = " + str(round(ty, 3)) + " (slope = " + str(round(mag, 3)) + " C/cm)")
    st.write("Second partials: Txx = " + str(round(txx, 3)) + ", Tyy = " + str(round(tyy, 3)) + ", Txy = " + str(round(txy, 3)))
    st.write("Hessian D = " + str(round(d, 2)) + " (" + res + ")")

# Chip cooling via gradient descent
st.subheader("Cool Down a Chip")
cx0 = st.number_input("Start chip x (cm)", value=1.5)
cy0 = st.number_input("Start chip y (cm)", value=1.5)
if st.button("Move chip"):
    if cx0 < 0.0 or cx0 > plate.L or cy0 < 0.0 or cy0 > plate.L:
        st.warning("Chip start position is outside the plate (0 to " + str(plate.L) + ")!")
    else:
        path, final_t = calculus.gradient_descent(plate, cx0, cy0)
        st.write("New position: (" + str(round(path[-1][0], 2)) + ", " + str(round(path[-1][1], 2)) + ")")
        st.write("New temperature: " + str(round(final_t, 2)) + " C")
        fig_d = plots.plot_descent_path(plate, path, show=False)
        st.pyplot(fig_d)

# Download CSV report
metrics = ["Model", "Plate Size L", "T_edge", "T0", "Hottest X", "Hottest Y", "Peak Temp", "Risk Level", "Average Temp"]
values = [plate.model, plate.L, plate.t_edge, plate.t0, round(hx, 2), round(hy, 2), round(ht, 2), risk, round(avg_t, 2)]
df = pd.DataFrame({"Metric": metrics, "Value": values})
st.download_button("Download Report (CSV)", df.to_csv(index=False), "report_" + plate.model + ".csv", "text/csv")
