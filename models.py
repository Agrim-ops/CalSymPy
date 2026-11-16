# models.py - temperature formulas and hand-derived derivatives
import numpy as np

# Calculates temperature for Model A (circular Gaussian hotspot).
# Inputs: coordinates x, y and hotspot parameters (t_edge, t0, s, cx, cy).
# Output: temperature value T in degrees C.
# Formula: T = t_edge + t0 * exp(-((x - cx)^2 + (y - cy)^2) / s).
def temp_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    return t_edge + t0 * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / s)

# Computes analytical first partial derivatives Tx and Ty for Model A.
# Inputs: coordinates x, y and hotspot parameters.
# Output: tuple (Tx, Ty) representing the gradient vector.
# Uses chain rule on exp(-r^2/s) where r^2 = (x - cx)^2 + (y - cy)^2.
def grad_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    # Chain rule on exp(-u): d/dx [r2/s] = 2*(x-cx)/s -> Tx = -2*T0*(x-cx)/s * exp(-r2/s)
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    factor = t0 * np.exp(-r2 / s) * (-2.0 / s)
    return factor * (x - cx), factor * (y - cy)

# Computes analytical second partial derivatives Txx, Tyy, and Txy for Model A.
# Inputs: coordinates x, y and hotspot parameters.
# Output: tuple (Txx, Tyy, Txy) for the Hessian matrix and D-test.
# Uses product rule on Tx and Ty to get second derivatives.
def hessian_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    # Product rule on Tx: d/dx [factor * (x-cx)] -> Txx = e*(4*(x-cx)^2/s^2 - 2/s)
    # Mixed partial: d/dy Tx -> Txy = e*(4*(x-cx)*(y-cy)/s^2)
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    e = t0 * np.exp(-r2 / s)
    txx = e * (4.0 * ((x - cx) ** 2) / (s ** 2) - 2.0 / s)
    tyy = e * (4.0 * ((y - cy) ** 2) / (s ** 2) - 2.0 / s)
    txy = e * (4.0 * (x - cx) * (y - cy) / (s ** 2))
    return txx, tyy, txy

# Calculates temperature for Model B (sinusoidal standing wave).
# Inputs: coordinates x, y and parameters t_edge, t0, and plate size L.
# Output: temperature value T in degrees C.
# Formula: T = t_edge + t0 * sin(pi * x / L) * sin(pi * y / L).
def temp_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    return t_edge + t0 * np.sin(np.pi * x / L) * np.sin(np.pi * y / L)

# Computes analytical first partial derivatives Tx and Ty for Model B.
# Inputs: coordinates x, y and plate parameters (t_edge, t0, L).
# Output: tuple (Tx, Ty) giving the gradient vector components.
# Uses chain rule: d/dx sin(pi*x/L) = (pi/L)*cos(pi*x/L).
def grad_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    # Chain rule: d/dx sin(pi*x/L) = (pi/L)*cos(pi*x/L)
    u, v = np.pi * x / L, np.pi * y / L
    scale = t0 * (np.pi / L)
    return scale * np.cos(u) * np.sin(v), scale * np.sin(u) * np.cos(v)

# Computes analytical second partial derivatives Txx, Tyy, and Txy for Model B.
# Inputs: coordinates x, y and plate parameters (t_edge, t0, L).
# Output: tuple (Txx, Tyy, Txy) for curvature and discriminant D.
# Differentiates Tx and Ty with respect to x and y.
def hessian_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    # Second derivative: d/dx cos(pi*x/L) = -(pi/L)*sin(pi*x/L)
    u, v = np.pi * x / L, np.pi * y / L
    factor = t0 * ((np.pi / L) ** 2)
    txx = -factor * np.sin(u) * np.sin(v)
    return txx, txx, factor * np.cos(u) * np.cos(v)

# Plate object holding parameters and dispatching model formulas
class Plate:
    # Initializes the square plate instance with default dimensions and model.
    # Inputs: model name string ("A" or "B").
    # Sets default plate size L=4.0 cm and delegates to set_model().
    def __init__(self, model="A"):
        self.L, self.s, self.cx, self.cy = 4.0, 2.0, 2.0, 2.0
        self.set_model(model)

    # Configures the active model type and restores default model parameters.
    # Inputs: model name string ("A" for hotspot, "B" for sine plate).
    # Updates plate attributes (t_edge, t0, and s, cx, cy for Model A).
    def set_model(self, model):
        self.model = model
        if model == "A":
            self.t_edge, self.t0, self.s, self.cx, self.cy = 25.0, 60.0, 2.0, 2.0, 2.0
        else:
            self.t_edge, self.t0 = 20.0, 50.0

    # Evaluates plate surface temperature at the specified coordinates.
    # Inputs: x and y coordinates on the plate.
    # Output: temperature T in degrees C dispatched from the active model.
    def get_temp(self, x, y):
        if self.model == "A":
            return temp_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return temp_b(x, y, self.t_edge, self.t0, self.L)

    # Evaluates the gradient vector components at given coordinates.
    # Inputs: x and y coordinates on the plate.
    # Output: tuple (Tx, Ty) dispatched from the active model.
    def get_grad(self, x, y):
        if self.model == "A":
            return grad_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return grad_b(x, y, self.t_edge, self.t0, self.L)

    # Evaluates second partial derivatives at given coordinates.
    # Inputs: x and y coordinates on the plate.
    # Output: tuple (Txx, Tyy, Txy) dispatched from the active model.
    def get_hessian(self, x, y):
        if self.model == "A":
            return hessian_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return hessian_b(x, y, self.t_edge, self.t0, self.L)
