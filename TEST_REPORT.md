# CalSymPy (MAT 112) Test Report

This test report documents the test runs, real failure logs, fixes applied, design limitations, and human verification checks for the `calsympy_v2` project.

---

## 1. Summary

- **Test Environment**:
  - Operating System: Windows 11 (win32)
  - Python Version: Python 3.12.10
  - Dependencies: `numpy==2.5.3`, `matplotlib==3.11.2`, `pandas==3.1.0`, `scipy==1.18.1`, `sympy==1.14.0`
  - Clean virtual environment created and verified from `requirements.txt`.
- **Total Test Cases Executed**: 24 tests across console, GUI, numerical integration, boundary conditions, and notebook execution.
- **Initial Test Results**:
  - Passed: 22
  - Failed (Real Bugs): 2
- **Bugs Fixed**: 2 (both fixed in beginner style and verified with automated re-tests).
- **Post-Fix Test Results**: 24 Passed, 0 Failed.

---

## 2. Test Case Table

| Test ID | Area | Input / Condition | Expected Behavior | Actual Behavior | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Environment | Fresh venv from `requirements.txt` | Clean pip install of all 5 libraries | Installed numpy, matplotlib, pandas, scipy, sympy cleanly | **PASS** |
| **TC-02** | SymPy Checks | `python check_with_sympy.py` | Off-axis checks match SymPy exact partials | All 3 models printed `MATCH` | **PASS** |
| **TC-03** | Calculus Asserts | `python test_calculus.py` | All asserts pass (gradient, D-test, tangent plane, Taylor, descent) | `All calculus tests passed successfully!` | **PASS** |
| **TC-04** | `main.py` Option 1 | Model switching: A -> B -> C -> A | Active model and defaults reset properly | Parameters and defaults reset cleanly on switch | **PASS** |
| **TC-05** | `main.py` Option 1 | Empty Enter on parameter input | Keep current parameter value unchanged | Kept current value without modification | **PASS** |
| **TC-06** | `main.py` Option 1 | Non-numeric letters in parameter input | Catch `ValueError`, print warning, keep value | `Invalid number. Keeping <current_val>` | **PASS** |
| **TC-07** | `main.py` Option 1 | Input `s = 0` or `s < 0` for Model A | Validate positive dispersion; prevent division by zero | Initially crashed with `ZeroDivisionError` (see Bug 1); fixed to reject non-positive values | **PASS (Fixed)** |
| **TC-08** | `main.py` Option 1 | Input `L = 0` or `L < 0` for plate size | Validate positive plate size; prevent division by zero | Initially crashed with `ZeroDivisionError` in Model B and `nan` in Model A; fixed | **PASS (Fixed)** |
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
| **TC-19** | `main.py` & `gui.py` | Save report when destination is read-only | Catch permission error without crashing | Initially crashed with `PermissionError` (see Bug 2); fixed with `try...except (IOError, OSError)` | **PASS (Fixed)** |
| **TC-20** | `calculus.py` | Model B D-test where $D=0$ at $(1.0, 1.0)$ | Hessian determinant evaluates near 0 | $D = 0.00000000$, classified as `Inconclusive` | **PASS** |
| **TC-21** | `calculus.py` | `average_temperature` vs SymPy exact ($n=10$) | Monotonic convergence toward exact integral | Value: $40.431729^\circ\text{C}$, Error: $0.167492^\circ\text{C}$ ($0.42\%$) | **PASS** |
| **TC-22** | `calculus.py` | `average_temperature` vs SymPy exact ($n=80$) | Higher accuracy midpoint Riemann sum | Value: $40.266841^\circ\text{C}$, Error: $0.002604^\circ\text{C}$ ($0.0065\%$) | **PASS** |
| **TC-23** | `calculus.py` | `average_temperature` vs SymPy exact ($n=400$) | Asymptotic double integral precision | Value: $40.264341^\circ\text{C}$, Error: $0.000104^\circ\text{C}$ ($0.0003\%$) | **PASS** |
| **TC-24** | Notebook | `notebooks/colab_backup.ipynb` top to bottom | Runs all cells in clean kernel without error | All 9 code cells ran cleanly, plots rendered | **PASS** |

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
- **Cause**: `ask_param` parsed any valid floating-point number without checking that physical dimensions and dispersion parameters ($L, s, s_1, s_2$) must be strictly positive ($> 0$).
- **Fix**:
  - *Before (`main.py`)*:
    ```python
    def ask_param(name, current_val):
        val = input("Enter " + name + " (current " + str(current_val) + "): ").strip()
        if val == "":
            return current_val
        try:
            return float(val)
        except ValueError:
            print("Invalid number. Keeping " + str(current_val))
            return current_val
    ```
  - *After (`main.py`)*:
    ```python
    def ask_param(name, current_val):
        val = input("Enter " + name + " (current " + str(current_val) + "): ").strip()
        if val == "":
            return current_val
        try:
            num = float(val)
            if name in ["L", "s", "s1", "s2"] and num <= 0.0:
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
- **Location**: `main.py` line 158 (`option_save_report`), and `gui.py` line 250 (`save_report`)
- **Steps to Reproduce**:
  1. Set read-only file permissions on `report_A.csv` (`attrib +r report_A.csv`)
  2. Launch GUI (`python gui.py`) or console (`python main.py`)
  3. Attempt to save the report as CSV
- **Expected**: The program catches file system errors, informs the user with an error dialog / console message, and continues running without crashing.
- **Actual (Real Traceback)**:
  ```text
  Traceback (most recent call last):
    File "E:\Study\Projects\calsympy_v2\gui.py", line 261, in save_report
      df.to_csv(fname, index=False)
    File "E:\Study\Projects\calsympy_v2\.venv_test\Lib\site-packages\pandas\core\generic.py", line 4026, in to_csv
      return DataFrameRenderer(formatter).to_csv(
    File "E:\Study\Projects\calsympy_v2\.venv_test\Lib\site-packages\pandas\io\formats\format.py", line 1027, in to_csv
      csv_formatter.save()
    File "E:\Study\Projects\calsympy_v2\.venv_test\Lib\site-packages\pandas\io\formats\csvs.py", line 251, in save
      with get_handle(
    File "E:\Study\Projects\calsympy_v2\.venv_test\Lib\site-packages\pandas\io\common.py", line 939, in get_handle
      handle = open(
  PermissionError: [Errno 13] Permission denied: 'report_A.csv'
  ```
- **Cause**: Direct invocation of `df.to_csv()` and `open(..., "w")` without wrapping in a `try...except (IOError, OSError)` block.
- **Fix**:
  - *Before (`gui.py`)*:
    ```python
    if fmt == "CSV":
        fname = "report_" + plate.model + ".csv"
        df = pd.DataFrame({"Metric": metrics, "Value": values})
        df.to_csv(fname, index=False)
    else:
        fname = "report_" + plate.model + ".txt"
        f = open(fname, "w")
        for i in range(len(metrics)):
            f.write(str(metrics[i]) + ": " + str(values[i]) + "\n")
        f.close()
    lbl_save_status.config(text="Report saved to " + fname)
    messagebox.showinfo("Report Saved", "Successfully saved report to " + fname)
    ```
  - *After (`gui.py`)*:
    ```python
    fname = "report_" + plate.model + (".csv" if fmt == "CSV" else ".txt")
    try:
        if fmt == "CSV":
            df = pd.DataFrame({"Metric": metrics, "Value": values})
            df.to_csv(fname, index=False)
        else:
            f = open(fname, "w")
            for i in range(len(metrics)):
                f.write(str(metrics[i]) + ": " + str(values[i]) + "\n")
            f.close()
        lbl_save_status.config(text="Report saved to " + fname, fg="green")
        messagebox.showinfo("Report Saved", "Successfully saved report to " + fname)
    except (IOError, OSError):
        lbl_save_status.config(text="Error saving " + fname, fg="red")
        messagebox.showerror("Save Error", "Could not save report (file may be open or read-only).")
    ```
  - Equivalent `try...except (IOError, OSError)` added to `option_save_report` in `main.py`.
- **Re-test Result**: With `report_A.csv` marked read-only, `main.py` prints `Error: Could not save report to report_A.csv` and returns to menu; `gui.py` displays a non-fatal error dialog. Zero unhandled exceptions.
- **Status**: Fixed in local commit `d496c6f`.

---

## 4. Limitations Found But Not Fixed (Design Choices)

1. **Initial Point Clamping in Gradient Descent**:
   - *Behavior*: If the user enters a start position near the extreme boundary (e.g. $x = 0.05 < 0.2$), `path[0]` records the exact initial position $(0.05, 0.05)$, while subsequent steps `path[1:]` are clamped to $[0.2, L-0.2]$.
   - *Reason*: This preserves truthful recording of the chip's actual initial placement while preventing the physical chip from traveling outside safe margins during movement.
2. **Blocking Console Matplotlib Plots**:
   - *Behavior*: In `plots.py`, calling `plt.show()` pauses the console until the user closes the figure window.
   - *Reason*: Standard Matplotlib interactive behaviour for console programs without custom GUI event loop integration.
3. **Single-Threaded UI Operations**:
   - *Behavior*: While computing high-resolution double integrals ($n_{\text{steps}} = 400$) or heavy operations, the Tkinter window will briefly pause before updating.
   - *Reason*: Multi-threading is strictly forbidden by the first-year student course rules.

---

## 5. Items Requiring Human Verification

The following items cannot be fully automated via script and require a person to visually inspect and click:
1. **Window Close Event (`WM_DELETE_WINDOW`)**: Clicking the physical 'X' button in the title bar of the Tkinter window to ensure the desktop process closes cleanly.
2. **Visual Layout and Aesthetic Spacing**: Visually verifying that font sizes, label margins, and button alignments render comfortably across different desktop screen DPI scalings.
3. **Interactive Plot Toolbar / Zoom / Pan**: If a user interacts directly with the canvas or hovers over contour lines on Tab 1 and Tab 4.

---

## 6. Commands to Reproduce Every Test

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
   python -c "import main, io, sys; sys.stdin = io.StringIO('1\nB\nn\n1\nC\nn\n1\nA\nn\n3\n2.0\n2.0\n4\n5\n6\n1.5\n1.5\nn\n7\n1\n7\n2\n0\n'); main.main()"
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

5. **Test GUI Controls & Validation Programmatically**:
   ```powershell
   python -c "import gui, tkinter as tk; gui.root = tk.Tk(); gui.setup_left_panel(gui.root); tabs = tk.ttk.Notebook(gui.root); tabs.add(gui.setup_tab_heatmap(tabs), text='Map'); gui.build_param_fields(); gui.draw_heatmap(); gui.root.update(); print('GUI initialized cleanly'); gui.root.destroy()"
   ```

6. **Test Colab Backup Notebook Top-to-Bottom**:
   ```powershell
   python -c "import json, matplotlib; matplotlib.use('Agg'); nb = json.load(open('notebooks/colab_backup.ipynb', encoding='utf-8')); g = {}; [exec(''.join(c['source']), g) for c in nb['cells'] if c['cell_type'] == 'code']; print('Notebook executed top-to-bottom successfully!')"
   ```
