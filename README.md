# CalSymPy

**Course**: MAT 112 Engineering Mathematics & Python  
**Team**: Team 4 (Delta-T)  
- Agrim Goel - Mathematics & Model Derivation  
- Team 4 Members - Numerical Algorithms, Interfaces, Testing & Documentation  

## Description
CalSymPy calculates and visualises steady-state 2D temperature distributions on a flat square plate. It evaluates partial derivatives to compute temperature gradients, slopes, and surface curvature classifications. The program also estimates average plate temperature using double integration and simulates moving a heat-sensitive chip downhill along the negative gradient to cool it down. Both a terminal console interface and a browser-based web application are provided.

## Thermal Models
All formulas are evaluated in plain algebraic form:

1. **Model A (Gaussian Hotspot)**:
   `T(x, y) = T_edge + T0 * exp(-((x - cx)^2 + (y - cy)^2) / s)`  
   Represents a localised hotspot centered at `(cx, cy)` with peak temperature rise `T0`, dispersion width `s`, and base edge temperature `T_edge`.

2. **Model B (Sine Plate)**:
   `T(x, y) = T_edge + T0 * sin(pi * x / L) * sin(pi * y / L)`  
   Represents a sinusoidal standing thermal distribution on a plate of side length `L`, where temperature is `T_edge` along all boundaries and peaks at the center `(L/2, L/2)`.

## Calculus Used
- **Partial Derivatives and Gradient**: First-order partial derivatives `Tx = dT/dx` and `Ty = dT/dy` form the gradient vector `<Tx, Ty>`, pointing in the direction of steepest temperature increase. The gradient magnitude `sqrt(Tx^2 + Ty^2)` gives the maximum slope in deg C/cm.
- **Second Derivative Test**: Second-order partial derivatives `Txx`, `Tyy`, and mixed partial `Txy` form the Hessian discriminant `D = Txx * Tyy - Txy^2`. Points with `D > 0` and `Txx < 0` are local maxima (hotspots), `D > 0` and `Txx > 0` are local minima, and `D < 0` are saddle points.
- **Double Integral**: The average temperature is computed via `(1 / Area) * iint T(x, y) dA` over the region `[0, L] x [0, L]`, evaluated using a 2D midpoint Riemann sum.
- **Tangent Plane and Taylor Polynomial**: The tangent plane gives the linear approximation `L(x, y) = T(a, b) + Tx*(x - a) + Ty*(y - b)` near `(a, b)`. The degree-2 Taylor polynomial adds the quadratic curvature terms `0.5*Txx*(dx^2) + Txy*dx*dy + 0.5*Tyy*(dy^2)`.
- **Gradient Descent**: Moves a chip downhill away from heat along the negative gradient direction `(-Tx, -Ty)` in discrete steps, keeping coordinates within plate boundaries.

## How to Run

Activate the virtual environment first (or use the `.venv` path directly):
```powershell
.\.venv\Scripts\Activate.ps1
```

### 1. Run Tests
```bash
python check_with_sympy.py
python test_calculus.py
```

### 2. Run the Web Application
```bash
streamlit run app.py
```
*(Or without activating: `.\.venv\Scripts\python.exe -m streamlit run app.py`)*

### 3. Run the Console Interface
```bash
python main.py
```

## Project Files
- `models.py`: Temperature formulas, analytical partial derivatives, and `Plate` class.
- `calculus.py`: Multivariable calculus algorithms (gradient, second derivative test, Riemann sum, tangent plane, Taylor polynomial, gradient descent).
- `plots.py`: Matplotlib plotting routines for temperature heatmap and gradient descent path.
- `main.py`: Console menu interface for terminal use.
- `app.py`: Streamlit web interface with interactive sliders, point lookup, cooling simulation, and CSV export.
- `check_with_sympy.py`: Verification script comparing analytical derivatives against SymPy symbolic derivatives.
- `test_calculus.py`: Unit test script checking calculus functions against expected values.
- `requirements.txt`: Pinned Python dependencies.
- `runtime.txt`: Python version specification for Render deployment (`python-3.12.10`).
- `DEPLOY.md`: Deployment instructions for hosting the web app on Render.
- `PSEUDOCODE.md`: Algorithmic pseudocode for all calculus routines.
- `TEST_REPORT.md`: Test execution results, recorded bugs, and verification logs.
- `notebooks/colab_backup.ipynb`: Backup notebook runnable on Google Colab.
- `.gitignore`: Untracked file rules for local environments.

## Limitations
- The plate is assumed to be an idealised flat 2D square with uniform physical properties.
- The equations model steady-state temperature only; transient time-dependent heat transfer is not modeled.
- Silicon risk levels (Low < 70 C, Medium 70-90 C, High > 90 C) are empirical thresholds chosen for project demonstration rather than manufacturer specifications.

## Live Link
- **Render Web App**: https://calsympy-heat-map.onrender.com
