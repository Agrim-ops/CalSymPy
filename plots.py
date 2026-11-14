# plots.py - visual plots using matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Visualizes 2D temperature field with heatmap and contours
def plot_heatmap(plate, n_grid=50, show=True):
    xs = np.linspace(0.0, plate.L, n_grid)
    X, Y = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(6, 5))
    im = plt.imshow(plate.get_temp(X, Y), origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    plt.colorbar(im, label="Temperature (deg C)")
    plt.contour(X, Y, plate.get_temp(X, Y), colors="white", linewidths=0.5)
    plt.title("Temperature Map: Model " + plate.model)
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    plt.tight_layout()
    if show:
        plt.show()
    return fig

# Plots gradient descent cooling path over temperature map
def plot_descent_path(plate, path, n_grid=50, show=True):
    xs = np.linspace(0.0, plate.L, n_grid)
    X, Y = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(6, 5))
    plt.imshow(plate.get_temp(X, Y), origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    px, py = [], []
    for pt in path:
        px.append(pt[0])
        py.append(pt[1])
    plt.plot(px, py, "w--", linewidth=2, label="Descent Path")
    plt.plot(px[0], py[0], "go", markersize=8, label="Start")
    plt.plot(px[-1], py[-1], "co", markersize=8, label="End (Cooler)")
    plt.title("Gradient Descent: Chip Relocation")
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
    return fig
