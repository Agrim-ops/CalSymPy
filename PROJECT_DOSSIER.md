# CalSymPy — Complete Project Dossier & Claude Handover Document
**Project**: CalSymPy (Team 4, Delta-T)  
**Academic Course**: MAT 112 Engineering Mathematics & Python Programming  
**Level**: First-Year Undergraduate Engineering College Project  
**Local Workspace**: `E:\Study\Projects\calsympy`  
**GitHub Repository**: `https://github.com/Agrim-ops/CalSymPy` (branch: `main`)  
**Python Runtime**: Python 3.12.10 (tested and verified in `.venv312`)  

---

## 1. Project Overview & Identity

CalSymPy is an educational analytical Python tool developed by Team 4 (Delta-T) for first-year engineering students and faculty. It models steady-state temperature distributions $T(x, y)$ on a flat square plate (side length $L = 4\text{ cm}$), analyzes the scalar and vector fields using multivariable differential and integral calculus, and provides risk-based cooling recommendations for electronic components.

The software is designed specifically for presentation to **Mathematics and Python faculty**. As a pedagogical requirement:
- Every line of code is simple, readable, and structured at a first-year college level.
- No obscure Python idioms or "clever tricks" are used.
- Every mathematical step is explained in plain-English comments directly above the calculus operations.
- All team members are able to explain the underlying calculus and programming logic.

---

## 2. Hard Syllabus Constraints (MAT 112 Only)

The project adheres strictly to the first-year MAT 112 syllabus constraints:

1. **Pure Spatial Steady-State ($T(x, y)$ Only)**:
   - **Strictly Forbidden**: The heat equation ($\frac{\partial T}{\partial t} = \alpha \nabla^2 T$), any partial differential equation (PDE), time dependence ($t$), time-stepping loops, finite difference methods, or numerical PDE solvers.
   - Temperature depends solely on spatial position: $T(x, y)$.

2. **Permitted Mathematical Topics**:
   - First partial derivatives: $T_x = \frac{\partial T}{\partial x}$, $T_y = \frac{\partial T}{\partial y}$.
   - Gradient vector field: $\nabla T(x, y) = \left\langle \frac{\partial T}{\partial x}, \frac{\partial T}{\partial y} \right\rangle$.
   - Direction of maximum temperature change ($|\nabla T| = \sqrt{T_x^2 + T_y^2}$).
   - Fourier's law of heat conduction: $\mathbf{F} = -k \nabla T$ (heat flows hot $\to$ cold down the negative gradient).
   - Second partial derivatives: $T_{xx} = \frac{\partial^2 T}{\partial x^2}$, $T_{yy} = \frac{\partial^2 T}{\partial y^2}$, $T_{xy} = \frac{\partial^2 T}{\partial x \partial y}$ (Clairaut's theorem: $T_{xy} = T_{yx}$).
   - Second derivative test (Hessian discriminant): $D = T_{xx} T_{yy} - (T_{xy})^2$.
     - $D > 0 \text{ and } T_{xx} < 0 \implies$ **True Maximum** (hotspot peak)
     - $D > 0 \text{ and } T_{xx} > 0 \implies$ **True Minimum** (cold spot)
     - $D < 0 \implies$ **Saddle Point** (thermal pass)
     - $D = 0 \implies$ **Inconclusive**
   - Divergence of heat flux vector field: $\operatorname{div} \mathbf{F} = \nabla \cdot \mathbf{F} = -k(T_{xx} + T_{yy}) = -k \nabla^2 T$.
     - $\operatorname{div} \mathbf{F} > 0 \implies$ net outflow (**Heat Source**)
     - $\operatorname{div} \mathbf{F} < 0 \implies$ net inflow (**Heat Sink**)
   - Double integrals: $\iint_R T(x, y)\,dA$ to find continuous average temperature and stored thermal energy.
   - Two-variable Taylor polynomial approximations:
     $$T(x, y) \approx T(a, b) + T_x(a, b)(x - a) + T_y(a, b)(y - b) + \frac{1}{2}\left[T_{xx}(a, b)(x - a)^2 + 2T_{xy}(a, b)(x - a)(y - b) + T_{yy}(a, b)(y - b)^2\right]$$
   - Constrained optimization via **Lagrange Multipliers**: $\nabla T = \lambda \nabla g$ along linear mounting rails $g(x, y) = ax + by - c = 0$.
   - Optimization via **Gradient Descent**: Minimizing sensor exposure by relocating heat sources along $-\nabla T$.

3. **Permitted Software Libraries**:
   - `numpy==2.5.3` (array math, grid coordinate evaluation, numerical trapezoid rule)
   - `sympy==1.14.0` (symbolic differentiation and lambdification caching)
   - `matplotlib==3.11.2` (2D temperature heatmaps, streamlines, divergence maps, optimization paths)
   - `scipy==1.18.1` (strictly `scipy.integrate.dblquad` only)
   - `gradio==6.31.0` (interactive browser GUI using built-in components only: `Blocks`, `Tabs`, `Dropdown`, `Slider`, `Number`, `Plot`, `Markdown`, `Dataframe`, `Button`, `File`, `Radio`)
   - `pytest==9.2.0` (comprehensive automated test suite)
   - **Zero custom HTML/CSS/JavaScript in the UI.**

4. **Performance Architecture**:
   - Symbolic derivatives ($T_x, T_y, T_{xx}, T_{yy}, T_{xy}, \nabla^2 T$) and vectorized callable functions (`sp.lambdify`) are compiled and cached **once per model at startup**.
   - No symbolic differentiation is ever executed during user slider movements or UI interactions.

---

## 3. Mathematical Models & Closed-Form Formulations

Plate geometry: Square domain $R = [0, L] \times [0, L]$ with side length default $L = 4\text{ cm}$.

### Model A: Single Hotspot (Centered Localized Heat Source)
$$T(x, y) = T_{\text{edge}} + T_0 \exp\left(-\frac{(x - c_x)^2 + (y - c_y)^2}{s}\right)$$
- **Default Parameters**: $T_{\text{edge}} = 25.0^\circ\text{C}$, $T_0 = 60.0^\circ\text{C}$, $s = 2.0\text{ cm}^2$, $c_x = 2.0\text{ cm}$, $c_y = 2.0\text{ cm}$, $L = 4.0\text{ cm}$.
- **Calculus Properties**:
  - Hotspot peak at $(2.0, 2.0)$: $T = 85.0^\circ\text{C}$, $T_x = T_y = 0$, $T_{xx} = T_{yy} = -60.0$, $T_{xy} = 0$, $D = 3600.0 > 0 \implies$ True Maximum. Laplacian $\nabla^2 T = -120.0$.
  - At $(3.0, 2.0)$: $T = 61.39^\circ\text{C}$, $T_x = -36.39^\circ\text{C/cm}$, $T_y = 0^\circ\text{C/cm}$.
  - At $(3.0, 3.0)$: $T = 47.07^\circ\text{C}$, $T_x = T_y = -22.07^\circ\text{C/cm}$, $|\nabla T| = 31.22^\circ\text{C/cm}$.

### Model B: Fixed Cold Edges (Dirichlet Boundary Conditions)
$$T(x, y) = T_{\text{edge}} + T_0 \sin\left(\frac{\pi x}{L}\right) \sin\left(\frac{\pi y}{L}\right)$$
- **Default Parameters**: $T_{\text{edge}} = 20.0^\circ\text{C}$, $T_0 = 50.0^\circ\text{C}$, $L = 4.0\text{ cm}$.
- **Calculus Properties**:
  - All four boundary edges ($x=0, x=L, y=0, y=L$) evaluate to exactly $T_{\text{edge}} = 20.0^\circ\text{C}$.
  - Hotspot peak at plate center $(2.0, 2.0)$: $T = 70.0^\circ\text{C}$ (classified as `MODERATE RISK`).
  - At $(1.0, 2.0)$: $T = 55.36^\circ\text{C}$, $T_x = 27.77^\circ\text{C/cm}$, $T_y = 0^\circ\text{C/cm}$.

### Model C: Sealed Edges (Smooth Zero Normal Flux)
$$T(x, y) = T_{\text{edge}} + T_0 \sin^2\left(\frac{\pi x}{L}\right) \sin^2\left(\frac{\pi y}{L}\right)$$
- **Default Parameters**: $T_{\text{edge}} = 40.0^\circ\text{C}$, $T_0 = 30.0^\circ\text{C}$, $L = 4.0\text{ cm}$.
- **Calculus Properties**:
  - Normal derivatives smoothly vanish on all 4 boundaries: $\left.\frac{\partial T}{\partial x}\right|_{x=0, L} = 0$ and $\left.\frac{\partial T}{\partial y}\right|_{y=0, L} = 0$.
  - Boundary edge temperature is identically $T_{\text{edge}} = 40.0^\circ\text{C}$.
  - Peak at center $(2.0, 2.0)$: $T = 70.0^\circ\text{C}$ (classified as `MODERATE RISK`).

### Model C2: True Insulated Edges (Neumann Boundary Condition $\partial T/\partial n = 0$)
$$T(x, y) = T_{\text{edge}} + T_0 \cos\left(\frac{\pi x}{L}\right) \cos\left(\frac{\pi y}{L}\right)$$
- **Default Parameters**: $T_{\text{edge}} = 40.0^\circ\text{C}$, $T_0 = 30.0^\circ\text{C}$, $L = 4.0\text{ cm}$.
- **Calculus Properties**:
  - Normal derivatives vanish identically everywhere along boundaries: $T_x = 0$ along $x=0$ and $x=L$; $T_y = 0$ along $y=0$ and $y=L$.
  - Peaks are located at the **corners** $(0,0), (4,0), (0,4), (4,4)$ with $T = 70.0^\circ\text{C}$.
  - The center $(2.0, 2.0)$ is a **saddle point**: $T = 40.0^\circ\text{C}$, $T_x = T_y = 0$, $D = -34.70 < 0$.
  - At $(1.0, 1.0)$: $T = 55.0^\circ\text{C}$, $T_x = T_y = -11.78^\circ\text{C/cm}$.
  - Continuous double integral: Because $\int_0^L \cos\left(\frac{\pi x}{L}\right)dx = 0$, the exact continuous average temperature is **identically $40.00^\circ\text{C}$**.

### Model D: Dual Hotspots (Two Nearby Microchips)
$$T(x, y) = T_{\text{edge}} + T_1 \exp\left(-\frac{(x - c_{x1})^2 + (y - c_{y1})^2}{s_1}\right) + T_2 \exp\left(-\frac{(x - c_{x2})^2 + (y - c_{y2})^2}{s_2}\right)$$
- **Default Parameters**: $T_{\text{edge}} = 25.0^\circ\text{C}$, $T_1 = 45.0^\circ\text{C}$, $s_1 = 1.5\text{ cm}^2$, $(c_{x1}, c_{y1}) = (1.2, 1.2)$, $T_2 = 45.0^\circ\text{C}$, $s_2 = 1.5\text{ cm}^2$, $(c_{x2}, c_{y2}) = (2.8, 2.8)$, $L = 4.0\text{ cm}$.
- **Verbatim Calculus Values**:
  - **Saddle Point at Center $(2.000, 2.000)\text{ cm}$**:
    $$T = 63.34^\circ\text{C}\quad (63.3393^\circ\text{C})$$
    $$T_x = 0.0000^\circ\text{C/cm},\quad T_y = 0.0000^\circ\text{C/cm}$$
    $$T_{xx} = -7.50\ (-7.4975),\quad T_{yy} = -7.50\ (-7.4975),\quad T_{xy} = 43.62\ (43.6216)$$
    $$D = T_{xx}T_{yy} - T_{xy}^2 = (-7.4975)^2 - (43.6216)^2 = -1846.6\ (-1846.6355) < 0 \implies \mathbf{Saddle\ Point}$$
  - **Dual Equal Maxima (Peaks)**:
    - Peak 1 at $(1.267, 1.267)\text{ cm}$: $T = 71.69^\circ\text{C}$ ($71.692^\circ\text{C}$), $T_{xx} = -53.70$, $T_{yy} = -53.70$, $T_{xy} = 8.56$, $D = 2810.45 > 0, T_{xx} < 0 \implies \mathbf{True\ Maximum}$.
    - Peak 2 at $(2.733, 2.733)\text{ cm}$: $T = 71.69^\circ\text{C}$ ($71.692^\circ\text{C}$), $T_{xx} = -53.70$, $T_{yy} = -53.70$, $T_{xy} = 8.56$, $D = 2810.45 > 0, T_{xx} < 0 \implies \mathbf{True\ Maximum}$.
  - **Near-Hotspot Benchmark Point at $(1.3, 1.3)\text{ cm}$**:
    $$T(1.3, 1.3) = 71.644^\circ\text{C}\quad (\text{tested with strict tolerance } 10^{-3})$$

---

## 4. Key Functional Modules & Implementation Details

### A. Peak Finding & Hessian Discriminant Classification (`features.py` & `calculus.py`)
- Discretizes plate on a uniform evaluation grid.
- Identifies local candidate maxima and clusters tied peaks (e.g., corners for Model C2, twin peaks for Model D).
- Applies 2D Newton-Raphson gradient root-finding to locate exact continuous peak coordinates.
- Evaluates the MAT 112 Hessian discriminant $D = T_{xx}T_{yy} - T_{xy}^2$ and reports status in plain language.

### B. Risk Assessment Heuristics (`risk.py`)
- **Threshold Engineering Origin**:
  - Cutoffs are project design heuristics informed by commercial semiconductor junction thermal limits (Intel/AMD $T_{j\max} \approx 95\text{--}105^\circ\text{C}$, maintaining a safety guardband of $\sim 15^\circ\text{C}$). They are engineering heuristics, not official regulatory standards.
- **Rules (evaluated after rounding temperature to 1 decimal place)**:
  - **LOW RISK**: $T < 70.0^\circ\text{C}$ (Badge: `🟢 LOW RISK`).
    - *Non-Technical*: "This component is running at a safe temperature. No action needed right now."
    - *Technical*: Operates with $>25^\circ\text{C}$ margin below $T_{j\max}$. No throttling expected.
  - **MODERATE RISK**: $70.0^\circ\text{C} \le T \le 90.0^\circ\text{C}$ (Badge: `🟡 MODERATE RISK`).
    - *Non-Technical*: "This part is running warmer than ideal. It's not an emergency, but it's worth adding some cooling soon - cheaper to prevent now than repair later."
    - *Technical*: Thermal headroom constricted ($\sim 5\text{--}25^\circ\text{C}$ margin). Wear accelerated.
  - **HIGH RISK**: $T > 90.0^\circ\text{C}$ (Badge: `🔴 HIGH RISK`).
    - *Non-Technical*: "This part is running dangerously hot. If nothing changes it will likely slow down or fail, which usually costs more to fix later than to prevent now."
    - *Technical*: Dangerously close to or exceeding $T_{j\max}$. High risk of shutdown or damage.
- **Operating Scenario Presets**:
  - Presets (Idle $\approx 55^\circ\text{C} \implies$ LOW, Normal $\approx 80^\circ\text{C} \implies$ MODERATE, Heavy $\approx 100^\circ\text{C} \implies$ HIGH) are tailored per model based on baseline edge temperatures:

| Model | Preset | $T_0$ / Amplitude ($^\circ\text{C}$) | Peak Temp ($^\circ\text{C}$) | Risk Badge |
|---|---|---|---|---|
| **A** | Idle | 30.0 | 55.00 | 🟢 LOW RISK |
| **A** | Normal | 55.0 | 80.00 | 🟡 MODERATE RISK |
| **A** | Heavy | 75.0 | 100.00 | 🔴 HIGH RISK |
| **B** | Idle | 35.0 | 55.00 | 🟢 LOW RISK |
| **B** | Normal | 60.0 | 80.00 | 🟡 MODERATE RISK |
| **B** | Heavy | 80.0 | 100.00 | 🔴 HIGH RISK |
| **C** | Idle | 15.0 | 55.00 | 🟢 LOW RISK |
| **C** | Normal | 40.0 | 80.00 | 🟡 MODERATE RISK |
| **C** | Heavy | 60.0 | 100.00 | 🔴 HIGH RISK |
| **C2** | Idle | 15.0 | 55.00 | 🟢 LOW RISK |
| **C2** | Normal | 40.0 | 80.00 | 🟡 MODERATE RISK |
| **C2** | Heavy | 60.0 | 100.00 | 🔴 HIGH RISK |
| **D** | Idle | 29.0 | 55.09 | 🟢 LOW RISK |
| **D** | Normal | 53.0 | 79.99 | 🟡 MODERATE RISK |
| **D** | Heavy | 72.3 | 100.02 | 🔴 HIGH RISK |

### C. Double Integrals & Thermal Energy Load (`features.py`)
- Evaluates exact continuous average temperature:
  $$T_{\text{avg}} = \frac{1}{\text{Area}} \iint_R T(x, y)\,dA = \frac{1}{L^2} \int_0^L \int_0^L T(x, y)\,dy\,dx$$
  via `scipy.integrate.dblquad`.
- Evaluates discrete $81 \times 81$ grid mean and trapezoidal numerical integration via `np.trapezoid`.
- **Explanation of the gap**: *"The plain mean counts the cooler edge points as full cells, while integration and the trapezoid rule count them as half cells (and corner points as quarter cells)."*
- **Stored Thermal Energy relative to ambient ($T_{\text{amb}} = 25.0^\circ\text{C}$)**:
  $$E = \rho c_p h \iint_R (T(x, y) - T_{\text{ambient}})\,dA \quad \text{[Joules]}$$
  - Materials supported:
    - **FR-4 PCB**: Density $\rho = 1850\text{ kg/m}^3$, thickness $h = 1.6\text{ mm}$, thermal conductivity $k = 0.29\text{ W/(m}\cdot\text{K)}$, specific heat capacity $c_p \approx 1100\text{ J/(kg}\cdot\text{K)}$ (*explicitly labeled as approximate, typical range 1000–1200*).
    - **Copper Plate**: $\rho = 8960\text{ kg/m}^3$, $h = 1.6\text{ mm}$, $k = 385.0\text{ W/(m}\cdot\text{K)}$, $c_p = 385.0\text{ J/(kg}\cdot\text{K)}$.
- For Model A default FR-4: Exact continuous average is $46.47^\circ\text{C}$, discrete mean is $46.06^\circ\text{C}$, trapezoid average is $46.46^\circ\text{C}$, and stored thermal energy is **$111.83\text{ J}$** ($\approx 112\text{ J}$).

### D. Heat Flux Streamlines & Divergence Field (`plots.py` & `features.py`)
- Heat flux vector field by Fourier's law: $\mathbf{F} = -k \nabla T = \left\langle -k T_x, -k T_y \right\rangle$.
- Matplotlib `streamplot` visualizes heat flowing from high to low temperatures.
- Divergence scalar field: $\operatorname{div}\mathbf{F} = -k \nabla^2 T = -k (T_{xx} + T_{yy})$.
  - Plotted with a diverging colormap (`bwr` centered at 0): red denotes heat sources ($\operatorname{div}\mathbf{F} > 0$), blue denotes heat sinks ($\operatorname{div}\mathbf{F} < 0$).
- Fixed shared color scale: Temperature heatmaps utilize a uniform $[20, 120]^\circ\text{C}$ range across all models so that high-risk cases never clip or visually distort.

### E. Advanced Calculus Optimizations (`features.py`)
1. **Gradient Descent Source Relocation**:
   - Given a heat-sensitive chip at $(x_s, y_s)$, relocates the thermal heat source center $(c_x, c_y)$ iteratively along the negative gradient $-\nabla T$ to achieve maximum passive cooling.
   - Constrained within plate interior safety margins.
2. **Lagrange Multipliers for Mounting Rail Extrema**:
   - Identifies hottest and coldest points along a physical straight mounting rail $g(x, y) = ax + by - c = 0$.
   - Solves the Lagrange multiplier equation system $\nabla T = \lambda \nabla g \implies T_x b - T_y a = 0$ symbolically using SymPy, and cross-checks against a dense 1D line numerical search.

### F. Factory-Defaults Self-Test Suite (`selftest.py`)
- Independent verification panel that evaluates theoretical known values strictly at factory defaults, regardless of UI slider positions.
- **34 distinct calculus and thermal checks**:
  - Model A: $T(2,2)=85$, $T_x=0$, $T_y=0$, $T_{xx}=-60$, $T_{yy}=-60$, $T(3,2)=61.39$, $T_x=-36.39$, $T_y=0$, $T(3,3)=47.07$, $T_x=-22.07$, $T_y=-22.07$, $|\nabla T|=31.22$.
  - Model B: Edges evaluate to 20, center $T(2,2)=70$, $T(1,2)=55.36$, $T_x=27.77$, $T_y=0$.
  - Model C: Edge temperatures equal 40, normal derivatives vanish on all 4 boundaries.
  - Model C2: Corner peaks at 70, center saddle at 40, $T(1,1)=55$, $T_x=T_y=-11.78$, normal derivatives vanish along $x=0,4$ and $y=0,4$.
  - Model D: Peak near $(1.267, 1.267)$ at $71.69^\circ\text{C}$, saddle at $(2, 2)$ at $63.34^\circ\text{C}$ ($D = -1846.6$), near-hotspot at $(1.3, 1.3)$ at $71.644^\circ\text{C}$.
- **Status**: **34 / 34 Checks Passed (100% PASS)**.

### G. Symbolic vs Lambdified Benchmark (`benchmark.py`)
- Compares computational execution time for evaluating an $N \times N$ coordinate grid ($N=25 \implies 625$ points):
  - Pure SymPy dictionary substitution (`.subs()`): $\approx 0.164\text{ s}$
  - Vectorized lambdified NumPy function: $\approx 0.000059\text{ s}$ ($59\ \mu\text{s}$)
  - Speedup factor: **$\approx 2800\times$ faster**.
  - Accuracy: Numerical agreement verified with maximum absolute difference $< 10^{-12}$.
  - Test assertions use relative comparisons (`numpy_seconds < sympy_seconds`) to avoid brittle hardware timing assumptions.

### H. Export Engine (`report.py`)
- Generates downloadable formatted `.txt` comprehensive technical reports and `.csv` numerical grid spreadsheets timestamped in UTC.

### I. Interactive Web UI (`app.py`)
- Built strictly with native Gradio components across **10 structured tabs**:
  1. **Overview**: 2D Matplotlib temperature distribution and heat flux vector map.
  2. **Risk**: Prominent status badge (`LOW`, `MODERATE`, `HIGH`), plain-English HR summary, and technical engineering analysis.
  3. **Calculus Checks**: Exact Hessian curvatures, discriminant $D$, critical point classification, and continuous point lookup.
  4. **Compare**: Bar chart and tabular comparison of peak $T$, average $T$, and boundary edge dissipation rates across all 5 models.
  5. **Heat Load**: Double integration continuous average, discrete grid mean, trapezoid-rule average, and stored energy in Joules.
  6. **Heat Flow**: Vector heat flux streamlines ($\mathbf{F} = -k\nabla T$) and divergence source/sink maps.
  7. **Optimiser**: Interactive gradient descent source relocation and Lagrange multipliers rail extrema.
  8. **Self-Test**: Interactive button running the 34-check factory defaults matrix.
  9. **Benchmark**: Interactive timer demonstrating symbolic caching speedup.
  10. **Export**: One-click download of `.txt` and `.csv` analytical reports.

---

## 5. File Inventory & Repository Structure

Local path: `E:\Study\Projects\calsympy\`

```text
E:\Study\Projects\calsympy\
├── .git/                                # Git version control metadata (3 commits, origin remote)
├── .gitignore                           # Merged GitHub Python + project-specific ignore rules
├── .venv312/                            # Clean Python 3.12.10 virtual environment
├── README.md                            # Hugging Face Space metadata + MAT 112 syllabus documentation
├── LICENSE                              # MIT License (Agrim Goel)
├── requirements.txt                     # Pinned reproducible dependencies
├── pytest.ini                           # Pytest configuration (pythonpath = .)
├── app.py                               # Gradio 10-tab web application (521 lines)
├── models.py                            # Models A, B, C, C2, D with SymPy differentiation & lambdify cache
├── calculus.py                          # Pure MAT 112 calculus engine (gradient, Hessian, D-test, divergence)
├── features.py                          # Domain calculations (peaks, lookup, compare, dblquad, optimizers)
├── plots.py                             # Matplotlib visualizers (closed figures, fixed 20-120 °C scale)
├── risk.py                              # Risk categorization, badges, technical and non-technical text
├── selftest.py                          # 34-check theoretical known-values verification panel
├── benchmark.py                         # SymPy substitution vs lambdified NumPy execution timer
├── report.py                            # Formatted text and CSV report generation
├── notebooks/
│   └── colab_backup.ipynb               # Complete 18-cell self-contained Google Colab backup notebook
└── tests/                               # 39 unit tests across 11 test files
    ├── test_feature1_hottest.py         # Tests peak finder, ties, and second derivative classifications
    ├── test_feature2_lookup.py          # Tests continuous point lookup against known points
    ├── test_feature3_risk.py            # Tests risk boundaries, rounding, and all 15 scenario presets
    ├── test_feature4_selftest.py        # Tests self-test panel and defaults independence
    ├── test_feature5_compare.py         # Tests cross-model comparative calculus metrics
    ├── test_feature6_integral.py        # Tests dblquad, trapezoid rule, energy, and FR-4 cp flag
    ├── test_feature7_multispot.py       # Tests Model D saddle, dual peaks, and exact derivatives
    ├── test_feature8_heatflow.py        # Tests Fourier's law direction and divergence sources/sinks
    ├── test_feature9_benchmark.py       # Tests benchmark execution and numerical equivalence
    ├── test_feature10_export.py         # Tests text and CSV report file creation
    └── test_feature11_optimiser.py      # Tests gradient descent and Lagrange rail extrema
```

---

## 6. Automated Test Suite Results

Tested with `pytest-9.2.0` on **Python 3.12.10** under `E:\Study\Projects\calsympy\.venv312`:
- **Result**: **39 passed in 11.14s (100% pass rate)**.
- Summary of verified assertions:
  - Exact analytical agreement across all 5 models (A, B, C, C2, D).
  - Model C2 exact continuous integral equals $40.00^\circ\text{C}$ identically.
  - Model C2 tied corner peaks handled without center misclassification.
  - Model D dual maxima ($71.69^\circ\text{C}$, $D = 2810.45$) and saddle point ($63.34^\circ\text{C}$, $D = -1846.6$) verified to $0.01$ tolerance.
  - Risk boundary conditions verified at $69.9^\circ\text{C}$ (LOW), $70.0^\circ\text{C}$ (MODERATE), $90.0^\circ\text{C}$ (MODERATE), and $90.1^\circ\text{C}$ (HIGH).
  - All 15 model-preset combinations verified to yield intended risk badges.
  - Trapezoid-rule grid mean verified within $0.01^\circ\text{C}$ of continuous double integral.
  - Fourier heat flux verified to flow strictly opposite to thermal gradient ($\mathbf{F} \cdot \nabla T < 0$).

---

## 7. Current Git & Deployment State

- **Local Branch**: `main`
- **Remote**: `origin` $\to$ `https://github.com/Agrim-ops/CalSymPy.git`
- **Git Commit Graph**:
  ```text
  *   edcc3e0 Merge remote origin/main: add LICENSE and combine .gitignore rules, keeping local README.md
  |\  
  | * d453091 Initial commit (remote initial commit with MIT LICENSE)
  * 1ac5f9f Apply verification fixes (Python 3.12, trapezoid load, Model D tests and precision)
  * 1526452 Initial commit of CalSymPy: Flat Plate Thermal Calculus Analysis Tool (Team 4, Delta-T)
  ```
- **Deployment & Execution**:
  - The working directory is clean.
  - All files are staged and committed locally.
  - To push these commits live to GitHub, run in an interactive terminal on the host machine:
    ```powershell
    cd E:\Study\Projects\calsympy
    git push -u origin main
    ```
    Git Credential Manager will open the browser sign-in window for GitHub authentication.
