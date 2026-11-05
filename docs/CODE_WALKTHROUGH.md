# CalSymPy — 10-Minute Demonstration Script (CODE_WALKTHROUGH.md)
**Project**: CalSymPy (Team 4, Delta-T) — MAT 112 Engineering Mathematics & Python  
**Role**: Presenter / Deployer Guide for live faculty and classroom demonstration.  
**Total Duration**: 10 Minutes (600 Seconds).

---

## Presentation Overview & Timing Breakdown

| Time Elapsed | Target Tab / Action | Core Calculus Concept |
| :--- | :--- | :--- |
| **0:00 – 1:00** | Introduction & Tab 1: Overview | Scalar fields $T(x,y)$, Gradient $\nabla T$, Hessian $D$-test |
| **1:00 – 2:00** | Tab 2: Point Inspector | Continuous evaluation, directional change, local linearity |
| **2:00 – 3:00** | Tab 3: Risk Assessment | Guardband thresholding & engineering communication |
| **3:00 – 4:00** | Tab 4: Compare Models | Boundary conditions: Dirichlet, Neumann, & mixed harmonics |
| **4:00 – 5:00** | Tab 5: Self-Test Panel | 37 theoretical benchmark verification checks at factory defaults |
| **5:00 – 6:00** | Tab 6: Heat Load & Energy | Double integrals $\iint T\,dA$, average temperature, trapezoid rule |
| **6:00 – 7:00** | Tab 7: Multi-Spot Hotspots | Multi-modal surfaces, dual peaks, and interior saddle points |
| **7:00 – 8:00** | Tab 8: Flux & Divergence | Fourier's Law $\mathbf{F} = -k\nabla T$ and field divergence $\operatorname{div} \mathbf{F} = -k\nabla^2 T$ |
| **8:00 – 9:00** | Tab 9: Performance Benchmark | Vectorized compiled NumPy vs symbolic SymPy substitution |
| **9:00 – 10:00** | Tab 10: Export & Optimization | Gradient descent source cooling, Lagrange rail extrema, and CSV export |

---

## Detailed Step-by-Step Walkthrough

### 1. Introduction & Overview (0:00 – 1:00)
- **Action**: Launch app via `python app.py`. Ensure the browser opens to **Tab 1: Overview** with default **Model A (Single Hotspot)**.
- **What to Click**: Adjust the **Scenario Preset** dropdown from *Idle* to *Normal* to *Heavy*. Point to the heatmap and the top risk badge updating from Green to Yellow to Red.
- **What to Say**: 
  > *"Good morning professors. CalSymPy is an interactive engineering tool designed to teach multivariable calculus through steady-state flat plate thermodynamics. On screen is Model A, representing a Gaussian microchip heat source on a 4-by-4 cm PCB. Notice that the Second Derivative Test independently evaluates the Hessian determinant $D = T_{xx} T_{yy} - (T_{xy})^2$. Because $D = 3600 > 0$ and $T_{xx} = -60 < 0$, the algorithm rigorously classifies the centre at $(2, 2)$ as an analytical local maximum peak reaching 85 °C."*
- **Calculus Concepts Shown**: Scalar field visualization, critical points ($\nabla T = \mathbf{0}$), concavity, and the Hessian discriminant $D$-test.

---

### 2. Tab 2: Point Inspector (1:00 – 2:00)
- **Action**: Click **Tab 2: Point Inspector**. Enter coordinate $x = 3.0$, $y = 2.0$.
- **What to Click**: Click anywhere on the plate or enter $(3.0, 2.0)$ in the coordinate boxes.
- **What to Say**: 
  > *"Moving away from the central chip to position $(3, 2)$ cm, we evaluate the continuous multivariable derivatives directly from our compiled functions. At this point, the temperature has dropped to 61.39 °C. The gradient vector is $\nabla T = \langle -36.39, 0.00 \rangle$ °C/cm. Because the gradient points in the direction of steepest temperature increase, its negative points rightward, showing that heat is conducting outward toward the right edge."*
- **Calculus Concepts Shown**: Gradient vector $\nabla T$, directional derivatives, and local linear approximation.

---

### 3. Tab 3: Risk Assessment (2:00 – 3:00)
- **Action**: Click **Tab 3: Risk Assessment**. Toggle between the *Idle* and *Heavy* scenarios in the sidebar.
- **What to Click**: Select **Heavy load** in the scenario preset.
- **What to Say**: 
  > *"Multivariable calculus is directly coupled to semiconductor reliability. Silicon junctions have typical thermal limits ($T_{j\text{Max}}$) around 95 to 105 °C. CalSymPy rounds temperatures to one decimal place to eliminate floating-point jitter and applies a 15 °C safety guardband. The system generates both an executive plain-English summary for non-technical managers and a technical engineering statement reporting exact thermal margins."*
- **Calculus Concepts Shown**: Continuous field bounding, mathematical rounding, and engineering safety margins.

---

### 4. Tab 4: Compare Models (3:00 – 4:00)
- **Action**: Click **Tab 4: Compare**. Click the **Refresh Cross-Model Comparison** button.
- **What to Click**: Point out the grouped bar chart and the pandas DataFrame below it.
- **What to Say**: 
  > *"In Tab 4, we compare all 5 plate configurations side-by-side using a structured pandas DataFrame. Notice Model C: it has zero edge gradient along all four boundaries because it models insulated Neumann boundary conditions ($\partial T/\partial n = 0$). In contrast, Model B has fixed cold edges, creating a steep edge gradient of 24.7 °C/cm that maximizes boundary heat dissipation."*
- **Calculus Concepts Shown**: Boundary value conditions (Dirichlet vs Neumann), normal derivatives $\partial T/\partial n$, and comparative multivariable metrics.

---

### 5. Tab 5: Theoretical Self-Test Panel (4:00 – 5:00)
- **Action**: Click **Tab 5: Self-Test**. Click **Run All Theoretical Self-Tests**.
- **What to Click**: Point to the status reading: `37 / 37 Checks Passed (ALL THEORETICAL KNOWN VALUES PASSED)`.
- **What to Say**: 
  > *"To ensure academic integrity, Tab 5 independently verifies 37 theoretical benchmark values derived by the engineering faculty. Most importantly, as highlighted on screen, this panel evaluates models strictly at factory default parameters, completely independent of current UI slider positions. Every check—including peak temperatures, vanishing gradients, negative Laplacians, and saddle determinants—passes with zero tolerance violations."*
- **Calculus Concepts Shown**: Analytical verification of stationary points, boundary conditions, and exact Hessian values.

---

### 6. Tab 6: Heat Load & Energy (5:00 – 6:00)
- **Action**: Click **Tab 6: Heat Load & Energy**. Select **FR-4 PCB** and then **Copper Plate**.
- **What to Click**: Point to the three reported average temperatures: Exact Double Integral, Plain Grid Mean, and Trapezoid-Rule Average.
- **What to Say**: 
  > *"Here we calculate the total thermal energy stored in the plate using double integration: $T_{\text{avg}} = \frac{1}{\text{Area}} \iint_R T(x, y)\,dA$, evaluated using `scipy.integrate.dblquad`. Notice that the plain grid mean (46.12 °C) slightly underestimates the exact integral (46.47 °C). This is because a plain grid counts cooler edge samples as full cells, whereas the continuous integral and the trapezoid rule (`np.trapezoid`) accurately weight edge points as half cells."*
- **Calculus Concepts Shown**: Double integrals $\iint_R T\,dA$, continuous mean value theorem, numerical quadrature, and specific heat energy storage.

---

### 7. Tab 7: Multi-Spot Hotspots (6:00 – 7:00)
- **Action**: In the sidebar model dropdown, select **Model D (Two Hotspots)**.
- **What to Click**: Show the dual-peak dashboard and point to the coordinates table.
- **What to Say**: 
  > *"Model D introduces a multi-modal thermal field created by two microchips. Our peak-finding algorithm detects both equal maxima near $(1.27, 1.27)$ and $(2.73, 2.73)$ at 71.69 °C. Even more interesting is the geometric midpoint at $(2.0, 2.0)$: here the first partial derivatives vanish ($\nabla T = \mathbf{0}$), but the Hessian discriminant is $D = -1846.6 < 0$. This confirms the presence of a saddle point between the two chips."*
- **Calculus Concepts Shown**: Multi-modal scalar fields, dual local extrema, and hyperbolic saddle points ($D < 0$).

---

### 8. Tab 8: Heat Flux & Vector Divergence (7:00 – 8:00)
- **Action**: Click **Tab 8: Heat Flux & Divergence**.
- **What to Click**: Point to the vector streamlines on the left and the diverging blue-white-red heatmap on the right.
- **What to Say**: 
  > *"Tab 8 visualizes Fourier’s Law of thermal conduction: $\mathbf{F} = -k \nabla T$. Streamlines trace the continuous path of heat flowing down the temperature gradient toward the colder edges. On the right, we plot the divergence of heat flux: $\operatorname{div} \mathbf{F} = -k \nabla^2 T$. Positive divergence (bright red) marks thermal sources where heat expands outward, while negative divergence (deep blue) marks thermal sinks where heat converges."*
- **Calculus Concepts Shown**: Vector fields, Fourier's Law, field divergence ($\nabla \cdot \mathbf{F}$), and the scalar Laplacian ($\nabla^2 T$).

---

### 9. Tab 9: Performance Benchmark (8:00 – 9:00)
- **Action**: Click **Tab 9: Benchmark**. Set grid resolution to $N = 25$ and click **Run Live Benchmark**.
- **What to Click**: Point to the measured execution seconds for SymPy versus NumPy and the speedup ratio.
- **What to Say**: 
  > *"This tab demonstrates why we cache symbolic calculus using `sp.lambdify`. Evaluating an $N \times N$ grid point-by-point with pure SymPy `.subs().evalf()` takes over a second of wall-clock time. In contrast, compiling once to vectorized NumPy array instructions evaluates the entire mesh in milliseconds, achieving over a 100x speedup while maintaining numerical agreement to within $10^{-10}$."*
- **Calculus Concepts Shown**: Computational complexity of symbolic expression graphs vs vectorized numerical array evaluation.

---

### 10. Tab 10: Optimization & Export (9:00 – 10:00)
- **Action**: Click **Tab 11: Gradient Descent**, run a relocation demo, then click **Tab 10: Export**.
- **What to Click**: Select **Coordinate Grid Data (.csv)** and click **Generate and Download Report**.
- **What to Say**: 
  > *"Finally, we explore advanced optimizations. Tab 11 uses Gradient Descent to relocate heat sources along $-\nabla T$, cooling sensitive sensors. Tab 12 solves constrained extrema along straight mounting rails using Lagrange Multipliers ($\nabla T = \lambda \nabla g$). All calculus data—including continuous coordinate grids ($x, y, T, T_x, T_y$) and summary audits—can be exported directly to CSV via pandas. Thank you, and we welcome your questions!"*
- **Calculus Concepts Shown**: Gradient descent unconstrained path optimization, Lagrange multipliers constrained optimization, and structured tabular data logging.
