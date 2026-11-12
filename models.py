# models.py - temperature formulas and hand-derived derivatives
import numpy as np

# Model A: Single hotspot T = T_edge + T0 * exp(-r^2 / s)
def temp_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    return t_edge + t0 * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / s)

def grad_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    # Chain rule on exp(-u): d/dx [r2/s] = 2*(x-cx)/s -> Tx = -2*T0*(x-cx)/s * exp(-r2/s)
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    factor = t0 * np.exp(-r2 / s) * (-2.0 / s)
    return factor * (x - cx), factor * (y - cy)

def hessian_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    # Product rule on Tx: d/dx [factor * (x-cx)] -> Txx = e*(4*(x-cx)^2/s^2 - 2/s)
    # Mixed partial: d/dy Tx -> Txy = e*(4*(x-cx)*(y-cy)/s^2)
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    e = t0 * np.exp(-r2 / s)
    txx = e * (4.0 * ((x - cx) ** 2) / (s ** 2) - 2.0 / s)
    tyy = e * (4.0 * ((y - cy) ** 2) / (s ** 2) - 2.0 / s)
    txy = e * (4.0 * (x - cx) * (y - cy) / (s ** 2))
    return txx, tyy, txy

# Model B: Sine plate T = T_edge + T0 * sin(pi*x/L) * sin(pi*y/L)
def temp_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    return t_edge + t0 * np.sin(np.pi * x / L) * np.sin(np.pi * y / L)

def grad_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    # Chain rule: d/dx sin(pi*x/L) = (pi/L)*cos(pi*x/L)
    u, v = np.pi * x / L, np.pi * y / L
    tx = t0 * (np.pi / L) * np.cos(u) * np.sin(v)
    ty = t0 * (np.pi / L) * np.sin(u) * np.cos(v)
    return tx, ty

def hessian_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    # Second derivative: d/dx cos(pi*x/L) = -(pi/L)*sin(pi*x/L)
    u, v = np.pi * x / L, np.pi * y / L
    factor = t0 * ((np.pi / L) ** 2)
    txx = -factor * np.sin(u) * np.sin(v)
    tyy = -factor * np.sin(u) * np.sin(v)
    txy = factor * np.cos(u) * np.cos(v)
    return txx, tyy, txy

class Plate:
    def __init__(self, model="A"):
        self.L, self.s, self.cx, self.cy = 4.0, 2.0, 2.0, 2.0
        self.set_model(model)

    def set_model(self, model):
        self.model = model
        if model == "A":
            self.t_edge, self.t0, self.s, self.cx, self.cy = 25.0, 60.0, 2.0, 2.0, 2.0
        elif model == "B":
            self.t_edge, self.t0 = 20.0, 50.0

    def get_temp(self, x, y):
        if self.model == "A":
            return temp_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return temp_b(x, y, self.t_edge, self.t0, self.L)

    def get_grad(self, x, y):
        if self.model == "A":
            return grad_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return grad_b(x, y, self.t_edge, self.t0, self.L)

    def get_hessian(self, x, y):
        if self.model == "A":
            return hessian_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        return hessian_b(x, y, self.t_edge, self.t0, self.L)
