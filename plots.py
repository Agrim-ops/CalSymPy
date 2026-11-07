# plots.py - visual plots using matplotlib
import numpy as np
import matplotlib.pyplot as plt

def plot_heatmap(plate, n_grid=50):
    # Heat map with contour lines
    xs = np.linspace(0.0, plate.L, n_grid)
    ys = np.linspace(0.0, plate.L, n_grid)
    X, Y = np.meshgrid(xs, ys)
    Z = plate.get_temp(X, Y)

    plt.figure(figsize=(6, 5))
    im = plt.imshow(Z, origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    plt.colorbar(im, label="Temperature (deg C)")
    plt.contour(X, Y, Z, colors="white", linewidths=0.5)
    plt.title("Temperature Map: Model " + plate.model)
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    plt.tight_layout()
    plt.show()

def plot_quiver(plate, n_grid=12):
    # Arrow plot showing gradient direction
    xs = np.linspace(0.3, plate.L - 0.3, n_grid)
    ys = np.linspace(0.3, plate.L - 0.3, n_grid)
    X, Y = np.meshgrid(xs, ys)
    Tx, Ty = plate.get_grad(X, Y)

    plt.figure(figsize=(6, 5))
    plt.quiver(X, Y, Tx, Ty, color="red")
    plt.title("Gradient Vector Field (Steepest Rise)")
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    plt.xlim(0, plate.L)
    plt.ylim(0, plate.L)
    plt.tight_layout()
    plt.show()

def plot_descent_path(plate, path, n_grid=50):
    # Plot gradient descent path over temperature map
    xs = np.linspace(0.0, plate.L, n_grid)
    ys = np.linspace(0.0, plate.L, n_grid)
    X, Y = np.meshgrid(xs, ys)
    Z = plate.get_temp(X, Y)
    plt.figure(figsize=(6, 5))
    plt.imshow(Z, origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    px = []
    py = []
    for pt in path:
        px.append(pt[0])
        py.append(pt[1])
    plt.plot(px, py, "w--", linewidth=2, label="Descent Path")
    plt.plot(px[0], py[0], "go", markersize=8, label="Start")
    plt.plot(px[-1], py[-1], "co", markersize=8, label="End (Cooler)")
    plt.title("Gradient Descent: Chip Relocation")
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    plt.legend()
    plt.tight_layout()
    plt.show()
