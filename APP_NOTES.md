# CalSymPy Web Application Notes (APP_NOTES.md)
**Course**: MAT 112 Engineering Mathematics & Python  
**Project**: CalSymPy v2 (Team 4, Delta-T)  
**File Covered**: `app.py` (Streamlit Web Interface)

---

## 1. What Streamlit Does on Each Rerun

Streamlit operates on an **immediate-mode reactive execution model**:
1. When the page first loads in a browser, Streamlit executes `app.py` from top to bottom (line 1 to line 74), generating all UI widgets and visualizations.
2. Whenever the user modifies **any widget** (such as switching the model dropdown, dragging a slider, or entering new coordinates), Streamlit immediately **reruns the entire script from top to bottom** with the new widget values.
3. Because the calculations in `models.py` and `calculus.py` are purely algebraic and vectorized with NumPy, the full top-to-bottom re-execution completes in a fraction of a second, providing instant visual feedback without complex event listeners or callback registrations.

---

## 2. Line-by-Line Group Explanation of `app.py`

### Lines 1–6: Imports
```python
import streamlit as st
import pandas as pd
import models
import calculus
import plots
```
- **Explanation**: Imports the Streamlit web framework as `st`, pandas for table generation, and our project modules: `models.py` for mathematical temperature models, `calculus.py` for differentiation and integration algorithms, and `plots.py` for Matplotlib figures.

### Lines 8–9: Header and Subtitle
```python
st.title("CalSymPy - Plate Heat Map")
st.write("Check temperatures, slopes, and cooling paths on a square plate.")
```
- **Explanation**: Renders the main web page title and a one-line description of the tool at the top of the browser view using simple student English.

### Lines 11–26: Sidebar Model and Parameter Sliders
```python
st.sidebar.header("Plate Settings")
model = st.sidebar.selectbox("Choose Model", ["A", "B"])
plate = models.Plate(model)

if model == "A":
    plate.L = st.sidebar.slider("Plate size L", min_value=1.0, max_value=10.0, value=4.0, step=0.5)
    plate.t_edge = st.sidebar.slider("Edge temp T_edge", min_value=0.0, max_value=50.0, value=15.0, step=1.0)
    plate.t0 = st.sidebar.slider("Hotspot heat T0", min_value=0.0, max_value=150.0, value=60.0, step=1.0)
    plate.s = st.sidebar.slider("Hotspot width s", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
    plate.cx = st.sidebar.slider("Hotspot center x", min_value=0.0, max_value=plate.L, value=2.0, step=0.1)
    plate.cy = st.sidebar.slider("Hotspot center y", min_value=0.0, max_value=plate.L, value=2.0, step=0.1)
else:
    plate.L = st.sidebar.slider("Plate size L", min_value=1.0, max_value=10.0, value=4.0, step=0.5)
    plate.t_edge = st.sidebar.slider("Edge temp T_edge", min_value=0.0, max_value=50.0, value=15.0, step=1.0)
    plate.t0 = st.sidebar.slider("Hotspot heat T0", min_value=0.0, max_value=150.0, value=50.0, step=1.0)
```
- **Explanation**: Creates controls in the left collapsible sidebar.
  - `st.sidebar.selectbox` lets the user choose between Model A (Gaussian hotspot) and Model B (sine plate).
  - An instance of `Plate(model)` is created.
  - Parameter sliders for $T_{\text{edge}}$, $T_0$, $L$, and Model A specifics ($s, c_x, c_y$) are bound directly to `plate` attributes with reduced default edge temp ($15.0$).
  - Enforces sensible physical constraints via slider bounds: `min_value=0.1` for dispersion $s$, and `min_value=1.0` for plate size $L$ to mathematically prevent division by zero.

### Lines 28–31: Main Temperature Heat Map
```python
st.subheader("Plate Heat Map")
fig = plots.plot_heatmap(plate, show=False)
st.pyplot(fig)
```
- **Explanation**: Calls `plot_heatmap(plate, show=False)` in `plots.py`. Passing `show=False` suppresses the blocking local desktop window `plt.show()` and instead returns the Matplotlib `Figure` object, which `st.pyplot(fig)` renders inline inside the web page.

### Lines 33–39: Plate Summary Metrics
```python
st.subheader("Plate Summary")
hx, hy, ht = calculus.find_hottest_point(plate)
risk = calculus.get_risk_level(ht)
avg_t = calculus.average_temperature(plate)
st.write("Hottest point: (" + str(round(hx, 2)) + ", " + str(round(hy, 2)) + ") at " + str(round(ht, 2)) + " C (" + risk + " risk)")
st.write("Average plate temperature: " + str(round(avg_t, 2)) + " C")
```
- **Explanation**: Executes three core mathematical tools:
  - `find_hottest_point(plate)`: 2D grid search finding coordinates and peak temperature.
  - `get_risk_level(ht)`: Categorizes operational risk (Low, Medium, High).
  - `average_temperature(plate)`: Double integral evaluated via a 2D midpoint Riemann sum ($80 \times 80$ subdivisions).
  - Displays formatted summary strings.

### Lines 41–55: Point Lookup and Second Derivative Test
```python
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
```
- **Explanation**: Provides interactive mathematical interrogation of any point on the plate.
  - Validates coordinates: if $x$ or $y$ is outside $[0, L]$, shows an amber warning banner.
  - Otherwise, evaluates analytical temperature $T(x, y)$, gradient slopes $\nabla T = \langle T_x, T_y \rangle$, gradient magnitude $|\nabla T|$, second partial derivatives ($T_{xx}, T_{yy}, T_{xy}$), and Hessian discriminant $D = T_{xx}T_{yy} - T_{xy}^2$ with classification (Local Maximum, Minimum, Saddle Point, or Inconclusive).

### Lines 57–69: Chip Cooling via Gradient Descent
```python
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
```
- **Explanation**: Simulates relocating an overheating chip away from the heat source.
  - When the user clicks the "Move chip" button, validates that the start position lies within plate margins.
  - Calls `calculus.gradient_descent(plate, cx0, cy0)`, which steps along the negative gradient $-\nabla T$ for 30 iterations while clamping to physical plate margins.
  - Displays final position, cooled temperature, and plots the trajectory overlay on the thermal heatmap.

### Lines 71–74: Downloadable Engineering Report
```python
metrics = ["Model", "Plate Size L", "T_edge", "T0", "Hottest X", "Hottest Y", "Peak Temp", "Risk Level", "Average Temp"]
values = [plate.model, plate.L, plate.t_edge, plate.t0, round(hx, 2), round(hy, 2), round(ht, 2), risk, round(avg_t, 2)]
df = pd.DataFrame({"Metric": metrics, "Value": values})
st.download_button("Download Report (CSV)", df.to_csv(index=False), "report_" + plate.model + ".csv", "text/csv")
```
- **Explanation**: Bundles the active plate parameters and calculated engineering values into a two-column pandas DataFrame.
  - `st.download_button` serves a browser file download of `report_A.csv` or `report_B.csv` without needing temporary files written to the server's disk.

---

## 3. How `app.py` Calls `models.py` and `calculus.py`

`app.py` acts strictly as an **input/output interface** without any embedded calculus logic:
- **State Carrier**: `plate = models.Plate(model)` creates a data container bundling parameters ($L, T_{\text{edge}}, T_0, s, c_x, c_y$).
- **Calculus Evaluation**: Functions in `calculus.py` receive `plate` as their first parameter (`gradient(plate, px, py)`, `second_derivative_test(plate, px, py)`, `average_temperature(plate)`, etc.).
- **Polymorphism**: When `calculus.py` calls `plate.get_temp(x, y)` or `plate.get_grad(x, y)`, the `Plate` class internally delegates to either Model A or Model B formulas, keeping the UI layer clean and simple.
