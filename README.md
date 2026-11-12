# CalSymPy (MAT 112 Engineering Mathematics & Python)

CalSymPy is a clean, explainable first-year engineering mathematics project modeling steady-state 2D heat distribution $T(x, y)$ on a square plate.

## Features
- **Models**:
  - Model A: Single Gaussian hotspot $T(x, y) = T_{\text{edge}} + T_0 \exp(-((x-c_x)^2 + (y-c_y)^2)/s)$
  - Model B: Sine plate $T(x, y) = T_{\text{edge}} + T_0 \sin(\pi x/L) \sin(\pi y/L)$
- **Hand-Derived Derivatives**: First partials ($T_x, T_y$), gradient magnitude, second partials ($T_{xx}, T_{yy}, T_{xy}$), and Hessian discriminant $D = T_{xx} T_{yy} - T_{xy}^2$ for critical point classification.
- **Calculus Tools**:
  - Midpoint Riemann sum double integral for average plate temperature
  - Linearisation (tangent plane) and quadratic Taylor approximation
  - Downhill gradient descent to relocate heat-sensitive components
  - Grid search for hottest point and silicon thermal risk level
- **Console Interface**: Interactive console menu in `main.py`.

> **Note on Graphical User Interface (GUI)**:
> A desktop Tkinter GUI was prototyped in previous explorations; graphical interface integration is planned as future scope. The current core project focuses strictly on lightweight, fully explainable console and notebook workflows.

## Running Tests
```bash
python check_with_sympy.py
python test_calculus.py
python main.py
```
