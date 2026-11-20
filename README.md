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

All derivatives are worked out by hand and written as formulas in calsympy.py. SymPy is used in check_sympy() (menu option 8) to confirm the hand formulas.

## Risk level and cooling suggestions

The peak temperature is classified as Low (below 70 degrees C), Medium (70 to 90) or High (above 90). Intel says the maximum junction temperature usually lies between about 100 and 110 degrees C, depending on the product. Our 70 and 90 degree limits are our own rule of thumb with a safety margin. For Medium and High, the program says how many degrees the peak must drop to reach Low and lists simple options such as reducing the chip heating, cooling the edges, adding a heat sink or fan, or moving the part. This is a set of if/else rules, not engineering advice.

## How to run

Install the libraries:

    pip install -r requirements.txt

Console version:

    python calsympy.py

Web version:

    streamlit run app.py

Checks (SymPy and assert tests):

    python calsympy.py
    (choose option 8: Self-check)

Or run the self-checks directly:

    python -c "import calsympy; calsympy.run_checks()"

Live link: (add after deployment)

## Files

- calsympy.py: single unified file containing temperature models, hand derivatives, calculus tools, plots, self-checks, and console menu
- app.py: Streamlit web page (a thin layer on top of calsympy.py)
- requirements.txt: list of required Python packages
- .gitignore: specifies untracked files
- PSEUDOCODE.md: pseudo-code for the main algorithms
- TEST_REPORT.md: tests we ran and the bugs found and fixed
- DEPLOY.md: how the web app was deployed
- notebooks/colab_backup.ipynb: backup copy that runs on Google Colab

## Libraries

NumPy, Matplotlib, Pandas and SymPy are used for the project. Streamlit is used only for the web page.

## Limitations

- The plate is a simple, flat, uniform square and the temperature is steady (it does not change with time).
- The two models are idealised shapes and have not been compared with real measurements.
- The risk limits and the cooling advice are our own simple rules.
- The average temperature is an approximation and gets more accurate when more steps are used.

## Failure cases

| Case | What could go wrong | What we did | Status |
| --- | --- | --- | --- |
| s or L = 0 | Division by zero in formulas (`1/s` or `pi/L`) causing `ZeroDivisionError` | `ask_param()` in `calsympy.py` rejects inputs `<= 0` and keeps current value; `app.py` sliders enforce `min_value=0.1` for `s` and `min_value=1.0` for `L` | Fixed |
| Letters or empty input | Program crashes with `ValueError` when converting strings to `float` | `ask_param()` catches `ValueError` and falls back to default; empty inputs keep current value; coordinates check catches invalid strings | Fixed |
| Point outside the plate | Point lookup computes out-of-bounds temperatures beyond the physical plate boundary $[0, L] \times [0, L]$ | `option_lookup()` in `calsympy.py` checks `0 <= x, y <= L` and prints warning; `app.py` displays warning banner | Fixed |
| Read-only report file | Saving report raises `PermissionError` (subclass of `OSError`) if destination file is locked or read-only | `option_save_report()` in `calsympy.py` wraps file writes in `try ... except (IOError, OSError)` and displays friendly error message | Fixed |
| D = 0 | Second derivative test cannot determine if a critical point is an extremum or saddle point; floating-point roundoff can yield tiny negative values (e.g. $D \approx -1.1 \times 10^{-13}$ on Model B at $(1, 1)$) falsely reporting "Saddle Point" | `second_derivative_test()` checks `abs(d) < 1e-6` first and returns `"Inconclusive"` | Fixed |
| D-test at non-critical point | Second derivative test only applies at critical points where the gradient is zero; at non-critical points (e.g. Model A at $(3, 2.5)$ where $|\nabla T| \approx 35.91\text{ C/cm}$), evaluating $D$ gives a mathematically invalid classification (such as "Saddle Point") | `calsympy.py` and `app.py` check if gradient magnitude $> 0.01$; if non-zero, they display $D$ but state the second derivative test does not apply here | Fixed |
| Chip starting at the peak | Chip is already at local maximum where gradient $\nabla T = \langle 0, 0 \rangle$, so magnitude is 0 and descent cannot find a downhill direction | In `gradient_descent()` the magnitude check `if mag > 0.0:` keeps the chip stationary; default start is set away from center $(1.5, 1.5)$ | Not fixed (limitation) |
| Large gradient descent step | A huge step size could overshoot or throw coordinates far off the plate | Each step moves along the unit downhill vector and coordinates are clamped to safe plate margins $[0.2, L - 0.2]$ on every step | Fixed |
| Few Riemann sum steps | Small `n_steps` (e.g. 2 or 5) produces coarse Riemann sum discretization error | Default `n_steps` is set to 80 ($80 \times 80 = 6,400$ midpoints), converging within $< 0.01^\circ\text{C}$ of continuous integral | Not fixed (limitation) |
| Grid-search hottest point accuracy | True peak location falls between discrete grid points, slightly underestimating peak temperature | Grid resolution defaults to $50 \times 50$ or $60 \times 60$ ($dx \approx 0.067\text{ cm}$), keeping error within $\sim 0.1^\circ\text{C}$; theoretical peak is known analytically | Not fixed (limitation) |
| Gradient descent stopping at plate margin | Downhill descent pushes chip into boundary margin $[0.2, L - 0.2]$, causing repeated stationary steps | Clamping keeps the chip inside safe margins $[0.2, L - 0.2]$, but the chip stops at the margin and does not search beyond it | Handled, with a limitation |
| Unrealistic parameter values | User inputs extreme values (e.g. $T_0 = 10,000^\circ\text{C}$ or $T_{\text{edge}} = -500^\circ\text{C}$ below absolute zero) | `app.py` sliders constrain values to reasonable ranges; CLI allows arbitrary floats (except $s, L \le 0$) | Not fixed (limitation) |
| Idealised models | Real boards have transient conduction, convection, traces, and non-uniform components | Handled as intentional pedagogical simplification; documented in README and app expander that formulas are idealized shapes | Not fixed (limitation) |
| Web app asleep or offline | Web app is sleeping or network is unavailable | Free apps go to sleep after a period with no visitors and may take a moment to wake up; the console version (`python calsympy.py`) and the Colab notebook work without the web app | Not fixed (limitation) |
| No safe place on the plate | All plate temperatures exceed threshold limit (e.g. limit=10 C or high T_edge) | `find_best_placement()` returns `None`; both CLI and web app report that no safe position exists | Fixed |
| Several equally good places | Multiple grid points have identical minimum distance to start position | First encountered point during grid iteration is returned | Handled, with a limitation |

