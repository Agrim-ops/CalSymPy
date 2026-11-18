# CalSymPy (MAT 112) Test Report
**Branch**: `main`  
**Project**: CalSymPy v2 (Team 4, Delta-T)

This test report documents the test runs, real failure logs, fixes applied, design limitations, and human verification checks for the `calsympy_v2` project.

---

## 1. Summary

- **Test Environment**:
  - Operating System: Windows 11 (win32)
  - Python Version: Python 3.12.10
  - Dependencies: `numpy==2.5.3`, `matplotlib==3.11.2`, `pandas==3.1.0`, `sympy==1.14.0`, `streamlit==1.67.0`
  - Clean virtual environment verified from `requirements.txt`.
- **Thermal Limits**:
  - Intel says the maximum junction temperature usually lies between about 100 and 110 degrees C, depending on the product. Our 70 and 90 degree limits are our own rule of thumb with a safety margin.
- **Total Test Cases Executed**: 30 tests across console, numerical integration, boundary conditions, notebook execution, and Streamlit web application.
- **Initial Test Results**:
  - Passed: 28
  - Failed (Real Bugs): 2
- **Bugs & Weaknesses Fixed**: 2 bugs + 1 gradient descent design weakness (all verified with automated re-tests).
- **Post-Fix Test Results**: 30 Passed, 0 Failed.
- **Scope**: Covers the two analytical temperature models (Model A: Gaussian hotspot, Model B: Sine plate), the 8 core multivariable calculus tools, the interactive console interface, and the Streamlit web application.

---

## 2. Test Case Table

| Test ID | Area | Input / Condition | Expected Behavior | Actual Behavior | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Environment | Fresh venv from `requirements.txt` | Clean pip install of all 5 libraries | Installed numpy, matplotlib, pandas, sympy, streamlit cleanly | **PASS** |
| **TC-02** | SymPy Checks | `python check_with_sympy.py` | Off-axis checks match SymPy exact partials | Model A and Model B printed `MATCH` | **PASS** |
| **TC-03** | Calculus Asserts | `python test_calculus.py` | All asserts pass (gradient, D-test, tangent plane, Taylor, descent) | `All calculus tests passed successfully!` | **PASS** |
| **TC-04** | `main.py` Option 1 | Model switching: A -> B -> A | Active model and defaults reset properly | Parameters and defaults reset cleanly on switch | **PASS** |
| **TC-05** | `main.py` Option 1 | Empty Enter on parameter input | Keep current parameter value unchanged | Kept current value without modification | **PASS** |
| **TC-06** | `main.py` Option 1 | Non-numeric letters in parameter input | Catch `ValueError`, print warning, keep value | `Invalid number. Keeping <current_val>` | **PASS** |
| **TC-07** | `main.py` Option 1 | Input `s = 0` or `s < 0` for Model A | Validate positive dispersion; prevent division by zero | Initially crashed with `ZeroDivisionError` (see Bug 1); fixed to reject non-positive values | **PASS (Fixed)** |
| **TC-08** | `main.py` Option 1 | Input `L = 0` or `L < 0` for plate size | Validate positive plate size; prevent division by zero | Initially crashed with `ZeroDivisionError` in Model B; fixed to reject non-positive values | **PASS (Fixed)** |
| **TC-09** | `main.py` Option 1 | Huge $T_0$ value ($10^9$) | Handled safely using standard float | $T(2, 2) = 1000000025.0^\circ\text{C}$ computed without overflow | **PASS** |
| **TC-10** | `main.py` Option 3 | Letters input for coordinates | Print `Invalid input coordinates.` and return | Printed message, returned cleanly to menu | **PASS** |
| **TC-11** | `main.py` Option 3 | Out-of-bounds coordinates ($x=5.0, y=2.0$) | Print error message and return to menu | `Coordinates must be between 0 and 4.0` | **PASS** |
| **TC-12** | `main.py` Option 3 | Boundary corners $(0, 0)$ and $(L, L)$ | Compute temperature and gradient properly | Evaluated $T(0,0)=26.10^\circ\text{C}$ and $T(4,4)=26.10^\circ\text{C}$ cleanly | **PASS** |
| **TC-13** | `main.py` Option 4 | Hottest point grid search | Find peak location $(2.0, 2.0)$ and Medium risk | Peak at $(2.0, 2.0)$, $85.0^\circ\text{C}$, Medium risk | **PASS** |
| **TC-14** | `main.py` Option 5 | Average temperature double integral | Midpoint Riemann sum calculation | Computed $46.47^\circ\text{C}$ | **PASS** |
| **TC-15** | `main.py` Option 6 | Descent starting at hotspot peak $(2, 2)$ | $\nabla T = [0, 0]$, chip stays at peak | Chip remained at $(2.00, 2.00)$, cooling $0.00^\circ\text{C}$ | **PASS** |
| **TC-16** | `main.py` Option 6 | Descent starting at corner $(0, 0)$ | Clamped to plate margins $[0.2, L-0.2]$ | Subsequent steps clamped to $x \ge 0.2, y \ge 0.2$ | **PASS** |
| **TC-17** | `main.py` Option 6 | Descent with huge step size ($1000.0$) | No step escapes the plate boundary | All steps clamped strictly within $[0.2, 3.8]$ | **PASS** |
| **TC-18** | `main.py` Option 7 | Save report twice (CSV then TXT) | Overwrites / creates files cleanly | Created `report_A.csv` and `report_A.txt` | **PASS** |
| **TC-19** | `main.py` | Save report when destination is read-only | Catch permission error without crashing | Initially crashed with `PermissionError` (see Bug 2); fixed with `try...except (IOError, OSError)` | **PASS (Fixed)** |
| **TC-20** | `calculus.py` | Model B D-test where $D=0$ at $(1.0, 1.0)$ | Hessian determinant evaluates near 0 | $D = 0.00000000$, classified as `Inconclusive` | **PASS** |
| **TC-21** | `calculus.py` | `average_temperature` vs SymPy exact ($n=10$) | Monotonic convergence toward exact integral | Value: $40.431729^\circ\text{C}$, Error: $0.167492^\circ\text{C}$ ($0.42\%$) | **PASS** |
| **TC-22** | `calculus.py` | `average_temperature` vs SymPy exact ($n=80$) | Higher accuracy midpoint Riemann sum | Value: $40.266841^\circ\text{C}$, Error: $0.002604^\circ\text{C}$ ($0.0065\%$) | **PASS** |
| **TC-23** | `calculus.py` | `average_temperature` vs SymPy exact ($n=400$) | Asymptotic double integral precision | Value: $40.264341^\circ\text{C}$, Error: $0.000104^\circ\text{C}$ ($0.0003\%$) | **PASS** |
| **TC-24** | Notebook | `notebooks/colab_backup.ipynb` top to bottom | Runs all cells in clean kernel without error | All 9 code cells ran cleanly, plots rendered | **PASS** |
| **TC-25** | `app.py` | Model switching & parameter customization (A <-> B, negative temperatures) | Reruns top-to-bottom with updated parameters | Models switched and updated without error | **PASS** |
| **TC-26** | `app.py` | Bad lookup coordinates ($x < 0, x > L, y < 0, y > L$) | Display warning banner, suppress calculus evaluation | Amber warning displayed, zero crash | **PASS** |
| **TC-27** | `app.py` | Chip relocation from hotspot peak $(2.0, 2.0)$ | Stays at peak ($\nabla T \approx 0$), cooling $0.00^\circ\text{C}$ | Chip stayed at peak, trajectory plotted cleanly | **PASS** |
| **TC-28** | `app.py` | Chip relocation from plate corner $(0.0, 0.0)$ | Clamps inside safe plate margins $[0.2, L-0.2]$ | Clamped to safe margins, cooling achieved | **PASS** |
| **TC-29** | `app.py` | Chip start position outside plate ($x > L, y > L$) | Display warning banner, avoid invalid steps | Warning displayed, zero crash | **PASS** |
| **TC-30** | `app.py` | CSV Report Download button | Generates in-memory CSV via pandas | Download button rendered with valid CSV payload | **PASS** |

---

## 3. Bug Log

### Bug 1: Missing Positive Validation for Dimensions and Dispersions in Console Menu
- **Bug ID**: BUG-01
- **Location**: `main.py`, `ask_param()`, line 18
- **Steps to Reproduce**:
  1. Run `python main.py`
  2. Choose Option `1` (Model A)
  3. Answer `y` to change parameters
  4. Press Enter to keep $T_{\text{edge}}$ and $T_0$, then enter `0` for $s$ (or `0` for $L$)
  5. Choose Option `3` (Point lookup) and enter coordinates `2.0` and `2.0`
- **Expected**: The program should reject $s \le 0$ or $L \le 0$ with an informative message and retain the safe previous parameter value.
- **Actual (Real Traceback)**:
  ```text
  Traceback (most recent call last):
    File "E:\Study\Projects\calsympy_v2\main.py", line 191, in main
      handle_choice(choice, plate)
    File "E:\Study\Projects\calsympy_v2\main.py", line 172, in handle_choice
      option_lookup(plate)
    File "E:\Study\Projects\calsympy_v2\main.py", line 81, in option_lookup
      t = plate.get_temp(x_in, y_in)
    File "E:\Study\Projects\calsympy_v2\models.py", line 120, in get_temp
      return temp_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
    File "E:\Study\Projects\calsympy_v2\models.py", line 9, in temp_a
      return t_edge + t0 * np.exp(-r2 / s)
  ZeroDivisionError: float division by zero
  ```
- **Cause**: `ask_param` parsed any valid floating-point number without checking that physical dimensions and dispersion parameters ($L, s$) must be strictly positive ($> 0$).
- **Fix**: In `main.py`, added positive check:
  ```python
  def ask_param(name, current_val):
      val = input("Enter " + name + " (current " + str(current_val) + "): ").strip()
      if val == "":
          return current_val
      try:
          num = float(val)
          if name in ["L", "s"] and num <= 0.0:
              print(name + " must be positive. Keeping " + str(current_val))
              return current_val
          return num
      except ValueError:
          print("Invalid number. Keeping " + str(current_val))
          return current_val
  ```
- **Re-test Result**: Running `main.py` with `s=0` prints `s must be positive. Keeping 2.0`. Subsequent point lookup runs normally with zero errors.
- **Status**: Fixed in local commit `e585923`.

---

### Bug 2: Unhandled PermissionError on Save Report when Target File is Read-Only
- **Bug ID**: BUG-02
- **Location**: `main.py`, `option_save_report()`
- **Steps to Reproduce**:
  1. Set read-only file permissions on `report_A.csv` (`attrib +r report_A.csv`)
  2. Launch console (`python main.py`)
  3. Attempt to save the report as CSV (Option 7)
- **Expected**: The program catches file system errors, informs the user with an error message, and continues running without crashing.
- **Actual (Real Traceback)**:
  ```text
  Traceback (most recent call last):
    File "E:\Study\Projects\calsympy_v2\main.py", line 158, in option_save_report
      df.to_csv(fname, index=False)
    File "E:\Study\Projects\calsympy_v2\.venv_test\Lib\site-packages\pandas\core\generic.py", line 4026, in to_csv
      return DataFrameRenderer(formatter).to_csv(
  PermissionError: [Errno 13] Permission denied: 'report_A.csv'
  ```
- **Cause**: Direct invocation of `df.to_csv()` and `open(..., "w")` without wrapping in a `try...except (IOError, OSError)` block.
- **Fix**: Wrapped file operations in `try...except (IOError, OSError)` in `option_save_report`:
  ```python
  try:
      if choice == "1":
          pd.DataFrame({"Metric": metrics, "Value": values}).to_csv(fname, index=False)
      else:
          with open(fname, "w") as f:
              for i in range(len(metrics)):
                  f.write(str(metrics[i]) + ": " + str(values[i]) + "\n")
      print("Report saved successfully to " + fname)
  except (IOError, OSError):
      print("Error: Could not save report to " + fname)
  ```
- **Re-test Result**: With `report_A.csv` marked read-only, `main.py` prints `Error: Could not save report to report_A.csv` and returns to menu. Zero unhandled exceptions.
- **Status**: Fixed in local commit `d496c6f`.

---

### Design Weakness: Raw Gradient Step Jumping Directly to Boundary Margins
- **Weakness ID**: DES-01 (Found by Hand Calculation & Fixed)
- **Location**: `calculus.py`, `gradient_descent()`
- **Issue Description**: The original implementation stepped proportionally to the raw gradient: `x = x - step_size * Tx`. At the default start $(1.5, 1.5)$ on Model A, the gradient was large ($\nabla T = \langle 22.99, 22.99 \rangle$), causing the first step ($0.08 \times 22.99 \approx 1.84$) to jump past the safe margin directly to $(0.2, 0.2)$ in one single step ($44.38^\circ\text{C}$ drop). Subsequent steps remained pinned to $(0.2, 0.2)$.
- **Real Trace (Before Fix)**:
  - Step 0: $(1.5000, 1.5000) \to 71.7280^\circ\text{C}$
  - Step 1: $(0.2000, 0.2000) \to 27.3498^\circ\text{C}$
  - Step 2: $(0.2000, 0.2000) \to 27.3498^\circ\text{C}$
  - Step 3: $(0.2000, 0.2000) \to 27.3498^\circ\text{C}$
  - Step 4: $(0.2000, 0.2000) \to 27.3498^\circ\text{C}$
- **Fix**: Changed `gradient_descent()` so each step moves a fixed distance along the unit downhill direction by dividing $T_x$ and $T_y$ by the gradient magnitude $\sqrt{T_x^2 + T_y^2}$. Defaults updated to `step_size=0.1, steps=40`. If magnitude is 0 (at the peak), the chip does not move. Clamping to $[0.2, L - 0.2]$ is maintained.
- **Real Trace (After Fix)**:
  - Step 0: $(1.5000, 1.5000) \to 71.7280^\circ\text{C}$
  - Step 1: $(1.4293, 1.4293) \to 68.3208^\circ\text{C}$
  - Step 2: $(1.3586, 1.3586) \to 64.7625^\circ\text{C}$
  - Step 3: $(1.2879, 1.2879) \to 61.1332^\circ\text{C}$
  - Step 4: $(1.2172, 1.2172) \to 57.5085^\circ\text{C}$
  ...
  - Step 38: $(0.2000, 0.2000) \to 27.3498^\circ\text{C}$
  - Step 39: $(0.2000, 0.2000) \to 27.3498^\circ\text{C}$
  - Step 40: $(0.2000, 0.2000) \to 27.3498^\circ\text{C}$
  The first step distance is now $0.1000\text{ cm} < 0.15\text{ cm}$, producing a gradual, physical downhill path.
- **Status**: Fixed in local commit.

---

## 4. Limitations Found But Not Fixed (Design Choices)

1. **Initial Point Clamping in Gradient Descent**:
   - *Behavior*: If the user enters a start position near the extreme boundary (e.g. $x = 0.05 < 0.2$), `path[0]` records the exact initial position $(0.05, 0.05)$, while subsequent steps `path[1:]` are clamped to $[0.2, L-0.2]$.
   - *Reason*: This preserves truthful recording of the chip's actual initial placement while preventing the physical chip from traveling outside safe margins during movement.
2. **Blocking Console Matplotlib Plots**:
   - *Behavior*: In `plots.py`, calling `plt.show()` pauses the console until the user closes the figure window.
   - *Reason*: Standard Matplotlib interactive behaviour for console programs. In the Streamlit web app, show=False returns the figure directly.

---

## 5. Commands to Reproduce Every Test

Execute the following commands from PowerShell inside `E:\Study\Projects\calsympy_v2`:

1. **Test Fresh Environment & Symbolic Checks**:
   ```powershell
   .\.venv\Scripts\activate
   python check_with_sympy.py
   python test_calculus.py
   ```

2. **Test Boundary & Invalid Parameters in Console (`main.py`)**:
   ```powershell
   # Test invalid s=0 (rejected, keeping 2.0)
   python -c "import main, io, sys; sys.stdin = io.StringIO('1\nA\ny\n\n\n0\n\n\n\n3\n2.0\n2.0\n0\n'); main.main()"

   # Test invalid L=0 (rejected, keeping 4.0)
   python -c "import main, io, sys; sys.stdin = io.StringIO('1\nB\ny\n\n\n0\n3\n0.0\n0.0\n0\n'); main.main()"
   ```

3. **Test Full Console Menu Cycling**:
   ```powershell
   python -c "import main, io, sys; sys.stdin = io.StringIO('1\nB\nn\n1\nA\nn\n3\n2.0\n2.0\n4\n5\n6\n1.5\n1.5\nn\n7\n1\n7\n2\n0\n'); main.main()"
   ```

4. **Test Read-Only File Error Handling**:
   ```powershell
   # Create read-only file and test save
   Set-Content -Path report_A.csv -Value 'locked'
   Set-ItemProperty -Path report_A.csv -Name IsReadOnly -Value $true
   python -c "import main, io, sys; sys.stdin = io.StringIO('7\n1\n0\n'); main.main()"
   Set-ItemProperty -Path report_A.csv -Name IsReadOnly -Value $false
   Remove-Item report_A.csv
   ```

5. **Test Colab Backup Notebook Top-to-Bottom**:
   ```powershell
   python -c "import json, matplotlib; matplotlib.use('Agg'); nb = json.load(open('notebooks/colab_backup.ipynb', encoding='utf-8')); g = {}; [exec(''.join(c['source']), g) for c in nb['cells'] if c['cell_type'] == 'code']; print('Notebook executed top-to-bottom successfully!')"
   ```
