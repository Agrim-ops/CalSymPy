# app.py - Streamlit web app for CalSymPy heat distribution
import streamlit as st
import pandas as pd
import models
import calculus
import plots

st.title("CalSymPy - Heat Distribution")
st.write("First-year multivariable calculus tools for temperature on a square plate.")

# Sidebar model and parameter controls
st.sidebar.header("Plate Settings")
model = st.sidebar.selectbox("Choose Model", ["A", "B"])
plate = models.Plate(model)

if model == "A":
    plate.t_edge = st.sidebar.number_input("T_edge (deg C)", value=25.0)
    plate.t0 = st.sidebar.number_input("T0 (peak rise)", value=60.0)
    plate.s = max(0.1, st.sidebar.number_input("s (dispersion)", value=2.0, min_value=0.1))
    plate.cx = st.sidebar.number_input("cx (center x)", value=2.0)
    plate.cy = st.sidebar.number_input("cy (center y)", value=2.0)
    plate.L = max(1.0, st.sidebar.number_input("L (plate size)", value=4.0, min_value=1.0))
else:
    plate.t_edge = st.sidebar.number_input("T_edge (deg C)", value=20.0)
    plate.t0 = st.sidebar.number_input("T0 (peak rise)", value=50.0)
    plate.L = max(1.0, st.sidebar.number_input("L (plate size)", value=4.0, min_value=1.0))

# Heat map display
st.subheader("Temperature Heat Map")
fig = plots.plot_heatmap(plate, show=False)
st.pyplot(fig)

# Plate summary metrics
st.subheader("Plate Summary")
hx, hy, ht = calculus.find_hottest_point(plate)
risk = calculus.get_risk_level(ht)
avg_t = calculus.average_temperature(plate)
st.write("Hottest point: (" + str(round(hx, 2)) + ", " + str(round(hy, 2)) + ") at " + str(round(ht, 2)) + " deg C (" + risk + " risk)")
st.write("Average plate temperature: " + str(round(avg_t, 2)) + " deg C")

# Point lookup and second derivative test
st.subheader("Point Lookup")
px = st.number_input("x coordinate (cm)", value=2.0)
py = st.number_input("y coordinate (cm)", value=2.0)
if px < 0.0 or px > plate.L or py < 0.0 or py > plate.L:
    st.warning("Point is outside the plate (0 to " + str(plate.L) + ")!")
else:
    t = plate.get_temp(px, py)
    tx, ty, mag = calculus.gradient(plate, px, py)
    txx, tyy, txy, d, res = calculus.second_derivative_test(plate, px, py)
    st.write("Temperature: " + str(round(t, 2)) + " deg C")
    st.write("Gradient: Tx = " + str(round(tx, 3)) + ", Ty = " + str(round(ty, 3)) + " (magnitude: " + str(round(mag, 3)) + " deg C/cm)")
    st.write("Curvature: Txx = " + str(round(txx, 3)) + ", Tyy = " + str(round(tyy, 3)) + ", Txy = " + str(round(txy, 3)))
    st.write("Discriminant D = " + str(round(d, 2)) + " (" + res + ")")

# Chip cooling via gradient descent
st.subheader("Chip Cooling")
cx0 = st.number_input("Start chip x (cm)", value=1.5)
cy0 = st.number_input("Start chip y (cm)", value=1.5)
if st.button("Move chip"):
    if cx0 < 0.0 or cx0 > plate.L or cy0 < 0.0 or cy0 > plate.L:
        st.warning("Chip start position is outside the plate (0 to " + str(plate.L) + ")!")
    else:
        path, final_t = calculus.gradient_descent(plate, cx0, cy0)
        st.write("Final chip position: (" + str(round(path[-1][0], 2)) + ", " + str(round(path[-1][1], 2)) + ")")
        st.write("Final chip temperature: " + str(round(final_t, 2)) + " deg C")
        fig_d = plots.plot_descent_path(plate, path, show=False)
        st.pyplot(fig_d)

# Download CSV report
metrics = ["Model", "Plate Size L", "T_edge", "T0", "Hottest X", "Hottest Y", "Peak Temp", "Risk Level", "Average Temp"]
values = [plate.model, plate.L, plate.t_edge, plate.t0, round(hx, 2), round(hy, 2), round(ht, 2), risk, round(avg_t, 2)]
df = pd.DataFrame({"Metric": metrics, "Value": values})
st.download_button("Download Report (CSV)", df.to_csv(index=False), "report_" + plate.model + ".csv", "text/csv")
