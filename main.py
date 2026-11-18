# main.py - interactive menu for temperature calculus
import pandas as pd
import models
import calculus
import plots

# Prints the numbered options menu for the interactive console.
# Inputs: none.
# Outputs: none (prints menu list to terminal).
# Displays choices 0 to 7 for all available program features.
def show_menu():
    print("\n--- CalSymPy Menu ---")
    print("1. Model & params\n2. Heat map\n3. Point lookup\n4. Hottest point\n5. Average temp\n6. Gradient descent\n7. Save report\n0. Quit")

# Prompts user for a numerical parameter and validates positive bounds.
# Inputs: parameter name string and current default value.
# Output: updated float value, or current value if input is empty/invalid.
# Enforces strictly positive values for plate size L and hotspot width s.
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

# Handles menu option 1 to switch thermal models and modify parameters.
# Inputs: active plate object.
# Outputs: none (modifies plate attributes in place).
# Lets user switch between Model A and Model B and update parameters.
def option_choose_model(plate):
    print("\nCurrent model is:", plate.model)
    m = input("Choose model (A: single hotspot, B: sine plate): ").strip().upper()
    if m in ["A", "B"]:
        plate.set_model(m)
        print("Model switched to:", m)
    if input("Do you want to change parameters? (y/n): ").strip().lower() == "y":
        plate.t_edge = ask_param("T_edge", plate.t_edge)
        plate.t0 = ask_param("T0", plate.t0)
        if plate.model == "A":
            plate.s = ask_param("s", plate.s)
            plate.cx = ask_param("cx", plate.cx)
            plate.cy = ask_param("cy", plate.cy)
        plate.L = ask_param("L", plate.L)

# Handles menu option 3 to look up temperature and derivatives at a point.
# Inputs: active plate object.
# Outputs: none (prints point metrics and D-test classification).
# Validates bounds (0 to L) and computes T, gradient, Hessian, and D.
def option_lookup(plate):
    try:
        x_in = float(input("Enter x coordinate (0 to " + str(plate.L) + "): ").strip())
        y_in = float(input("Enter y coordinate (0 to " + str(plate.L) + "): ").strip())
    except ValueError:
        print("Invalid input coordinates.")
        return
    if x_in < 0.0 or x_in > plate.L or y_in < 0.0 or y_in > plate.L:
        print("Coordinates must be between 0 and " + str(plate.L))
        return
    t = plate.get_temp(x_in, y_in)
    tx, ty, mag = calculus.gradient(plate, x_in, y_in)
    txx, tyy, txy, d, result = calculus.second_derivative_test(plate, x_in, y_in)
    print("\nResults at (" + str(x_in) + ", " + str(y_in) + "):")
    print("Temperature: " + str(round(t, 2)) + " deg C")
    print("Gradient: Tx = " + str(round(tx, 3)) + ", Ty = " + str(round(ty, 3)) + " (mag = " + str(round(mag, 3)) + " deg C/cm)")
    print("Second partials: Txx = " + str(round(txx, 3)) + ", Tyy = " + str(round(tyy, 3)) + ", Txy = " + str(round(txy, 3)))
    print("Discriminant D: " + str(round(d, 2)) + " (" + result + ")")

# Handles menu option 4 to find the peak temperature and cooling suggestions.
# Inputs: active plate object.
# Outputs: none (prints peak coordinates, risk level, and suggestions).
# Uses grid search to find the hotspot and outputs rules-of-thumb advice.
def option_hottest(plate):
    print("\nSearching grid for hottest point...")
    hx, hy, ht = calculus.find_hottest_point(plate, n_grid=60)
    print("Hottest point is at x = " + str(round(hx, 2)) + " cm, y = " + str(round(hy, 2)) + " cm")
    print("Peak temperature: " + str(round(ht, 2)) + " deg C (" + calculus.get_risk_level(ht) + " risk)")
    print("\nCooling suggestions:")
    for tip in calculus.cooling_suggestions(ht):
        print("- " + tip)
    print("These are simple rules of thumb, not engineering advice.")

# Handles menu option 5 to calculate average plate temperature.
# Inputs: active plate object.
# Outputs: none (prints estimated average temperature).
# Evaluates a 2D midpoint Riemann sum over [0, L] x [0, L].
def option_average(plate):
    print("\nCalculating double integral Riemann sum...")
    avg = calculus.average_temperature(plate, n_steps=80)
    print("Average plate temperature: " + str(round(avg, 2)) + " deg C")

# Handles menu option 6 to simulate downhill chip cooling relocation.
# Inputs: active plate object.
# Outputs: none (prints trajectory and optionally plots path).
# Moves along the unit downhill gradient vector step by step to cool the chip.
def option_descent(plate):
    try:
        val_x = input("Enter initial chip x (default 1.5): ").strip()
        val_y = input("Enter initial chip y (default 1.5): ").strip()
        sx = 1.5 if val_x == "" else float(val_x)
        sy = 1.5 if val_y == "" else float(val_y)
    except ValueError:
        print("Invalid input coordinates.")
        return
    if sx < 0.0 or sx > plate.L or sy < 0.0 or sy > plate.L:
        print("Coordinates must be between 0 and " + str(plate.L))
        return
    start_t = plate.get_temp(sx, sy)
    path, final_t = calculus.gradient_descent(plate, sx, sy)
    print("\nInitial temperature at (" + str(sx) + ", " + str(sy) + "): " + str(round(start_t, 2)) + " deg C")
    print("Final position: (" + str(round(path[-1][0], 2)) + ", " + str(round(path[-1][1], 2)) + ")")
    print("Final temperature: " + str(round(final_t, 2)) + " deg C (cooling: " + str(round(start_t - final_t, 2)) + " deg C)")
    if input("Show descent path plot? (y/n): ").strip().lower() == "y":
        plots.plot_descent_path(plate, path)

# Handles menu option 7 to export summary plate metrics to a file.
# Inputs: active plate object.
# Outputs: none (writes a CSV or text file to local disk).
# Exports peak coordinates, risk level, and average temperature with error handling.
def option_save_report(plate):
    hx, hy, ht = calculus.find_hottest_point(plate, n_grid=50)
    avg_t = calculus.average_temperature(plate, n_steps=60)
    metrics = ["Model", "Peak_X", "Peak_Y", "Peak_Temp", "Risk_Level", "Average_Temp"]
    values = [plate.model, round(hx, 2), round(hy, 2), round(ht, 2), calculus.get_risk_level(ht), round(avg_t, 2)]
    fmt = input("Save format (1 for .csv, 2 for .txt): ").strip()
    filename = "report_" + plate.model + (".csv" if fmt == "1" else ".txt")
    try:
        if fmt == "1":
            pd.DataFrame({"Metric": metrics, "Value": values}).to_csv(filename, index=False)
        else:
            with open(filename, "w") as f:
                for i in range(len(metrics)):
                    f.write(str(metrics[i]) + ": " + str(values[i]) + "\n")
        print("Saved report to " + filename)
    except (IOError, OSError):
        print("Error: Could not save report to " + filename)

# Main execution loop displaying the menu and dispatching user choices.
# Inputs: none.
# Outputs: none (runs interactive loop until choice 0 is entered).
# Initializes a Plate object and routes commands to option functions.
def main():
    plate = models.Plate("A")
    print("Welcome to CalSymPy (MAT 112 Engineering Mathematics & Python)")
    choice = ""
    while choice != "0":
        show_menu()
        choice = input("Enter choice (0-7): ").strip()
        if choice == "1": option_choose_model(plate)
        elif choice == "2": plots.plot_heatmap(plate)
        elif choice == "3": option_lookup(plate)
        elif choice == "4": option_hottest(plate)
        elif choice == "5": option_average(plate)
        elif choice == "6": option_descent(plate)
        elif choice == "7": option_save_report(plate)
        elif choice != "0": print("Invalid option. Please choose 0 to 7.")
    print("Exiting CalSymPy. Goodbye!")

if __name__ == "__main__":
    main()
