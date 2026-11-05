# CalSymPy — Baseline Verification & Bug Audit (BUGS.md)
**Project**: CalSymPy (Team 4, Delta-T) — MAT 112 Engineering Mathematics & Python  
**Environment**: Python 3.12.10 (`.venv312`), Windows 10/11  
**Audit Date**: 05 November 2026  

---

## 1. Audit Summary

All 11 unit test files and `notebooks/colab_backup.ipynb` are present. Baseline `pytest -q` runs cleanly (39 passed).
A complete audit of the codebase against the known issue suspects confirms 8 issues and refutes 1 (as `.gitignore` is already correctly named and functioning).

---

## 2. Suspect Verification & Bug Registry

### Issue 1: Outdated Python Version Header in requirements.txt
- **File**: `requirements.txt`
- **Line**: 2
- **Symptom**: Header states `# Python version: 3.14.4` while the project runtime, virtual environment, and Hugging Face Spaces configuration standardize on Python 3.12.10.
- **Proposed Fix**: Update line 2 header comment to `# Python version: 3.12.10`.
- **Severity**: Low (Documentation/Consistency)
- **Status**: **CONFIRMED**

### Issue 2: Missing `pandas` in requirements.txt
- **File**: `requirements.txt`
- **Line**: N/A (Missing)
- **Symptom**: `pandas` is imported by `app.py` and `plots.py` (and required for structured tabular data across Compare, Self-Test, and CSV exports), but is not explicitly declared in `requirements.txt`.
- **Proposed Fix**: Add `pandas==3.1.0` (matching the verified pip freeze version) to `requirements.txt`.
- **Severity**: Medium (Deployment Dependency)
- **Status**: **CONFIRMED**

### Issue 3: Hardcoded Model Parameters & Text Transform in report.py
- **File**: `report.py`
- **Lines**:
  - Line 100: `f" - Explanation of Gap: {load['gap_explanation'].capitalize()}"`
  - Lines 158–160: Hardcodes `["Parameters", "T_edge", ...]` and `["Parameters", "T0", ...]`.
- **Symptom**:
  1. For Model D, parameters are `T1, s1, cx1, cy1, T2, s2, cx2, cy2`, so hardcoding `T0` outputs irrelevant/fallback entries.
  2. Calling `.capitalize()` on `gap_explanation` lowercases all subsequent words in the explanation sentence.
  3. CSV is generated via basic `csv.writer` instead of an idiomatic pandas DataFrame (`df.to_csv`), and no dense coordinate grid export is provided.
- **Proposed Fix**:
  1. Dynamically iterate over `model.param_keys` to output active parameter names and values.
  2. Replace `.capitalize()` with first-letter uppercase: `load['gap_explanation'][0].upper() + load['gap_explanation'][1:]`.
  3. Rebuild `generate_csv_report` using a pandas DataFrame with columns `['Section', 'Metric', 'Value', 'Units']`.
  4. Add `generate_grid_csv(model, params=None, grid_res=41, output_path=None)` exporting a DataFrame with columns `['x', 'y', 'T', 'Tx', 'Ty']`.
- **Severity**: High (Data Integrity & Course Requirement)
- **Status**: **CONFIRMED**

### Issue 4: Missing User Parameters & Missing Vertical Line in plots.py
- **File**: `plots.py`
- **Lines**:
  - Line 275 (`plot_optimization_trajectory`): `params = model.default_params`
  - Line 315 (`plot_lagrange_rail`): `params = model.default_params`
  - Lines 331–337 (`plot_lagrange_rail`): Only loops over $x$ when $b \ne 0$.
- **Symptom**:
  1. Both optimization plots ignore the user's active UI slider parameters, reverting to factory defaults.
  2. For a vertical mounting rail ($b = 0$, $ax = c \implies x = c/a$), no line is drawn because the loop only evaluates $y = (c - ax)/b$.
- **Proposed Fix**:
  1. Add an optional `params=None` argument to `plot_optimization_trajectory` and `plot_lagrange_rail`, merged with `model.default_params`. Update `app.py` callers to pass current slider values.
  2. In `plot_lagrange_rail`, check if `abs(b) < 1e-6`: if $0 \le c/a \le L$, draw a vertical line from $(c/a, 0)$ to $(c/a, L)$.
- **Severity**: High (Interactive Functional Bug)
- **Status**: **CONFIRMED**

### Issue 5: Unit Inconsistency between Spatial Gradient and Thermal Conductivity
- **File**: `features.py`, `plots.py`, `calculus.py`
- **Lines**:
  - `features.py` (lines 208–215): Computes `flux_mag = k * grad_mag` with $T_x$ in $^\circ\text{C/cm}$ and $k$ in $\text{W/(m}\cdot\text{K)}$, yet labels units as $\text{W/m}^2$.
  - `plots.py` (line 226): Divergence colorbar labels units as `"div F (W/(m²·cm))"`.
- **Symptom**: Units are inconsistent between SI meters and plate centimeters.
- **Proposed Fix**:
  - Standardize on SI: Convert spatial derivatives to meters by scaling gradient by $100$ ($1\text{ cm} = 0.01\text{ m} \implies \nabla T_{\text{m}} = 100 \nabla T_{\text{cm}}$), yielding heat flux $\mathbf{F} = -k \nabla T_{\text{m}}$ in $\text{W/m}^2$.
  - Scale Laplacian by $10000$ ($1\text{ cm}^2 = 10^{-4}\text{ m}^2$) for divergence $\operatorname{div} \mathbf{F} = -k \nabla^2 T_{\text{m}}$ in $\text{W/m}^3$.
  - Update docstrings, printouts, colorbar labels, and unit test assertions accordingly. Verify that the 34 (now 37) theoretical known values (which test $T, T_x, T_{xx}, \nabla^2 T$ in pure $^\circ\text{C}$ and cm) remain unaffected.
- **Severity**: Medium (Physical & Dimensional Consistency)
- **Status**: **CONFIRMED**

### Issue 6: Colab Display Incompatibility due to `Agg` Backend
- **File**: `plots.py` (line 36) & `notebooks/colab_backup.ipynb`
- **Lines**: `plots.py` line 36 (`matplotlib.use('Agg')`), notebook plotting cells
- **Symptom**: Unconditional setting of the non-interactive `Agg` backend suppresses inline figure rendering in interactive Jupyter/Google Colab environments when calling `plt.show()`.
- **Proposed Fix**: In `notebooks/colab_backup.ipynb`, explicitly display returned figure objects using IPython's `IPython.display.display(fig)`. In `plots.py`, guard `matplotlib.use('Agg')` so it does not override an already active interactive notebook backend (`module://ipykernel.pylab.backend_inline`).
- **Severity**: Medium (Jupyter/Colab Presentation)
- **Status**: **CONFIRMED**

### Issue 7: Unused Imports, Non-Neutral Header, & Incomplete Model D Coverage in selftest.py
- **File**: `selftest.py`
- **Lines**:
  - Lines 31–35: Unused imports `math`, `compute_gradient_magnitude`, `compute_laplacian`, `compute_discriminant`, `find_hottest_points`.
  - Line 9: `# As instructed by the user...`
  - Lines 184–187: Model D only has 1 test check (`T(1.3, 1.3)`), missing theoretical checks for the saddle at $(2, 2)$ ($T=63.34, D=-1846.6$) and the peak at $(1.267, 1.267)$ ($T=71.69$).
- **Symptom**: Dead code, non-neutral phrasing in comments, and mismatch between self-test count (34) and claimed verified properties in README/dossier.
- **Proposed Fix**:
  1. Remove dead imports.
  2. Reword line 9 to neutral: `Important Design Rule: The self-test suite ALWAYS evaluates models strictly at their DEFAULT parameters...`.
  3. Add the 3 missing Model D verification checks (Saddle $T=63.34^\circ\text{C}$, Saddle $D=-1846.6$, Peak $T=71.69^\circ\text{C}$), raising total checks from 34 to 37.
  4. Update expected test count in `test_feature4_selftest.py`, `app.py`, `README.md`, and `PROJECT_DOSSIER.md`.
- **Severity**: Medium (Code Hygiene & Verification Alignment)
- **Status**: **CONFIRMED**

### Issue 8: Unused Import in benchmark.py
- **File**: `benchmark.py`
- **Line**: 24
- **Symptom**: `import sympy as sp` is imported but `sp` is never used (`sympy` expressions are accessed via `model.expr_sym`).
- **Proposed Fix**: Remove line 24 (`import sympy as sp`).
- **Severity**: Low (Dead Code Cleanup)
- **Status**: **CONFIRMED**

### Issue 9: .gitignore Naming and Rules
- **File**: `.gitignore`
- **Status**: **REFUTED** (Already Correct)
- **Finding**: The file is correctly named `.gitignore` (not `_gitignore`), and `git check-ignore` confirms that `.venv312`, `__pycache__`, and `.pytest_cache` are properly ignored by Git. No action needed for ignore rules.
