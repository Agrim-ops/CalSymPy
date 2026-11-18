# plots.py - visual plots using matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Draws a 2D color heatmap and contour lines of the temperature distribution.
# Inputs: plate object, grid resolution n_grid, and boolean flag show.
# Output: Matplotlib Figure object displaying the heat map.
# Uses imshow with inferno colormap and overlays white contour lines.
def plot_heatmap(plate, n_grid=50, show=True):
    xs = np.linspace(0.0, plate.L, n_grid)
    x_grid, y_grid = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(6, 5))
    im = plt.imshow(plate.get_temp(x_grid, y_grid), origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    plt.colorbar(im, label="Temperature (deg C)")
    plt.contour(x_grid, y_grid, plate.get_temp(x_grid, y_grid), colors="white", linewidths=0.5)
    plt.title("Temperature Map: Model " + plate.model)
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    plt.tight_layout()
    if show:
        plt.show()
    return fig

# Overlays the downhill gradient descent trajectory on the temperature map.
# Inputs: plate object, path coordinate list, grid resolution n_grid, and show flag.
# Output: Matplotlib Figure object with the path and start/end markers.
# Draws the background temperature surface and marks path steps from hot to cool.
def plot_descent_path(plate, path, n_grid=50, show=True, best_point=None):
    xs = np.linspace(0.0, plate.L, n_grid)
    x_grid, y_grid = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(6, 5))
    plt.imshow(plate.get_temp(x_grid, y_grid), origin="lower", extent=[0, plate.L, 0, plate.L], cmap="inferno")
    px, py = [], []
    for pt in path:
        px.append(pt[0])
        py.append(pt[1])
    plt.plot(px, py, "w--", linewidth=2, label="Descent Path")
    plt.plot(px[0], py[0], "go", markersize=8, label="Start")
    plt.plot(px[-1], py[-1], "co", markersize=8, label="End (Cooler)")
    if best_point is not None:
        plt.plot(best_point[0], best_point[1], "y*", markersize=12, label="Best Placement")
    plt.title("Gradient Descent: Chip Relocation")
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
    return fig
