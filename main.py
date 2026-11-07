# main.py - interactive menu for temperature calculus
import pandas as pd
import models
import calculus
import plots

def show_menu():
    print("\n--- CalSymPy Menu ---")
    print("1. Choose model and change parameters")
    print("2. Show temperature heat map")
    print("3. Point lookup (T, gradient, D-test)")
    print("4. Find hottest point and risk level")
    print("5. Calculate average temperature (double integral)")
    print("6. Move chip with gradient descent")
    print("7. Save results report (.txt or .csv)")
    print("0. Quit")

def option_choose_model(plate):
    print("\nCurrent model is:", plate.model)
    m = input("Choose model (A: single hotspot, B: sine plate, C: two hotspots): ").strip().upper()
    if m in ["A", "B", "C"]:
        plate.set_model(m)
        print("Model switched to:", m)
    
    ans = input("Do you want to change parameters? (y/n): ").strip().lower()
    if ans == "y":
        try:
            val = input("Enter T_edge (current " + str(plate.t_edge) + "): ").strip()
            if val != "":
                plate.t_edge = float(val)
            val = input("Enter T0 (current " + str(plate.t0) + "): ").strip()
            if val != "":
                plate.t0 = float(val)
            if plate.model == "A":
                val = input("Enter s dispersion (current " + str(plate.s) + "): ").strip()
                if val != "":
                    plate.s = float(val)
        except ValueError:
            print("Invalid number entered. Keeping previous values.")

def option_lookup(plate):
    try:
        x_in = float(input("Enter x coordinate (0 to " + str(plate.L) + "): ").strip())
        y_in = float(input("Enter y coordinate (0 to " + str(plate.L) + "): ").strip())
    except ValueError:
        print("Invalid input coordinates.")
        return

    t = plate.get_temp(x_in, y_in)
    tx, ty, mag = calculus.gradient(plate, x_in, y_in)
    txx, tyy, txy, d, result = calculus.second_derivative_test(plate, x_in, y_in)

    print("\nResults at (" + str(x_in) + ", " + str(y_in) + "):")
    print("Temperature: " + str(round(t, 2)) + " deg C")
    print("Gradient: Tx = " + str(round(tx, 3)) + ", Ty = " + str(round(ty, 3)))
    print("Gradient magnitude: " + str(round(mag, 3)) + " deg C/cm")
    print("Second partials: Txx = " + str(round(txx, 3)) + ", Tyy = " + str(round(tyy, 3)) + ", Txy = " + str(round(txy, 3)))
    print("Discriminant D: " + str(round(d, 2)))
    print("Classification: " + result)

def option_hottest(plate):
    print("\nSearching grid for hottest point...")
    hx, hy, ht = calculus.find_hottest_point(plate, n_grid=60)
    risk = calculus.get_risk_level(ht)
    print("Hottest point is at x = " + str(round(hx, 2)) + " cm, y = " + str(round(hy, 2)) + " cm")
    print("Peak temperature: " + str(round(ht, 2)) + " deg C")
    print("Thermal risk level: " + risk)

def option_average(plate):
    print("\nCalculating double integral Riemann sum...")
    avg = calculus.average_temperature(plate, n_steps=80)
    print("Average plate temperature: " + str(round(avg, 2)) + " deg C")

def option_descent(plate):
    try:
        sx = float(input("Enter initial chip x (default 1.5): ") or 1.5)
        sy = float(input("Enter initial chip y (default 1.5): ") or 1.5)
    except ValueError:
        sx = 1.5
        sy = 1.5
    
    start_t = plate.get_temp(sx, sy)
    path, final_t = calculus.gradient_descent(plate, sx, sy, step_size=0.08, steps=30)
    cooling = start_t - final_t

    print("\nInitial temperature at (" + str(sx) + ", " + str(sy) + "): " + str(round(start_t, 2)) + " deg C")
    end_pt = path[-1]
    print("Final position after cooling: (" + str(round(end_pt[0], 2)) + ", " + str(round(end_pt[1], 2)) + ")")
    print("Final temperature: " + str(round(final_t, 2)) + " deg C")
    print("Cooling achieved: " + str(round(cooling, 2)) + " deg C")
    
    show_plot = input("Show descent path plot? (y/n): ").strip().lower()
    if show_plot == "y":
        plots.plot_descent_path(plate, path)

def option_save_report(plate):
    hx, hy, ht = calculus.find_hottest_point(plate, n_grid=50)
    risk = calculus.get_risk_level(ht)
    avg_t = calculus.average_temperature(plate, n_steps=60)
    
    metrics = ["Model", "Peak_X", "Peak_Y", "Peak_Temp", "Risk_Level", "Average_Temp"]
    values = [plate.model, round(hx, 2), round(hy, 2), round(ht, 2), risk, round(avg_t, 2)]
    
    df = pd.DataFrame({"Metric": metrics, "Value": values})
    
    fmt = input("Save format (1 for .csv, 2 for .txt): ").strip()
    if fmt == "1":
        filename = "report_" + plate.model + ".csv"
        df.to_csv(filename, index=False)
        print("Saved report to " + filename)
    else:
        filename = "report_" + plate.model + ".txt"
        f = open(filename, "w")
        for i in range(len(metrics)):
            f.write(str(metrics[i]) + ": " + str(values[i]) + "\n")
        f.close()
        print("Saved report to " + filename)

def main():
    plate = models.Plate("A")
    print("Welcome to CalSymPy (MAT 112 Engineering Mathematics & Python)")
    
    running = True
    while running:
        show_menu()
        choice = input("Enter choice (0-7): ").strip()
        if choice == "1":
            option_choose_model(plate)
        elif choice == "2":
            plots.plot_heatmap(plate)
        elif choice == "3":
            option_lookup(plate)
        elif choice == "4":
            option_hottest(plate)
        elif choice == "5":
            option_average(plate)
        elif choice == "6":
            option_descent(plate)
        elif choice == "7":
            option_save_report(plate)
        elif choice == "0":
            print("Exiting CalSymPy. Goodbye!")
            running = False
        else:
            print("Invalid option. Please choose 0 to 7.")

if __name__ == "__main__":
    main()
