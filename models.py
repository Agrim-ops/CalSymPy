# models.py - temperature formulas and hand-derived derivatives
import numpy as np

# Model A: Single hotspot
# Formula: T = T_edge + T0 * exp(-r^2 / s) where r^2 = (x-cx)^2 + (y-cy)^2
def temp_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    # Gaussian heat source in the center
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    return t_edge + t0 * np.exp(-r2 / s)

def grad_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    # d/dx exp(-u) = -exp(-u) * du/dx, where u = r^2 / s
    # Tx = T0 * exp(-r2/s) * (-2*(x-cx)/s)
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    factor = t0 * np.exp(-r2 / s) * (-2.0 / s)
    tx = factor * (x - cx)
    ty = factor * (y - cy)
    return tx, ty

def hessian_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0):
    # Product rule on Tx: d/dx [factor * (x-cx)]
    # Txx = T0*exp(-r2/s) * (4*(x-cx)^2/s^2 - 2/s)
    # Txy = T0*exp(-r2/s) * (4*(x-cx)*(y-cy)/s^2)
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    e = t0 * np.exp(-r2 / s)
    txx = e * (4.0 * ((x - cx) ** 2) / (s ** 2) - 2.0 / s)
    tyy = e * (4.0 * ((y - cy) ** 2) / (s ** 2) - 2.0 / s)
    txy = e * (4.0 * (x - cx) * (y - cy) / (s ** 2))
    return txx, tyy, txy

# Model B: Sine plate
# Formula: T = T_edge + T0 * sin(pi*x/L) * sin(pi*y/L)
def temp_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    # Standing wave temperature pattern
    u = np.pi * x / L
    v = np.pi * y / L
    return t_edge + t0 * np.sin(u) * np.sin(v)

def grad_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    # d/dx sin(pi*x/L) = (pi/L)*cos(pi*x/L)
    u = np.pi * x / L
    v = np.pi * y / L
    tx = t0 * (np.pi / L) * np.cos(u) * np.sin(v)
    ty = t0 * (np.pi / L) * np.sin(u) * np.cos(v)
    return tx, ty

def hessian_b(x, y, t_edge=20.0, t0=50.0, L=4.0):
    # d/dx cos(pi*x/L) = -(pi/L)*sin(pi*x/L)
    u = np.pi * x / L
    v = np.pi * y / L
    factor = t0 * ((np.pi / L) ** 2)
    txx = -factor * np.sin(u) * np.sin(v)
    tyy = -factor * np.sin(u) * np.sin(v)
    txy = factor * np.cos(u) * np.cos(v)
    return txx, tyy, txy

# Model C: Two hotspots
# Formula: sum of two Gaussians
def temp_c(x, y, t_edge=25.0, t1=40.0, s1=1.5, cx1=1.2, cy1=1.2, t2=40.0, s2=1.5, cx2=2.8, cy2=2.8):
    # Two hot spots added together
    r1 = (x - cx1) ** 2 + (y - cy1) ** 2
    r2 = (x - cx2) ** 2 + (y - cy2) ** 2
    part1 = t1 * np.exp(-r1 / s1)
    part2 = t2 * np.exp(-r2 / s2)
    return t_edge + part1 + part2

def grad_c(x, y, t_edge=25.0, t1=40.0, s1=1.5, cx1=1.2, cy1=1.2, t2=40.0, s2=1.5, cx2=2.8, cy2=2.8):
    # Derivative of sum is sum of derivatives
    tx1, ty1 = grad_a(x, y, 0.0, t1, s1, cx1, cy1)
    tx2, ty2 = grad_a(x, y, 0.0, t2, s2, cx2, cy2)
    return tx1 + tx2, ty1 + ty2

def hessian_c(x, y, t_edge=25.0, t1=40.0, s1=1.5, cx1=1.2, cy1=1.2, t2=40.0, s2=1.5, cx2=2.8, cy2=2.8):
    # Second derivative of sum is sum of second derivatives
    txx1, tyy1, txy1 = hessian_a(x, y, 0.0, t1, s1, cx1, cy1)
    txx2, tyy2, txy2 = hessian_a(x, y, 0.0, t2, s2, cx2, cy2)
    return txx1 + txx2, tyy1 + tyy2, txy1 + txy2

# Simple class to store plate settings
class Plate:
    def __init__(self, model="A"):
        self.L = 4.0
        self.s = 2.0
        self.cx = 2.0
        self.cy = 2.0
        self.t1 = 40.0
        self.s1 = 1.5
        self.cx1 = 1.2
        self.cy1 = 1.2
        self.t2 = 40.0
        self.s2 = 1.5
        self.cx2 = 2.8
        self.cy2 = 2.8
        self.set_model(model)

    def set_model(self, model):
        self.model = model
        if model == "A":
            self.t_edge = 25.0
            self.t0 = 60.0
        elif model == "B":
            self.t_edge = 20.0
            self.t0 = 50.0
        elif model == "C":
            self.t_edge = 25.0

    def get_temp(self, x, y):
        if self.model == "A":
            return temp_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        elif self.model == "B":
            return temp_b(x, y, self.t_edge, self.t0, self.L)
        else:
            return temp_c(x, y, self.t_edge, self.t1, self.s1, self.cx1, self.cy1, self.t2, self.s2, self.cx2, self.cy2)

    def get_grad(self, x, y):
        if self.model == "A":
            return grad_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        elif self.model == "B":
            return grad_b(x, y, self.t_edge, self.t0, self.L)
        else:
            return grad_c(x, y, self.t_edge, self.t1, self.s1, self.cx1, self.cy1, self.t2, self.s2, self.cx2, self.cy2)

    def get_hessian(self, x, y):
        if self.model == "A":
            return hessian_a(x, y, self.t_edge, self.t0, self.s, self.cx, self.cy)
        elif self.model == "B":
            return hessian_b(x, y, self.t_edge, self.t0, self.L)
        else:
            return hessian_c(x, y, self.t_edge, self.t1, self.s1, self.cx1, self.cy1, self.t2, self.s2, self.cx2, self.cy2)
