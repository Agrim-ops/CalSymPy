# Using Partial Derivatives and Matplotlib in Python to Visualize Heat Distribution on a Surface

Team 4 (Delta-T), Mathematics and Python Programming  
CalSymPy project

## What this project does

This program models how temperature is spread over a flat square plate, for example a circuit board with a chip on it. It uses calculus to find the hottest point, the direction heat changes fastest, the average temperature, and a better place to put a heat-sensitive part. It shows the results as heat maps and also gives simple cooling suggestions. The temperature depends only on position (x, y), so there is no time variable.

## Team

| Member | Role |
| --- | --- |
| Anvesha Misra | Project Manager |
| Swastik Mishra | Researcher |
| Manvi Singh | Mathematical Modeler |
| Advitiya Sharma | Pseudocode Formulator |
| Tanmay Singh | Code Developer |
| Agrim Goel | Program Deployer and Tester |
| Pari Raj | Information Analyst |

## The two models

The plate has side length L = 4 cm. Both models are fixed formulas that we chose to give realistic shapes. They are not solutions of the heat equation.

Model A (single hotspot): one chip at (cx, cy) heats the area around it.

```text
T(x, y) = T_edge + T0 * exp(-((x - cx)^2 + (y - cy)^2) / s)
```

Default values: T_edge = 25, T0 = 60, s = 2, cx = cy = 2. The peak is 85 degrees C at (2, 2).

Model B (cold edges): the edges are kept at T_edge and the plate is hottest in the middle.

```text
T(x, y) = T_edge + T0 * sin(pi*x/L) * sin(pi*y/L)
```

Default values: T_edge = 20, T0 = 50. The peak is 70 degrees C at (2, 2).

## Calculus used

- Partial derivatives Tx and Ty, and the gradient vector with its magnitude. The gradient points in the direction where temperature rises fastest.
- Second partial derivatives Txx, Tyy and Txy, and the second derivative test `D = Txx * Tyy - Txy^2`. The test applies at critical points where the gradient is zero: D > 0 with Txx < 0 is a maximum, D > 0 with Txx > 0 is a minimum, D < 0 is a saddle point, and D = 0 is inconclusive.
- Double integral for the average temperature, calculated with a midpoint Riemann sum.
- Tangent plane (linear approximation) and a degree 2 Taylor polynomial around a point.
- Gradient descent: a chip is moved step by step in the direction of -gradient so it ends up in a cooler place.
- Best placement search: finds the closest location inside safe plate margins where temperature is below a safe limit (e.g. 70 degrees C).

SymPy differentiates both temperature models symbolically (`sp.diff`) and `sp.lambdify` compiles $T, T_x, T_y, T_{xx}, T_{yy},$ and $T_{xy}$ into NumPy functions cached in `st.session_state["funcs"]` inside `app.py`.

## Risk level and cooling suggestions

The peak temperature is classified as Low (below 70 degrees C), Medium (70 to 90) or High (above 90). Intel says the maximum junction temperature usually lies between about 100 and 110 degrees C, depending on the product. Our 70 and 90 degree limits are our own rule of thumb with a safety margin. For Medium and High, the program says how many degrees the peak must drop to reach Low and lists simple options such as reducing the chip heating, cooling the edges, adding a heat sink or fan, or moving the part. This is a set of if/else rules, not engineering advice.

## How to run

Install the libraries:

    pip install -r requirements.txt

Run the web app:

    streamlit run app.py

## Files

- app.py: single self-contained file containing SymPy model compilation, `Plate` class, calculus tools, optimization, and the Streamlit web UI
- functions.md: reference guide explaining all functions and mathematics in plain, intuitive terms
- PSEUDOCODE.md: formal algorithm specifications, pseudocode, and time/space complexity analysis
- blocked_pseudocode.md: slide-ready blocked pseudocode
- FLOWCHART.md: algorithm flowchart diagrams
- requirements.txt: list of required Python packages (`numpy`, `matplotlib`, `pandas`, `sympy`, `streamlit`)
- README.md: project overview, models, calculus formulas, and usage guide
- .gitignore: specifies untracked files

## Libraries

NumPy, Matplotlib, Pandas, SymPy, and Streamlit are used in `app.py`.

## Limitations

- The plate is a simple, flat, uniform square and the temperature is steady (it does not change with time).
- The two models are idealised shapes and have not been compared with real measurements.
- The risk limits and the cooling advice are our own simple rules.
- The average temperature is an approximation and gets more accurate when more steps are used.

## Failure cases

| Case | What could go wrong | What we did | Status |
| --- | --- | --- | --- |
| s or L = 0 | Division by zero in formulas (`1/s` or `pi/L`) causing `ZeroDivisionError` | `app.py` sliders enforce `min_value=0.1` for `s` and `1.0` for `L` | Fixed |
| Letters or empty input | Crash if non-numeric input is passed | `app.py` uses Streamlit `slider` and `number_input` widgets so invalid strings cannot be entered | Fixed |
| Point outside the plate | Point lookup computes out-of-bounds coordinates beyond $[0, L] \times [0, L]$ | `app.py` checks `0 <= px <= L and 0 <= py <= L` (and chip start coordinates) and shows `st.warning(...)` | Fixed |
| Report file write error | Local file writes could fail on read-only paths | `app.py` exports the CSV directly in browser via `st.download_button(...)` | Fixed |
| D = 0 | Second derivative test cannot determine if a critical point is an extremum or saddle point; floating-point roundoff can yield tiny values falsely reporting "Saddle Point" | `second_derivative_test()` checks `abs(d) < 1e-6` first and returns `"Inconclusive"` | Fixed |
| D-test at non-critical point | Second derivative test only applies at critical points where gradient is zero | `app.py` checks `if mag < 0.01`; if non-zero, it prints $D$ with `(not a critical point, so the D test does not apply)` | Fixed |
| Chip starting at the peak | Gradient $\nabla T = \langle 0, 0 \rangle$ at peak, so magnitude is 0 | In `gradient_descent()` the check `if mag > 0:` keeps the chip stationary; default chip start is `(1.5, 1.5)` | Not fixed (limitation) |
| Large gradient descent step | Huge step size could overshoot or leave the plate | Each step moves along unit downhill direction (`step=0.1`) and clamps coordinates to `[0.2, plate.L - 0.2]` | Fixed |
| Few Riemann sum steps | Small grid `n` produces coarse discretization error | Default `n=80` (`80 x 80 = 6,400` midpoints) in `average_temperature(plate, n=80)` | Not fixed (limitation) |
| Grid-search hottest point accuracy | True peak can fall between discrete grid points | Grid defaults to `n=50` in `find_hottest_point` and `n=60` in `find_best_placement` | Not fixed (limitation) |
| Gradient descent stopping at plate margin | Downhill descent pushes chip into boundary `[0.2, L - 0.2]` | Clamping keeps the chip inside safe margins `[0.2, L - 0.2]`, stopping at the border | Handled, with a limitation |
| Unrealistic parameter values | Extreme temperatures or dimensions | `app.py` sidebar sliders constrain `L` (`1.0..10.0`), `T_edge` (`0.0..50.0`), `T0` (`0.0..150.0`), `s` (`0.1..10.0`), `cx`/`cy` (`0.0..L`) | Handled |
| Idealised models | Real boards have transient conduction, convection, traces, and non-uniform components | Documented in `README.md` and the app expander that formulas are idealized shapes | Not fixed (limitation) |
| Web app asleep or offline | Hosted web app is sleeping or network is unavailable | Free hosted apps sleep after inactivity; running `streamlit run app.py` locally works offline | Not fixed (limitation) |
| No safe place on the plate | All grid points exceed `limit=70.0` C | `find_best_placement()` returns `None`; `app.py` prints `Best placement below 70 C: none on this plate` | Fixed |
| Several equally good places | Multiple grid points have identical minimum distance to start | First encountered grid point minimizing distance (`dist < best[3]`) is returned | Handled, with a limitation |

