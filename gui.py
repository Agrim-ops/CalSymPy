# gui.py - Tkinter graphical interface for CalSymPy
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import models
import calculus

# Global plate model and widget references
plate = models.Plate("A")
entry_dict = {}

# Tkinter and Matplotlib global handles
root = None
model_combo = None
param_frame = None
lbl_param_status = None
fig_map = None
canvas_map = None
fig_cool = None
canvas_cool = None

entry_lookup_x = None
entry_lookup_y = None
lbl_lookup_result = None

lbl_hottest = None
lbl_risk = None
lbl_avg = None

entry_cool_x = None
entry_cool_y = None
lbl_cool_result = None

combo_save = None
lbl_save_status = None

def read_param(key):
    # Read a floating point number from an entry box
    text = entry_dict[key].get().strip()
    return float(text)

def apply_params_a():
    # Update Model A parameters from entries
    plate.t_edge = read_param("t_edge")
    plate.t0 = read_param("t0")
    plate.s = read_param("s")
    plate.cx = read_param("cx")
    plate.cy = read_param("cy")
    plate.L = read_param("L")

def apply_params_b():
    # Update Model B parameters from entries
    plate.t_edge = read_param("t_edge")
    plate.t0 = read_param("t0")
    plate.L = read_param("L")

def apply_params_c():
    # Update Model C parameters from entries
    plate.t_edge = read_param("t_edge")
    plate.t1 = read_param("t1")
    plate.s1 = read_param("s1")
    plate.cx1 = read_param("cx1")
    plate.cy1 = read_param("cy1")
    plate.t2 = read_param("t2")
    plate.s2 = read_param("s2")
    plate.cx2 = read_param("cx2")
    plate.cy2 = read_param("cy2")
    plate.L = read_param("L")

def validate_plate_params():
    # Check that plate dimensions and dispersion are physically valid
    if plate.L <= 0.0:
        return "Plate size L must be positive."
    if plate.model == "A" and plate.s <= 0.0:
        return "Dispersion s must be positive."
    if plate.model == "C":
        if plate.s1 <= 0.0 or plate.s2 <= 0.0:
            return "Dispersions s1 and s2 must be positive."
    return ""

def apply_parameters():
    # Apply button callback to read and update plate settings
    try:
        if plate.model == "A":
            apply_params_a()
        elif plate.model == "B":
            apply_params_b()
        else:
            apply_params_c()
    except ValueError:
        messagebox.showwarning("Warning", "All parameters must be valid numbers.")
        return
    err = validate_plate_params()
    if err != "":
        messagebox.showwarning("Warning", err)
        return
    draw_heatmap()
    draw_blank_cooling()
    calculate_summary()
    lbl_param_status.config(text="Parameters applied.")

def build_param_fields():
    # Rebuild entry boxes for the selected model
    for child in param_frame.winfo_children():
        child.destroy()
    entry_dict.clear()
    if plate.model == "A":
        params = [("T_edge", "t_edge", plate.t_edge), ("T0", "t0", plate.t0), ("s", "s", plate.s), ("cx", "cx", plate.cx), ("cy", "cy", plate.cy), ("L", "L", plate.L)]
    elif plate.model == "B":
        params = [("T_edge", "t_edge", plate.t_edge), ("T0", "t0", plate.t0), ("L", "L", plate.L)]
    else:
        params = [("T_edge", "t_edge", plate.t_edge), ("t1", "t1", plate.t1), ("s1", "s1", plate.s1), ("cx1", "cx1", plate.cx1), ("cy1", "cy1", plate.cy1), ("t2", "t2", plate.t2), ("s2", "s2", plate.s2), ("cx2", "cx2", plate.cx2), ("cy2", "cy2", plate.cy2), ("L", "L", plate.L)]
    for i in range(len(params)):
        item = params[i]
        lbl = tk.Label(param_frame, text=item[0] + ":")
        lbl.grid(row=i, column=0, padx=5, pady=3, sticky="e")
        ent = tk.Entry(param_frame, width=10)
        ent.insert(0, str(item[2]))
        ent.grid(row=i, column=1, padx=5, pady=3)
        entry_dict[item[1]] = ent

def on_model_select(event):
    # Dropdown callback when user switches model
    chosen = model_combo.get()
    plate.set_model(chosen)
    build_param_fields()
    draw_heatmap()
    draw_blank_cooling()
    calculate_summary()
    lbl_param_status.config(text="Model switched to " + chosen)

def draw_heatmap():
    # Draw heat map, contour lines, and gradient vectors on Tab 1
    fig_map.clf()
    ax = fig_map.add_subplot(111)
    xs = np.linspace(0.0, plate.L, 50)
    ys = np.linspace(0.0, plate.L, 50)
    X, Y = np.meshgrid(xs, ys)
    Z = plate.get_temp(X, Y)
    im = ax.imshow(Z, origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    ax.contour(X, Y, Z, colors="white", linewidths=0.5)
    q_xs = np.linspace(0.3, plate.L - 0.3, 10)
    q_ys = np.linspace(0.3, plate.L - 0.3, 10)
    QX, QY = np.meshgrid(q_xs, q_ys)
    Tx, Ty = plate.get_grad(QX, QY)
    ax.quiver(QX, QY, Tx, Ty, color="cyan", alpha=0.8)
    fig_map.colorbar(im, ax=ax, label="Temperature (deg C)")
    ax.set_title("Temperature Field & Gradient Arrows (Model " + plate.model + ")")
    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    fig_map.tight_layout()
    canvas_map.draw()

def show_lookup():
    # Point Lookup button callback
    try:
        x = float(entry_lookup_x.get().strip())
        y = float(entry_lookup_y.get().strip())
    except ValueError:
        messagebox.showwarning("Warning", "Coordinates must be valid numbers.")
        return
    if x < 0.0 or x > plate.L or y < 0.0 or y > plate.L:
        messagebox.showwarning("Warning", "Coordinates must be between 0 and " + str(plate.L))
        return
    t = plate.get_temp(x, y)
    tx, ty, mag = calculus.gradient(plate, x, y)
    txx, tyy, txy, d, result = calculus.second_derivative_test(plate, x, y)
    res = "Point (" + str(round(x, 2)) + ", " + str(round(y, 2)) + "):\n\n"
    res = res + "Temperature T: " + str(round(t, 2)) + " deg C\n"
    res = res + "Gradient Tx: " + str(round(tx, 3)) + "\n"
    res = res + "Gradient Ty: " + str(round(ty, 3)) + "\n"
    res = res + "Gradient Magnitude: " + str(round(mag, 3)) + " deg C/cm\n\n"
    res = res + "Second Partials:\n"
    res = res + "  Txx: " + str(round(txx, 3)) + ", Tyy: " + str(round(tyy, 3)) + ", Txy: " + str(round(txy, 3)) + "\n\n"
    res = res + "Discriminant D: " + str(round(d, 2)) + "\n"
    res = res + "Classification: " + result
    lbl_lookup_result.config(text=res)

def calculate_summary():
    # Plate Summary button callback
    hx, hy, ht = calculus.find_hottest_point(plate, n_grid=60)
    risk = calculus.get_risk_level(ht)
    avg_t = calculus.average_temperature(plate, n_steps=60)
    lbl_hottest.config(text="Hottest Point: (" + str(round(hx, 2)) + ", " + str(round(hy, 2)) + ") cm\nPeak Temperature: " + str(round(ht, 2)) + " deg C")
    lbl_risk.config(text="Thermal Risk Level: " + risk)
    if risk == "Low":
        lbl_risk.config(fg="green")
    elif risk == "Medium":
        lbl_risk.config(fg="darkorange")
    else:
        lbl_risk.config(fg="red")
    lbl_avg.config(text="Average Plate Temperature: " + str(round(avg_t, 2)) + " deg C")

def draw_blank_cooling():
    # Reset cooling tab plot with background heat map
    fig_cool.clf()
    ax = fig_cool.add_subplot(111)
    xs = np.linspace(0.0, plate.L, 50)
    ys = np.linspace(0.0, plate.L, 50)
    X, Y = np.meshgrid(xs, ys)
    Z = plate.get_temp(X, Y)
    im = ax.imshow(Z, origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    fig_cool.colorbar(im, ax=ax, label="Temperature (deg C)")
    ax.set_title("Cooling Trajectory (Model " + plate.model + ")")
    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    fig_cool.tight_layout()
    canvas_cool.draw()

def draw_cooling_path(path):
    # Draw descent trajectory line over cooling heat map
    draw_blank_cooling()
    ax = fig_cool.axes[0]
    px = []
    py = []
    for i in range(len(path)):
        px.append(path[i][0])
        py.append(path[i][1])
    ax.plot(px, py, "w--", linewidth=2, label="Descent Path")
    ax.plot(px[0], py[0], "go", markersize=8, label="Start")
    ax.plot(px[-1], py[-1], "co", markersize=8, label="End (Cooler)")
    ax.legend(loc="upper right")
    canvas_cool.draw()

def run_descent():
    # Move chip button callback to run gradient descent
    try:
        sx = float(entry_cool_x.get().strip())
        sy = float(entry_cool_y.get().strip())
    except ValueError:
        messagebox.showwarning("Warning", "Coordinates must be valid numbers.")
        return
    if sx < 0.0 or sx > plate.L or sy < 0.0 or sy > plate.L:
        messagebox.showwarning("Warning", "Coordinates must be between 0 and " + str(plate.L))
        return
    start_t = plate.get_temp(sx, sy)
    path, final_t = calculus.gradient_descent(plate, sx, sy, step_size=0.08, steps=30)
    cooling = start_t - final_t
    draw_cooling_path(path)
    end_pt = path[-1]
    msg = "Start Temp: " + str(round(start_t, 2)) + " deg C  |  "
    msg = msg + "End Pos: (" + str(round(end_pt[0], 2)) + ", " + str(round(end_pt[1], 2)) + ")  |  "
    msg = msg + "End Temp: " + str(round(final_t, 2)) + " deg C  |  "
    msg = msg + "Cooling: " + str(round(cooling, 2)) + " deg C"
    lbl_cool_result.config(text=msg)

def save_report():
    # Save button callback to write summary to file
    hx, hy, ht = calculus.find_hottest_point(plate, n_grid=50)
    risk = calculus.get_risk_level(ht)
    avg_t = calculus.average_temperature(plate, n_steps=60)
    metrics = ["Model", "Peak_X", "Peak_Y", "Peak_Temp", "Risk_Level", "Average_Temp"]
    values = [plate.model, round(hx, 2), round(hy, 2), round(ht, 2), risk, round(avg_t, 2)]
    fmt = combo_save.get().upper()
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

def setup_left_panel(parent):
    # Build left panel widgets for model and parameters
    global model_combo, param_frame, lbl_param_status
    left = tk.Frame(parent, width=240, padx=10, pady=10)
    left.grid(row=0, column=0, sticky="nsw")
    title = tk.Label(left, text="Model & Parameters", font=("Arial", 12, "bold"))
    title.grid(row=0, column=0, columnspan=2, pady=5)
    lbl_m = tk.Label(left, text="Select Model:")
    lbl_m.grid(row=1, column=0, sticky="w", pady=5)
    model_combo = ttk.Combobox(left, values=["A", "B", "C"], state="readonly", width=8)
    model_combo.set("A")
    model_combo.grid(row=1, column=1, sticky="w", pady=5)
    model_combo.bind("<<ComboboxSelected>>", on_model_select)
    param_frame = tk.Frame(left)
    param_frame.grid(row=2, column=0, columnspan=2, pady=10)
    btn_apply = tk.Button(left, text="Apply Parameters", command=apply_parameters, width=16)
    btn_apply.grid(row=3, column=0, columnspan=2, pady=5)
    lbl_param_status = tk.Label(left, text="", fg="blue")
    lbl_param_status.grid(row=4, column=0, columnspan=2, pady=5)

def setup_tab_heatmap(parent):
    # Setup embedded canvas for Tab 1 Heat Map
    global fig_map, canvas_map
    tab = tk.Frame(parent, padx=10, pady=10)
    fig_map = Figure(figsize=(6.5, 5.2), dpi=100)
    canvas_map = FigureCanvasTkAgg(fig_map, master=tab)
    canvas_widget = canvas_map.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky="nsew")
    return tab

def setup_tab_lookup(parent):
    # Setup widgets for Tab 2 Point Lookup
    global entry_lookup_x, entry_lookup_y, lbl_lookup_result
    tab = tk.Frame(parent, padx=15, pady=15)
    top_box = tk.Frame(tab)
    top_box.grid(row=0, column=0, sticky="w", pady=10)
    lbl_x = tk.Label(top_box, text="x (cm):")
    lbl_x.grid(row=0, column=0, padx=5)
    entry_lookup_x = tk.Entry(top_box, width=8)
    entry_lookup_x.insert(0, "2.0")
    entry_lookup_x.grid(row=0, column=1, padx=5)
    lbl_y = tk.Label(top_box, text="y (cm):")
    lbl_y.grid(row=0, column=2, padx=5)
    entry_lookup_y = tk.Entry(top_box, width=8)
    entry_lookup_y.insert(0, "2.0")
    entry_lookup_y.grid(row=0, column=3, padx=5)
    btn = tk.Button(top_box, text="Calculate", command=show_lookup, width=12)
    btn.grid(row=0, column=4, padx=10)
    lbl_lookup_result = tk.Label(tab, text="Enter coordinates and click Calculate.", justify="left", font=("Consolas", 10))
    lbl_lookup_result.grid(row=1, column=0, sticky="w", pady=10)
    return tab

def setup_tab_summary(parent):
    # Setup widgets for Tab 3 Plate Summary
    global lbl_hottest, lbl_risk, lbl_avg
    tab = tk.Frame(parent, padx=20, pady=20)
    btn = tk.Button(tab, text="Refresh Summary", command=calculate_summary, width=18)
    btn.grid(row=0, column=0, sticky="w", pady=10)
    lbl_hottest = tk.Label(tab, text="", font=("Arial", 11), justify="left")
    lbl_hottest.grid(row=1, column=0, sticky="w", pady=10)
    lbl_risk = tk.Label(tab, text="", font=("Arial", 12, "bold"), justify="left")
    lbl_risk.grid(row=2, column=0, sticky="w", pady=10)
    lbl_avg = tk.Label(tab, text="", font=("Arial", 11), justify="left")
    lbl_avg.grid(row=3, column=0, sticky="w", pady=10)
    return tab

def setup_tab_cooling(parent):
    # Setup widgets for Tab 4 Cooling
    global entry_cool_x, entry_cool_y, lbl_cool_result, fig_cool, canvas_cool
    tab = tk.Frame(parent, padx=10, pady=10)
    top_box = tk.Frame(tab)
    top_box.grid(row=0, column=0, sticky="w", pady=5)
    lbl_x = tk.Label(top_box, text="Start x (cm):")
    lbl_x.grid(row=0, column=0, padx=5)
    entry_cool_x = tk.Entry(top_box, width=8)
    entry_cool_x.insert(0, "1.5")
    entry_cool_x.grid(row=0, column=1, padx=5)
    lbl_y = tk.Label(top_box, text="Start y (cm):")
    lbl_y.grid(row=0, column=2, padx=5)
    entry_cool_y = tk.Entry(top_box, width=8)
    entry_cool_y.insert(0, "1.5")
    entry_cool_y.grid(row=0, column=3, padx=5)
    btn = tk.Button(top_box, text="Move Chip", command=run_descent, width=12)
    btn.grid(row=0, column=4, padx=10)
    lbl_cool_result = tk.Label(tab, text="Click Move Chip to run gradient descent.", font=("Arial", 9))
    lbl_cool_result.grid(row=1, column=0, sticky="w", pady=5)
    fig_cool = Figure(figsize=(6.0, 4.2), dpi=100)
    canvas_cool = FigureCanvasTkAgg(fig_cool, master=tab)
    canvas_cool.get_tk_widget().grid(row=2, column=0, sticky="nsew", pady=5)
    return tab

def setup_tab_save(parent):
    # Setup widgets for Tab 5 Save
    global combo_save, lbl_save_status
    tab = tk.Frame(parent, padx=20, pady=20)
    lbl_title = tk.Label(tab, text="Export Plate Report", font=("Arial", 12, "bold"))
    lbl_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=10)
    lbl_fmt = tk.Label(tab, text="Choose Format:")
    lbl_fmt.grid(row=1, column=0, sticky="w", pady=5)
    combo_save = ttk.Combobox(tab, values=["CSV", "TXT"], state="readonly", width=8)
    combo_save.set("CSV")
    combo_save.grid(row=1, column=1, sticky="w", padx=10, pady=5)
    btn = tk.Button(tab, text="Save Report", command=save_report, width=16)
    btn.grid(row=2, column=0, columnspan=2, sticky="w", pady=15)
    lbl_save_status = tk.Label(tab, text="", fg="green", font=("Arial", 10))
    lbl_save_status.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
    return tab

def main():
    # Build complete window and launch GUI event loop
    global root
    root = tk.Tk()
    root.title("CalSymPy - Heat Distribution")
    root.geometry("1100x700")
    setup_left_panel(root)
    tabs = ttk.Notebook(root)
    tabs.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    tabs.add(setup_tab_heatmap(tabs), text="Heat Map")
    tabs.add(setup_tab_lookup(tabs), text="Point Lookup")
    tabs.add(setup_tab_summary(tabs), text="Plate Summary")
    tabs.add(setup_tab_cooling(tabs), text="Cooling")
    tabs.add(setup_tab_save(tabs), text="Save")
    build_param_fields()
    draw_heatmap()
    draw_blank_cooling()
    calculate_summary()
    root.mainloop()

if __name__ == "__main__":
    main()
