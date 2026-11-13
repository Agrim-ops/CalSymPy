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
- **Interfaces**:
  - **Web Application**: Lightweight Streamlit UI in `app.py` (`streamlit run app.py`). See `APP_NOTES.md` and `DEPLOY.md`.
  - **Console Interface**: Interactive console menu in `main.py` (`python main.py`).

## Running the Application & Tests
```bash
# Run unit tests and symbolic checks
python check_with_sympy.py
python test_calculus.py

# Launch web UI
streamlit run app.py

# Launch console interface
python main.py
```
