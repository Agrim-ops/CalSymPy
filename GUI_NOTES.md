# CalSymPy GUI Reference & Notes

This document describes the structure, widgets, and functions of `gui.py`, the Tkinter graphical interface for CalSymPy (MAT 112).

---

## 1. Core Tkinter Concepts Explained in Plain Words

1. **`root.mainloop()`**: This is Tkinter's continuous event-listening loop that keeps the application window open on your screen and constantly listens for user interactions such as mouse clicks, keyboard keystrokes, and window resizing.
2. **Callbacks**: A callback is a regular Python function that is assigned to a widget (for example, passing `command=apply_parameters` to a Button); whenever the user triggers that widget, Tkinter automatically calls that function to execute our code.
3. **`FigureCanvasTkAgg`**: This is a bridge between Matplotlib and Tkinter that wraps a Matplotlib `Figure` into a native Tkinter canvas widget (`canvas.get_tk_widget()`), allowing interactive scientific plots to be drawn and refreshed inside the GUI using `canvas.draw()`.

---

## 2. Function-by-Function Breakdown

### Parameter & Model Management

- **`read_param(key)`**
  - **What it does**: Fetches the text string from the specified Entry widget in `entry_dict`, strips whitespace, and converts it to a floating-point number.
  - **Invoked by**: Called internally by `apply_params_a`, `apply_params_b`, and `apply_params_c`.

- **`apply_params_a()`**
  - **What it does**: Reads user inputs from `entry_dict` and assigns them to the 6 parameters of Model A ($T_{\text{edge}}, T_0, s, c_x, c_y, L$).
  - **Invoked by**: Called by `apply_parameters()` when active model is `"A"`.

- **`apply_params_b()`**
  - **What it does**: Reads user inputs from `entry_dict` and assigns them to the 3 parameters of Model B ($T_{\text{edge}}, T_0, L$).
  - **Invoked by**: Called by `apply_parameters()` when active model is `"B"`.

- **`apply_params_c()`**
  - **What it does**: Reads user inputs from `entry_dict` and assigns them to the 10 parameters of Model C ($T_{\text{edge}}, t_1, s_1, c_{x1}, c_{y1}, t_2, s_2, c_{x2}, c_{y2}, L$).
  - **Invoked by**: Called by `apply_parameters()` when active model is `"C"`.

- **`validate_plate_params()`**
  - **What it does**: Verifies that plate dimensions and Gaussian dispersion values are strictly positive ($L > 0$, $s > 0$). Returns an error description or an empty string if valid.
  - **Invoked by**: Called by `apply_parameters()` before updating plots.

- **`apply_parameters()`**
  - **What it does**: Reads all current parameter Entry values with a `try/except ValueError` block, validates physical bounds, updates the plate attributes, redraws the heat map, resets the cooling plot, updates the plate summary, and updates `lbl_param_status`.
  - **Invoked by**: The **"Apply Parameters"** Button in the left panel.

- **`build_param_fields()`**
  - **What it does**: Clears the `param_frame` container and dynamically creates Labels and Entry boxes pre-filled with the active model's default values, storing widget references in `entry_dict`.
  - **Invoked by**: Called during initial setup in `main()` and by `on_model_select()` upon switching models.

- **`on_model_select(event)`**
  - **What it does**: Reads the newly chosen model from the Combobox, updates `plate.set_model(chosen)`, rebuilds the parameter inputs, and refreshes the heat map and summary calculations.
  - **Invoked by**: Bound to the `<<ComboboxSelected>>` event of the **Model Dropdown** (`model_combo`).

---

### Tab 1: Heat Map

- **`draw_heatmap()`**
  - **What it does**: Evaluates the plate's temperature and gradient on a $50 \times 50$ grid, clears `fig_map`, draws the `imshow` heat map, white contour lines, cyan gradient vector arrows (`quiver`), and colorbar, then calls `canvas_map.draw()`.
  - **Invoked by**: Called during startup, and after parameter updates or model changes.

---

### Tab 2: Point Lookup

- **`show_lookup()`**
  - **What it does**: Reads $x$ and $y$ from `entry_lookup_x` and `entry_lookup_y`. If input is non-numeric or outside $[0, L]$, displays a warning messagebox. Otherwise, calculates temperature $T$, gradient $(T_x, T_y)$, gradient magnitude $|\nabla T|$, second partial derivatives $(T_{xx}, T_{yy}, T_{xy})$, discriminant $D$, and classification, displaying them on `lbl_lookup_result`.
  - **Invoked by**: The **"Calculate"** Button on Tab 2.

---

### Tab 3: Plate Summary

- **`calculate_summary()`**
  - **What it does**: Searches a 2D grid to locate the hottest point and peak temperature, determines the silicon risk level (Low, Medium, or High), calculates the plate's average temperature via double integral Riemann sum, and formats `lbl_hottest`, `lbl_risk` (colored green, dark orange, or red), and `lbl_avg`.
  - **Invoked by**: The **"Refresh Summary"** Button on Tab 3, as well as upon model changes and parameter updates.

---

### Tab 4: Cooling Trajectory

- **`draw_blank_cooling()`**
  - **What it does**: Clears `fig_cool` and draws a clean temperature field heat map with colorbar ready for overlaying descent paths.
  - **Invoked by**: Called during startup, upon model selection, and after parameter updates.

- **`draw_cooling_path(path)`**
  - **What it does**: Redraws the cooling background and overlays the chip's descent trajectory with a dashed white line, a green circle at the start position, and a cyan circle at the cooler resting position.
  - **Invoked by**: Called by `run_descent()`.

- **`run_descent()`**
  - **What it does**: Reads initial chip coordinates $(x, y)$ from `entry_cool_x` and `entry_cool_y`, validates numeric bounds, runs gradient descent steps downhill away from heat sources via `calculus.gradient_descent()`, plots the trajectory, and displays the temperature drop and final coordinates on `lbl_cool_result`.
  - **Invoked by**: The **"Move Chip"** Button on Tab 4.

---

### Tab 5: Save Reports

- **`save_report()`**
  - **What it does**: Gathers plate summary metrics, checks the selected format in `combo_save` (CSV or TXT), exports the report to disk using a pandas DataFrame or text file, updates `lbl_save_status`, and shows a confirmation messagebox.
  - **Invoked by**: The **"Save Report"** Button on Tab 5.

---

### Layout & Window Assembly

- **`setup_left_panel(parent)`**
  - **What it does**: Constructs the left Frame containing the title, model selection dropdown, parameter container Frame, Apply button, and status label.
  - **Invoked by**: Called once by `main()`.

- **`setup_tab_heatmap(parent)`**
  - **What it does**: Constructs the Frame for Tab 1 and initializes the embedded `FigureCanvasTkAgg` widget for the heat map.
  - **Invoked by**: Called once by `main()`.

- **`setup_tab_lookup(parent)`**
  - **What it does**: Constructs the Frame for Tab 2 containing coordinate input fields, the Calculate button, and the results label.
  - **Invoked by**: Called once by `main()`.

- **`setup_tab_summary(parent)`**
  - **What it does**: Constructs the Frame for Tab 3 containing the refresh button, hottest point label, colored risk label, and average temperature label.
  - **Invoked by**: Called once by `main()`.

- **`setup_tab_cooling(parent)`**
  - **What it does**: Constructs the Frame for Tab 4 containing start coordinate entries, the Move Chip button, results label, and embedded cooling plot canvas.
  - **Invoked by**: Called once by `main()`.

- **`setup_tab_save(parent)`**
  - **What it does**: Constructs the Frame for Tab 5 containing the format selection dropdown, Save Report button, and confirmation label.
  - **Invoked by**: Called once by `main()`.

- **`main()`**
  - **What it does**: Initializes the root `Tk` window, configures title and size ($1100 \times 700$), builds the left panel and notebook tabs, runs initial calculations and plots, and starts `root.mainloop()`.
  - **Invoked by**: Executed when running `python gui.py`.
