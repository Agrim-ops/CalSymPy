# CalSymPy Function Reference & Deep-Dive Guide
**Project**: CalSymPy (MAT 112 Engineering Mathematics & Python Programming)  
**Team 4 (Delta-T)**: Circuit Board Thermal Distribution & Multivariable Calculus  
**Unified File**: `calsympy.py` | **Web Interface**: `app.py`

---

## 1. Executive Summary & Code Architecture

The CalSymPy project models steady-state two-dimensional temperature distributions $T(x, y)$ over a square circuit plate of side length $L$ ($[0, L] \times [0, L]$). It implements multivariable calculus algorithms to analyze thermal properties, locate hot spots, evaluate spatial average temperatures, compute tangent planes and quadratic approximations, and relocate heat-sensitive electronic chips to cooler regions using constrained gradient descent.

The codebase is consolidated into a single primary file, `calsympy.py`, cleanly partitioned into five logical sections:
1. **Models (`# --- models ---`)**: Analytical surface formulas, exact hand-derived first/second partial derivatives, and the `Plate` data carrier.
2. **Calculus (`# --- calculus ---`)**: Core mathematical algorithms (gradient vector, Hessian discriminant test, double integral Riemann sum, tangent plane, Taylor polynomial, unit-step gradient descent, peak grid search, risk categorization, cooling suggestions, and closest safe placement search).
3. **Plots (`# --- plots ---`)**: Matplotlib visualization functions supporting both blocking desktop interactive display and non-blocking headless rendering.
4. **Checks (`# --- checks ---`)**: Automated verification suite validating hand derivations against SymPy symbolic calculus and asserting algorithmic properties.
5. **Console (`# --- console ---`)**: Terminal user interface providing an interactive numbered menu (options 0 to 8).

The Streamlit web application (`app.py`) acts as a thin graphical presentation layer on top of `calsympy.py`, importing the module and rendering controls and visualizations dynamically.

---

## 2. Master Function Directory

Below is a complete index of all 36 functions and methods defined in `calsympy.py`:

| # | Function / Method | Category | Inputs | Returns | Mathematical / Operational Purpose |
| :- | :--- | :--- | :--- | :--- | :--- |
| 1 | `temp_a` | Models | `x, y, t_edge, t0, s, cx, cy` | `float` or `ndarray` | Evaluates Model A Gaussian hotspot temperature |
| 2 | `grad_a` | Models | `x, y, t_edge, t0, s, cx, cy` | `(Tx, Ty)` | Analytical first partial derivatives for Model A |
| 3 | `hessian_a` | Models | `x, y, t_edge, t0, s, cx, cy` | `(Txx, Tyy, Txy)` | Analytical second partial derivatives for Model A |
| 4 | `temp_b` | Models | `x, y, t_edge, t0, L` | `float` or `ndarray` | Evaluates Model B sinusoidal standing wave temperature |
| 5 | `grad_b` | Models | `x, y, t_edge, t0, L` | `(Tx, Ty)` | Analytical first partial derivatives for Model B |
| 6 | `hessian_b` | Models | `x, y, t_edge, t0, L` | `(Txx, Tyy, Txy)` | Analytical second partial derivatives for Model B |
| 7 | `Plate.__init__` | Class | `model="A"` | `None` | Initializes plate attributes ($L, s, c_x, c_y$) and default model |
| 8 | `Plate.set_model` | Class | `model` | `None` | Switches active model and resets default parameters |
| 9 | `Plate.get_temp` | Class | `x, y` | `float` or `ndarray` | Dispatches temperature evaluation to active model |
| 10 | `Plate.get_grad` | Class | `x, y` | `(Tx, Ty)` | Dispatches gradient evaluation to active model |
| 11 | `Plate.get_hessian` | Class | `x, y` | `(Txx, Tyy, Txy)` | Dispatches Hessian partials to active model |
| 12 | `gradient` | Calculus | `plate, x, y` | `(Tx, Ty, mag)` | Calculates gradient vector and Euclidean magnitude $|\nabla T|$ |
| 13 | `second_derivative_test` | Calculus | `plate, x, y` | `(Txx, Tyy, Txy, D, class)` | Classifies critical point using Hessian discriminant $D$ |
| 14 | `average_temperature` | Calculus | `plate, n_steps=80` | `float` | Approximates $\frac{1}{\text{Area}}\iint_R T\,dA$ via 2D midpoint Riemann sum |
| 15 | `tangent_plane` | Calculus | `plate, a, b, x, y` | `float` | Linear Taylor approximation $L(x, y)$ near base point $(a, b)$ |
| 16 | `taylor_degree_2` | Calculus | `plate, a, b, x, y` | `float` | Quadratic Taylor approximation $Q(x, y)$ near base point $(a, b)$ |
| 17 | `gradient_descent` | Calculus | `plate, start_x, start_y, ...` | `(path, final_temp)` | Downhill cooling relocation using unit negative gradient |
| 18 | `find_hottest_point` | Calculus | `plate, n_grid=50` | `(best_x, best_y, peak_t)` | 2D regular grid search for maximum plate temperature |
| 19 | `get_risk_level` | Calculus | `temp` | `"Low"\|"Medium"\|"High"` | Industrial electronics operational risk classification |
| 20 | `cooling_suggestions` | Calculus | `peak_temp` | `list[str]` | Practical thermal engineering rules of thumb |
| 21 | `find_best_placement` | Calculus | `plate, start_x, start_y, ...` | `(x, y, temp, dist)` or `None` | Finds closest safe position ($< 70^\circ\text{C}$) inside margins |
| 22 | `plot_heatmap` | Plots | `plate, n_grid=50, show=True` | `plt.Figure` | 2D thermal color map with contour line overlays |
| 23 | `plot_descent_path` | Plots | `plate, path, ...` | `plt.Figure` | Overlays descent trajectory and best placement on heatmap |
| 24 | `check_sympy` | Checks | None | `None` | Compares hand partial derivatives against SymPy exact calculus |
| 25 | `check_plate_calculus` | Checks | None | `None` | Unit test assertions for temperatures, slopes, and curvature |
| 26 | `check_optimization` | Checks | None | `None` | Unit test assertions for descent, risk, and placement search |
| 27 | `run_checks` | Checks | None | `None` | Master runner executing all assertions and symbolic checks |
| 28 | `show_menu` | Console | None | `None` | Prints interactive menu options (0 to 8) to terminal |
| 29 | `ask_param` | Console | `name, current_val` | `float` | Safe numeric prompt with strictly positive input validation |
| 30 | `option_choose_model` | Console | `plate` | `None` | Option 1: switch active model type and adjust parameters |
| 31 | `option_lookup` | Console | `plate` | `None` | Option 3: evaluate point temperature, gradient, and D-test |
| 32 | `option_hottest` | Console | `plate` | `None` | Option 4: search for peak hotspot and cooling suggestions |
| 33 | `option_average` | Console | `plate` | `None` | Option 5: calculate spatial average temperature via Riemann sum |
| 34 | `option_descent` | Console | `plate` | `None` | Option 6: simulate chip cooling relocation and plot path |
| 35 | `option_save_report` | Console | `plate` | `None` | Option 7: export summary metrics to CSV or plain text file |
| 36 | `main` | Console | None | `None` | Main program loop dispatching user choices 0 to 8 |

---

## 3. In-Depth Function Breakdown

### Part 1: Analytical Thermal Models (`# --- models ---`)

#### 1. `temp_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0)`
- **Role**: Mathematical model function for Model A.
- **Physics / Engineering Context**: Models an overheating microchip positioned at $(c_x, c_y)$ emitting heat that diffuses symmetrically outward in a bell-shaped Gaussian curve.
- **Mathematical Formula**:
  $$T_A(x, y) = T_{\text{edge}} + T_0 \exp\left( -\frac{(x - c_x)^2 + (y - c_y)^2}{s} \right)$$
- **Parameters**:
  - `x, y`: Coordinate(s) on plate (scalar `float` or NumPy array).
  - `t_edge`: Ambient plate boundary temperature ($25.0^\circ\text{C}$).
  - `t0`: Maximum temperature rise generated by the chip ($60.0^\circ\text{C}$).
  - `s`: Gaussian dispersion / spread parameter ($2.0\text{ cm}^2$). Must be $> 0$.
  - `cx, cy`: Center location of the hotspot ($(2.0, 2.0)\text{ cm}$).
- **Behavior**:
  - At center $(c_x, c_y)$: Distance $r = 0 \implies \exp(0) = 1 \implies T = T_{\text{edge}} + T_0 = 85.0^\circ\text{C}$.
  - Far away ($r \to \infty$): $\exp(-r^2/s) \to 0 \implies T \to T_{\text{edge}} = 25.0^\circ\text{C}$.

---

#### 2. `grad_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0)`
- **Role**: Analytical first partial derivatives for Model A.
- **Calculus Principle**: Multivariable Chain Rule.
  Let $u(x, y) = -\frac{(x - c_x)^2 + (y - c_y)^2}{s} = -\frac{r^2}{s}$. Then $T = T_{\text{edge}} + T_0 e^{u}$.
  $$\frac{\partial u}{\partial x} = -\frac{2(x - c_x)}{s}, \quad \frac{\partial u}{\partial y} = -\frac{2(y - c_y)}{s}$$
  Applying chain rule $\frac{\partial T}{\partial x} = T_0 e^u \frac{\partial u}{\partial x}$:
  $$T_x = -\frac{2 T_0}{s}(x - c_x)\exp\left(-\frac{r^2}{s}\right)$$
  $$T_y = -\frac{2 T_0}{s}(y - c_y)\exp\left(-\frac{r^2}{s}\right)$$
- **Return Value**: Tuple `(Tx, Ty)` representing $\nabla T_A = \langle T_x, T_y \rangle$.
- **Critical Point**: At $(c_x, c_y)$, $x - c_x = 0$ and $y - c_y = 0 \implies \nabla T = \langle 0, 0 \rangle$.

---

#### 3. `hessian_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0)`
- **Role**: Analytical second partial derivatives for Model A.
- **Calculus Principle**: Product Rule and Chain Rule.
  Let $e = T_0 \exp(-r^2 / s)$. Since $T_x = e \cdot \left(-\frac{2(x - c_x)}{s}\right)$:
  $$\frac{\partial}{\partial x}[T_x] = \left(\frac{\partial e}{\partial x}\right)\left(-\frac{2(x - c_x)}{s}\right) + e \cdot \frac{\partial}{\partial x}\left(-\frac{2(x - c_x)}{s}\right)$$
  $$= \left(e \cdot -\frac{2(x - c_x)}{s}\right)\left(-\frac{2(x - c_x)}{s}\right) + e \cdot \left(-\frac{2}{s}\right) = e \left[ \frac{4(x - c_x)^2}{s^2} - \frac{2}{s} \right]$$
  $$T_{yy} = e \left[ \frac{4(y - c_y)^2}{s^2} - \frac{2}{s} \right]$$
  $$T_{xy} = \frac{\partial}{\partial y}[T_x] = \left(e \cdot -\frac{2(y - c_y)}{s}\right)\left(-\frac{2(x - c_x)}{s}\right) = e \cdot \frac{4(x - c_x)(y - c_y)}{s^2}$$
- **Clairaut's Theorem**: $T_{xy} = T_{yx}$ because $T_A(x, y)$ is smooth and continuously differentiable ($C^\infty$).
- **Return Value**: Tuple `(Txx, Tyy, Txy)`.
- **Value at Peak $(2, 2)$**:
  $T_{xx} = 60(1)[0 - 2/2] = -60.0$, $T_{yy} = -60.0$, $T_{xy} = 0.0$.

---

#### 4. `temp_b(x, y, t_edge=20.0, t0=50.0, L=4.0)`
- **Role**: Mathematical model function for Model B.
- **Physics / Engineering Context**: Models a symmetric standing wave thermal field on a plate with edges actively clamped to cold temperatures (e.g., edge heatsinks).
- **Mathematical Formula**:
  $$T_B(x, y) = T_{\text{edge}} + T_0 \sin\left(\frac{\pi x}{L}\right)\sin\left(\frac{\pi y}{L}\right)$$
- **Boundary Condition Behavior**:
  - Along all four physical edges ($x=0, x=L, y=0, y=L$), $\sin(0) = \sin(\pi) = 0$.
  - Therefore, $T(0, y) = T(L, y) = T(x, 0) = T(x, L) = T_{\text{edge}} = 20.0^\circ\text{C}$.
  - Peak occurs at plate center $(L/2, L/2) = (2, 2)$: $\sin(\pi/2)\sin(\pi/2) = 1 \cdot 1 = 1 \implies T_{\text{peak}} = 20 + 50 = 70.0^\circ\text{C}$.

---

#### 5. `grad_b(x, y, t_edge=20.0, t0=50.0, L=4.0)`
- **Role**: Analytical first partial derivatives for Model B.
- **Calculus Principle**: Differentiation of trigonometric products.
  Let $u = \frac{\pi x}{L}$ and $v = \frac{\pi y}{L}$.
  $$T_x = T_0 \frac{\pi}{L} \cos\left(\frac{\pi x}{L}\right)\sin\left(\frac{\pi y}{L}\right)$$
  $$T_y = T_0 \frac{\pi}{L} \sin\left(\frac{\pi x}{L}\right)\cos\left(\frac{\pi y}{L}\right)$$
- **Return Value**: Tuple `(Tx, Ty)`.
- **Center Value $(2, 2)$**: $\cos(\pi/2) = 0 \implies T_x = 0, T_y = 0$ (critical point).

---

#### 6. `hessian_b(x, y, t_edge=20.0, t0=50.0, L=4.0)`
- **Role**: Analytical second partial derivatives for Model B.
- **Mathematical Derivation**:
  Differentiating $T_x$ and $T_y$:
  $$T_{xx} = -T_0 \left(\frac{\pi}{L}\right)^2 \sin\left(\frac{\pi x}{L}\right)\sin\left(\frac{\pi y}{L}\right)$$
  $$T_{yy} = -T_0 \left(\frac{\pi}{L}\right)^2 \sin\left(\frac{\pi x}{L}\right)\sin\left(\frac{\pi y}{L}\right) = T_{xx}$$
  $$T_{xy} = T_0 \left(\frac{\pi}{L}\right)^2 \cos\left(\frac{\pi x}{L}\right)\cos\left(\frac{\pi y}{L}\right)$$
- **Return Value**: Tuple `(Txx, Tyy, Txy)` where `Tyy = Txx`.
- **Curvature at Critical Point $(2, 2)$**:
  $T_{xx} = -50(\pi/4)^2(1)(1) \approx -30.843$, $T_{yy} \approx -30.843$, $T_{xy} = 0$.
  Discriminant $D = T_{xx}T_{yy} - T_{xy}^2 = (-30.843)^2 - 0 \approx 951.27 > 0$, $T_{xx} < 0 \implies$ Local Maximum.

---

#### 7–11. `Plate` Class
- **Role**: Object-oriented data container and polymorphic dispatcher.
- **Methods**:
  - `__init__(self, model="A")`: Sets default plate geometry $L = 4.0\text{ cm}$, hotspot parameters $s = 2.0, c_x = 2.0, c_y = 2.0$, and calls `set_model(model)`.
  - `set_model(self, model)`: Sets `self.model` to `"A"` or `"B"`. Resets default baseline temperatures ($T_{\text{edge}}=25, T_0=60$ for A; $T_{\text{edge}}=20, T_0=50$ for B).
  - `get_temp(self, x, y)`: Routes evaluation to `temp_a` or `temp_b` based on `self.model`.
  - `get_grad(self, x, y)`: Routes evaluation to `grad_a` or `grad_b`.
  - `get_hessian(self, x, y)`: Routes evaluation to `hessian_a` or `hessian_b`.
- **Architectural Value**: Eliminates repetitive `if plate.model == "A"` branches across all calculus and plotting functions.

---

### Part 2: Multivariable Calculus Tools (`# --- calculus ---`)

#### 12. `gradient(plate, x, y)`
- **Role**: Evaluates the gradient vector and total slope magnitude.
- **Mathematical Definition**:
  $$\nabla T(x, y) = \left\langle \frac{\partial T}{\partial x}, \frac{\partial T}{\partial y} \right\rangle = \langle T_x, T_y \rangle$$
  $$|\nabla T| = \sqrt{T_x^2 + T_y^2}$$
- **Physical Meaning**: $\nabla T$ points in the direction of steepest temperature ascent. Its magnitude $|\nabla T|$ is the directional derivative along that path, measured in $^\circ\text{C/cm}$.
- **Return Value**: Tuple `(Tx, Ty, magnitude)`.

---

#### 13. `second_derivative_test(plate, x, y)`
- **Role**: Classifies surface curvature and stationary points.
- **Mathematical Formula**:
  The Hessian matrix is $\mathcal{H} = \begin{bmatrix} T_{xx} & T_{xy} \\ T_{xy} & T_{yy} \end{bmatrix}$. The discriminant is:
  $$D = \det(\mathcal{H}) = T_{xx} T_{yy} - T_{xy}^2$$
- **Classification Rules**:
  1. **Numerical Near-Zero Guard**: If $|D| < 10^{-6}$, return `"Inconclusive"`. (Prevents floating-point roundoff from misclassifying points where analytical $D = 0$, such as Model B at $(1, 1)$ where $\sin(\pi/4) = \cos(\pi/4)$).
  2. If $D > 0$ and $T_{xx} < 0$: `"Local Maximum"` (surface is concave down in all directions).
  3. If $D > 0$ and $T_{xx} > 0$: `"Local Minimum"` (surface is concave up in all directions).
  4. If $D < 0$: `"Saddle Point"` (surface curves up in one direction and down in another).
- **Non-Critical Point Condition**: In `calsympy.py` and `app.py`, this test is only evaluated if $|\nabla T| \le 0.01$. If $|\nabla T| > 0.01$, the program reports that the point is not a critical point so the test does not apply.

---

#### 14. `average_temperature(plate, n_steps=80)`
- **Role**: Evaluates the spatial average temperature across the 2D surface.
- **Continuous Formulation**:
  $$T_{\text{avg}} = \frac{1}{\text{Area}} \iint_R T(x, y) \, dA = \frac{1}{L^2} \int_0^L \int_0^L T(x, y) \, dx \, dy$$
- **Discrete Approximation (2D Midpoint Riemann Sum)**:
  Subdivides $[0, L] \times [0, L]$ into $n_{\text{steps}} \times n_{\text{steps}} = 80 \times 80 = 6,400$ sub-rectangles.
  $$\Delta x = \frac{L}{n_{\text{steps}}}, \quad \Delta A = \Delta x^2$$
  $$x_i = \left(i + \frac{1}{2}\right)\Delta x, \quad y_j = \left(j + \frac{1}{2}\right)\Delta x$$
  $$T_{\text{avg}} \approx \frac{1}{L^2} \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} T(x_i, y_j) \Delta A$$
- **Benchmark**: For Model A default ($L=4, T_{\text{edge}}=25, T_0=60, s=2$), $T_{\text{avg}} \approx 46.47^\circ\text{C}$.

---

#### 15. `tangent_plane(plate, a, b, x, y)`
- **Role**: Evaluates the first-order (linear) Taylor polynomial approximation.
- **Mathematical Formula**:
  $$L(x, y) = T(a, b) + T_x(a, b)(x - a) + T_y(a, b)(y - b)$$
- **Geometric Interpretation**: Represents the unique tangent plane touching the 3D surface $z = T(x, y)$ at the base point $(a, b, T(a, b))$.

---

#### 16. `taylor_degree_2(plate, a, b, x, y)`
- **Role**: Evaluates the second-order (quadratic) Taylor polynomial approximation.
- **Mathematical Formula**:
  $$Q(x, y) = T(a, b) + T_x(a, b)\Delta x + T_y(a, b)\Delta y + \frac{1}{2}T_{xx}(a, b)\Delta x^2 + T_{xy}(a, b)\Delta x \Delta y + \frac{1}{2}T_{yy}(a, b)\Delta y^2$$
  where $\Delta x = x - a$ and $\Delta y = y - b$.
- **Geometric Interpretation**: Represents the osculating paraboloid that matches both the slopes (first partials) and the surface curvature (second partials) at $(a, b)$.

---

#### 17. `gradient_descent(plate, start_x, start_y, step_size=0.1, steps=40)`
- **Role**: Simulates relocating a hot chip downhill to cooler regions.
- **Algorithm**:
  For step $k = 0, 1, \dots, \text{steps}-1$:
  1. Evaluate gradient $\nabla T = \langle T_x, T_y \rangle$ and magnitude $|\nabla T| = \sqrt{T_x^2 + T_y^2}$.
  2. If $|\nabla T| > 0$, compute unit direction vector $\hat{u} = \frac{\nabla T}{|\nabla T|}$ and move along $-\hat{u}$:
     $$x_{k+1} = x_k - \text{step\_size} \cdot \frac{T_x}{|\nabla T|}, \quad y_{k+1} = y_k - \text{step\_size} \cdot \frac{T_y}{|\nabla T|}$$
  3. Clamp coordinates to safe plate margins $[0.2, L - 0.2]$:
     $$x_{k+1} = \max(0.2, \min(L - 0.2, x_{k+1}))$$
  4. Record new point in `path`.
- **Why Unit Steps?**: Raw gradient descent moves by $-\alpha \nabla T$. Near peaks where $|\nabla T| \approx 36\text{ C/cm}$, a fixed step size without normalization would cause huge jumps overshooting the plate. Unit-step descent guarantees each physical step moves exactly $\text{step\_size} = 0.10\text{ cm}$.

---

#### 18. `find_hottest_point(plate, n_grid=50)`
- **Role**: Global peak search across the 2D plate.
- **Algorithm**: Scans a regular $(n_{\text{grid}} + 1) \times (n_{\text{grid}} + 1)$ grid ($51 \times 51 = 2,601$ points) spanning $[0, L] \times [0, L]$. Tracks and returns the maximum temperature and its coordinates $(x^*, y^*, T^*)$.

---

#### 19. `get_risk_level(temp)`
- **Role**: Translates operating temperature into standard electronics risk levels.
- **Thresholds**:
  - `temp < 70.0 C`: `"Low"` (safe continuous operation).
  - `70.0 <= temp <= 90.0 C`: `"Medium"` (elevated temperature; cooling recommended).
  - `temp > 90.0 C`: `"High"` (danger of thermal throttling or component failure).

---

#### 20. `cooling_suggestions(peak_temp)`
- **Role**: Practical engineering rules of thumb for thermal dissipation.
- **Logic**:
  - If `Low`: `"Temperature is safe; no action needed."`
  - If `Medium` or `High`:
    - Computes required temperature reduction: $\Delta T = \text{round}(\text{peak\_temp} - 69.9, 1)$.
    - Advises: `"Peak temperature must fall by at least <drop> deg C to reach Low risk."`
    - Option 1: Reduce chip heating $T_0$ by $\Delta T$.
    - Option 2: Cool plate surroundings and edges $T_{\text{edge}}$ by $\Delta T$.
  - If `High`: Additionally recommends adding a heatsink or fan, and relocating components via gradient descent.

---

#### 21. `find_best_placement(plate, start_x, start_y, limit=70.0, n_grid=60)`
- **Role**: Constrained optimization finding the closest safe point to an overheating chip.
- **Algorithm**:
  - If $T(\text{start\_x}, \text{start\_y}) < \text{limit}$, returns initial position with distance $0.0$.
  - Otherwise, discretizes safe internal region $[0.2, L - 0.2] \times [0.2, L - 0.2]$ into $(61 \times 61 = 3,721)$ points.
  - Finds point $(x, y)$ that satisfies $T(x, y) < \text{limit}$ while minimizing Euclidean distance:
    $$\text{dist} = \sqrt{(x - \text{start\_x})^2 + (y - \text{start\_y})^2}$$
- **Return Value**: Tuple `(x, y, temp, dist)` or `None` if no point on the plate is below `limit`.

---

### Part 3: Visualization Routines (`# --- plots ---`)

#### 22. `plot_heatmap(plate, n_grid=50, show=True)`
- **Role**: Generates a 2D thermal color map with contour lines.
- **Implementation**:
  - Generates coordinate mesh using `np.meshgrid` from $0$ to $L$.
  - Uses `plt.imshow` with `cmap="inferno"`, colorbar labeled in $^\circ\text{C}$, and `origin="lower"`.
  - Overlays white contour lines (`plt.contour`) showing isotherms.
  - Dual Mode: If `show=True`, opens desktop GUI (`plt.show()`); always returns the Matplotlib `Figure` object for Streamlit or test inspection.

---

#### 23. `plot_descent_path(plate, path, n_grid=50, show=True, best_point=None)`
- **Role**: Visualizes the downhill optimization trajectory.
- **Visual Features**:
  - Background thermal heatmap (`inferno`).
  - White dashed line (`w--`) tracing the descent steps.
  - Green circle (`go`) marking the starting position.
  - Cyan circle (`co`) marking the final descent location.
  - Yellow star (`y*`) marking the closest safe placement found by `find_best_placement` (if provided).

---

### Part 4: Automated Verification Suite (`# --- checks ---`)

#### 24. `check_sympy()`
- **Role**: Rigorous symbolic validation against SymPy exact calculus.
- **Mechanism**:
  - Defines symbolic variables `x, y, te, t0, s, cx, cy, L = sp.symbols(...)`.
  - Computes symbolic derivatives using `sp.diff` and evaluates via `.subs().evalf()`.
  - Tests off-axis points: Model A at $(3.0, 2.5)$ and Model B at $(1.0, 1.5)$ (guaranteeing non-zero values for all first and second partials).
  - Asserts that $T, T_x, T_y, T_{xx}, T_{yy}, T_{xy}$ match hand formulas within $10^{-5}$ tolerance. Prints `"MATCH"` for both models.

---

#### 25. `check_plate_calculus()`
- **Role**: Unit tests asserting mathematical correctness across plate calculus.
- **Assertions**:
  - Model A peak temperature $T(2, 2) = 85.0^\circ\text{C}$ and gradient $\approx \langle 0, 0 \rangle$.
  - Model A peak Hessian $T_{xx} = -60.0, T_{yy} = -60.0, T_{xy} = 0.0, D = 3600.0 \implies$ Local Maximum.
  - Model B peak $T(2, 2) = 70.0^\circ\text{C}$.
  - Model B D-test at $(1, 1) \implies$ `"Inconclusive"` (validates tolerance fix for $D \approx 0$).
  - Average temperature bounds: $45.0 < T_{\text{avg}} < 48.0$.
  - Tangent plane accuracy at $(2, 2)$ and off-center $(3, 2)$.
  - Taylor polynomial degree 2 accuracy near peak ($|Q(2.1, 2.1) - T(2.1, 2.1)| < 0.01$).

---

#### 26. `check_optimization()`
- **Role**: Unit tests asserting optimization, search, and cooling algorithms.
- **Assertions**:
  - Gradient descent cooling: $T_{\text{final}} < T_{\text{initial}}$.
  - First descent step distance $< 0.15\text{ cm}$ (validates unit-step formulation).
  - Peak search coordinates within $0.15\text{ cm}$ of $(2.0, 2.0)$ and temperature $\approx 85.0^\circ\text{C}$.
  - Risk classification boundaries for $50^\circ\text{C}$ (Low), $75^\circ\text{C}$ (Medium), $95^\circ\text{C}$ (High).
  - Text validation of cooling suggestions.
  - Best placement search accuracy, distance $> 0$, and fallback to `None` for impossible thresholds.

---

#### 27. `run_checks()`
- **Role**: Master automated test runner.
- **Execution**: Executes `check_plate_calculus()`, `check_optimization()`, and `check_sympy()`. Prints `"All checks passed"`.

---

### Part 5: Interactive Terminal Interface (`# --- console ---`)

#### 28. `show_menu()`
- **Role**: Displays the terminal menu choices:
  ```text
  --- CalSymPy Menu ---
  1. Model & params
  2. Heat map
  3. Point lookup
  4. Hottest point
  5. Average temp
  6. Gradient descent
  7. Save report
  8. Self-check (SymPy and asserts)
  0. Quit
  ```

---

#### 29. `ask_param(name, current_val)`
- **Role**: Robust numeric input prompt with error handling.
- **Safety Features**:
  - If user presses Enter without typing, returns `current_val`.
  - Catches `ValueError` if letters are typed, prints warning, and preserves `current_val`.
  - Enforces strictly positive values ($> 0$) for plate size $L$ and dispersion $s$, completely preventing `ZeroDivisionError`.

---

#### 30. `option_choose_model(plate)`
- **Role**: Handles Option 1 to switch between Model A and Model B and optionally modify parameters.

---

#### 31. `option_lookup(plate)`
- **Role**: Handles Option 3 to inspect coordinates $(x, y)$.
- **Validation**:
  - Checks $0 \le x, y \le L$; prints warning if out of bounds.
  - Evaluates $T, \nabla T, |\nabla T|, T_{xx}, T_{yy}, T_{xy}, D$.
  - If $|\nabla T| > 0.01$, explicitly notifies user: `"Not a critical point (the gradient is not zero), so the second derivative test does not apply here."`
  - If $|\nabla T| \le 0.01$, outputs classification (Local Maximum, Minimum, Saddle Point, or Inconclusive).

---

#### 32. `option_hottest(plate)`
- **Role**: Handles Option 4. Runs grid search, displays peak coordinates, temperature, risk level, and cooling suggestions.

---

#### 33. `option_average(plate)`
- **Role**: Handles Option 5. Evaluates 2D midpoint Riemann sum and prints spatial average temperature.

---

#### 34. `option_descent(plate)`
- **Role**: Handles Option 6. Prompts for start coordinates $(x_0, y_0)$, simulates downhill relocation, runs best placement search, and optionally displays descent path plot.

---

#### 35. `option_save_report(plate)`
- **Role**: Handles Option 7. Exports plate summary metrics to `report_A.csv`, `report_B.csv`, or `.txt`.
- **Fault Tolerance**: Wraps file writing in `try ... except (IOError, OSError)` to catch read-only file or permission errors gracefully without crashing.

---

#### 36. `main()`
- **Role**: Main program entry point. Initializes `Plate("A")` and runs the interactive menu loop until choice `"0"` is entered.

---

## 4. Web Application Architecture (`app.py`)

The Streamlit web interface (`app.py`) is designed with a strict **separation of concerns**:
- **Zero Embedded Calculus**: All mathematical evaluations, partial derivatives, double integrals, and optimization algorithms are executed by calling `calsympy.*`.
- **Resource Management**: Calls `plt.close(fig)` immediately after every `st.pyplot(fig)` call, preventing server memory leakage and Matplotlib figure accumulation warnings.
- **Mathematical Rendering**: Uses `st.latex()` to display analytical equations with LaTeX typography.
- **In-Memory CSV Download**: Uses `df.to_csv(index=False)` in RAM via `st.download_button`, preventing server disk write issues.

---

## 5. Summary Matrix: Mathematical Concepts & Implemented Functions

| Calculus Concept | Implemented In | Mathematical Significance |
| :--- | :--- | :--- |
| **Scalar Fields** | `temp_a`, `temp_b` | 2D temperature distribution $T: \mathbb{R}^2 \to \mathbb{R}$ |
| **Partial Derivatives** | `grad_a`, `grad_b`, `gradient` | Directional slopes along Cartesian axes $\frac{\partial T}{\partial x}, \frac{\partial T}{\partial y}$ |
| **Chain Rule & Product Rule** | `grad_a`, `hessian_a` | Analytical differentiation of composite Gaussian functions |
| **Gradient Vector & Norm** | `gradient` | Steepest ascent direction $\nabla T$ and maximum rate of increase $|\nabla T|$ |
| **Second Partial Derivatives** | `hessian_a`, `hessian_b` | Surface curvature and concavity ($T_{xx}, T_{yy}, T_{xy}$) |
| **Clairaut's Theorem** | `hessian_a`, `hessian_b` | Equality of mixed partials $T_{xy} = T_{yx}$ for smooth fields |
| **Second Derivative Test** | `second_derivative_test` | Critical point classification via discriminant $D = T_{xx}T_{yy} - T_{xy}^2$ |
| **Linear Approximation** | `tangent_plane` | Tangent plane $L(x, y) = T(a, b) + \nabla T \cdot \Delta \mathbf{r}$ |
| **Quadratic Approximation** | `taylor_degree_2` | Osculating paraboloid matching local curvature |
| **Double Integrals** | `average_temperature` | Spatial mean temperature $\frac{1}{\text{Area}}\iint_R T(x, y)\,dA$ |
| **2D Riemann Sums** | `average_temperature` | Numerical integration via midpoint grid discretization |
| **Gradient Descent** | `gradient_descent` | Downhill optimization stepping along $-\frac{\nabla T}{|\nabla T|}$ |
| **Constrained Optimization** | `find_best_placement` | Minimizing $\text{dist}(\mathbf{x}, \mathbf{x}_0)$ subject to $T(\mathbf{x}) < T_{\text{limit}}$ and $\mathbf{x} \in \text{margins}$ |
| **Symbolic Verification** | `check_sympy` | Automated proof that hand-derived formulas match exact symbolic calculus |
