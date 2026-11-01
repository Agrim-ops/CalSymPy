---
title: CalSymPy Flat Plate Thermal Calculus
emoji: 🔥
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: 6.31.0
python_version: "3.11"
app_file: app.py
pinned: false
---

# CalSymPy — Flat Plate Thermal Calculus Analysis
**Team 4, Delta-T | MAT 112 Engineering Mathematics & Python**

CalSymPy is an educational analytical Python tool developed by Team 4 (Delta-T) for first-year engineering students and faculty. It models steady-state temperature distributions $T(x, y)$ on a flat square plate (side length $L = 4\text{ cm}$), analyzes the scalar and vector fields using multivariable calculus, and provides risk-based cooling recommendations.

---

## 1. Syllabus & Mathematical Foundations (MAT 112)

CalSymPy adheres strictly to the MAT 112 syllabus:
- **No Heat Equation or Numerical PDEs**: Temperature is modeled as a purely spatial scalar field $T(x, y)$ in steady-state. There is no time variable $t$, no $\partial T/\partial t$, and no time-stepping solvers.
- **First Partial Derivatives & Gradient**:
  $$\nabla T(x, y) = \left\langle \frac{\partial T}{\partial x}, \frac{\partial T}{\partial y} \right\rangle$$
  The gradient points in the direction of steepest temperature increase; its Euclidean magnitude $|\nabla T| = \sqrt{T_x^2 + T_y^2}$ represents the maximum rate of temperature change per centimetre.
- **Fourier's Law of Heat Conduction**: Heat flows down the thermal gradient (from hot to cold):
  $$\mathbf{F} = -k \nabla T = \left\langle -k \frac{\partial T}{\partial x}, -k \frac{\partial T}{\partial y} \right\rangle$$
  where $k$ is thermal conductivity ($0.29\text{ W/(m}\cdot\text{K)}$ for FR-4 PCB, $385\text{ W/(m}\cdot\text{K)}$ for Copper).
- **Second Partial Derivatives & Discriminant Test (D-Test)**:
  $$D = T_{xx} T_{yy} - (T_{xy})^2$$
  - $D > 0 \text{ and } T_{xx} < 0 \implies$ **True Maximum** (peak hotspot)
  - $D > 0 \text{ and } T_{xx} > 0 \implies$ **True Minimum** (cold spot)
  - $D < 0 \implies$ **Saddle Point** (mountain pass)
  - $D = 0 \implies$ **Inconclusive**
- **Divergence of Heat Flux**:
  $$\operatorname{div} \mathbf{F} = \nabla \cdot \mathbf{F} = -k (T_{xx} + T_{yy}) = -k \nabla^2 T$$
  - $\operatorname{div} \mathbf{F} > 0$: Net heat outflow $\implies$ **Heat Source**
  - $\operatorname{div} \mathbf{F} < 0$: Net heat inflow $\implies$ **Heat Sink**
- **Double Integrals**:
  - Exact Average Temperature:
    $$T_{\text{avg}} = \frac{1}{\text{Area}} \iint_R T(x, y)\,dA = \frac{1}{L^2} \int_0^L \int_0^L T(x, y)\,dy\,dx$$
    Evaluated continuously via `scipy.integrate.dblquad`.
  - Stored Thermal Energy relative to ambient ($T_{\text{ambient}} = 25^\circ\text{C}$):
    $$E = \rho \, c_p \, \tau \iint_R (T(x, y) - T_{\text{ambient}})\,dA \quad \text{[Joules]}$$
- **Optimization**:
  - **Gradient Descent**: Moving heat source position $(c_x, c_y)$ along $-\nabla_{\mathbf{c}} T_{\text{sensor}}$ to cool a sensitive sensor at $(x_s, y_s)$ within plate margins.
  - **Lagrange Multipliers**: Maximizing temperature along a straight mounting rail $g(x, y) = ax + by - c = 0$ using $\nabla T = \lambda \nabla g$.

---

## 2. Supported Thermal Models

1. **Model A (Single Hotspot)**:
   $$T(x, y) = T_{\text{edge}} + T_0 \exp\left(-\frac{(x - c_x)^2 + (y - c_y)^2}{s}\right)$$
   *Defaults*: $T_{\text{edge}} = 25^\circ\text{C}, T_0 = 60^\circ\text{C}, s = 2.0\text{ cm}^2, c_x = 2.0, c_y = 2.0, L = 4.0\text{ cm}$. Peak $= 85.0^\circ\text{C}$.
2. **Model B (Fixed Cold Edges)**:
   $$T(x, y) = T_{\text{edge}} + T_0 \sin\left(\frac{\pi x}{L}\right) \sin\left(\frac{\pi y}{L}\right)$$
   *Defaults*: $T_{\text{edge}} = 20^\circ\text{C}, T_0 = 50^\circ\text{C}, L = 4.0\text{ cm}$. Peak $= 70.0^\circ\text{C}$ at centre $(2, 2)$.
3. **Model C (Sealed Edges)**:
   $$T(x, y) = T_{\text{edge}} + T_0 \sin^2\left(\frac{\pi x}{L}\right) \sin^2\left(\frac{\pi y}{L}\right)$$
   *Defaults*: $T_{\text{edge}} = 40^\circ\text{C}, T_0 = 30^\circ\text{C}, L = 4.0\text{ cm}$. Peak $= 70.0^\circ\text{C}$ at centre $(2, 2)$. Normal derivatives vanish along all boundaries.
4. **Model C2 (True Insulated Edges)**:
   $$T(x, y) = T_{\text{edge}} + T_0 \cos\left(\frac{\pi x}{L}\right) \cos\left(\frac{\pi y}{L}\right)$$
   *Defaults*: $T_{\text{edge}} = 40^\circ\text{C}, T_0 = 30^\circ\text{C}, L = 4.0\text{ cm}$. Tied peak corners at $(0, 0)$ and $(4, 4)$ at $70.0^\circ\text{C}$ ($D > 0, T_{xx} < 0$). Center $(2, 2)$ is a saddle point ($D < 0$).
5. **Model D (Two Hotspots)**:
   $$T(x, y) = 25 + 45\exp\left(-\frac{(x - 1.2)^2 + (y - 1.2)^2}{1.5}\right) + 45\exp\left(-\frac{(x - 2.8)^2 + (y - 2.8)^2}{1.5}\right)$$
   *Defaults*: Peak near $(1.27, 1.27)$ at $\approx 71.7^\circ\text{C}$.

---

## 3. Risk Classification Translation

Evaluated after rounding temperature to 1 decimal place:
- **LOW ($T < 70.0^\circ\text{C}$)**:
  - *Plain-English*: *"This component is running at a safe temperature. No action needed right now."*
  - *Technical*: Safely below $70^\circ\text{C}$, maintaining $>25^\circ\text{C}$ operating margin below typical semiconductor junction limit (TjMax ~95–105 °C).
- **MODERATE ($70.0^\circ\text{C} \le T \le 90.0^\circ\text{C}$)**:
  - *Plain-English*: *"This part is running warmer than ideal. It's not an emergency, but it's worth adding some cooling soon - cheaper to prevent now than repair later."*
  - *Technical*: Reduced thermal headroom (~5–25 °C margin below TjMax).
- **HIGH ($T > 90.0^\circ\text{C}$)**:
  - *Plain-English*: *"This part is running dangerously hot. If nothing changes it will likely slow down or fail, which usually costs more to fix later than to prevent now."*
  - *Technical*: Approaching or exceeding silicon thermal thresholds, risking thermal throttling and permanent failure.

---

## 4. Architecture & Symbolic Caching

All partial derivatives ($T_x, T_y, T_{xx}, T_{yy}, T_{xy}$) are evaluated symbolically **once** at module load using SymPy and compiled into vectorized NumPy numerical functions via `sp.lambdify`. Interactive slider movements never trigger symbolic differentiation, achieving instantaneous responsiveness.

---

## 5. Quickstart & Testing

### Installation
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running Tests
```bash
pytest -v
```

### Running the Gradio App
```bash
python app.py
```
Open your browser at the displayed local URL (default: `http://127.0.0.1:7860`).

---

## 6. Project Files

- `app.py`: Gradio user interface with 10 analytical tabs.
- `models.py`: Analytical models with SymPy symbolic pre-compilation and caching.
- `calculus.py`: MAT 112 calculus functions (gradient, Hessian, discriminant test, Laplacian, divergence).
- `features.py`: Peak search, point lookup, cross-model comparison, thermal load, gradient descent, and Lagrange multipliers.
- `risk.py`: Stakeholder and technical risk assessment rules.
- `selftest.py`: Live verification of theoretical known values at factory default settings.
- `benchmark.py`: Pure SymPy substitution vs lambdified NumPy speedup timer.
- `report.py`: Plain-text and CSV report generator.
- `plots.py`: Matplotlib plotting routines (overview, streamlines, divergence, comparisons, trajectories).
- `notebooks/colab_backup.ipynb`: Backup runnable demo notebook.
