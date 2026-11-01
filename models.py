# ==============================================================================
# CalSymPy (Team 4, Delta-T) — models.py
#
# Plain-English Summary:
# This module defines the mathematical models for temperature distribution T(x, y)
# across a flat square plate (side length L = 4 cm). In our MAT 112 Engineering
# Mathematics course, temperature is modeled as a scalar field that depends only
# on physical coordinates (x, y) — steady-state conditions with no time dependence.
#
# To achieve high performance without re-doing symbolic math during interactive use,
# this module computes all symbolic derivatives (partial derivatives and Hessian matrix)
# once using SymPy, and compiles ("lambdifies") them into fast NumPy numerical
# functions. When users adjust parameter sliders, the code calls these pre-compiled
# functions directly, avoiding repeated symbolic differentiation.
# ==============================================================================

import numpy as np
import sympy as sp


def _ensure_array(val, shape_reference):
    """
    Ensure the returned value has the same shape as the input coordinate array.
    
    Calculus context:
    Some derivatives evaluate to a constant (for example, a cross derivative T_xy
    that is identically zero). When evaluated on a grid of points, SymPy's
    lambdified function may return a single number (e.g. 0.0). This helper
    broadcasts that constant across the full coordinate grid so every point has
    its corresponding derivative value.
    """
    if isinstance(val, (int, float, np.number)):
        if isinstance(shape_reference, np.ndarray):
            return np.full_like(shape_reference, float(val), dtype=float)
        return float(val)
    return np.asarray(val, dtype=float)


class ThermalModel:
    """
    Represents an analytical 2D steady-state temperature distribution T(x, y).
    
    Stores the mathematical definition, default parameter values, symbolic
    expressions, and cached numerical functions for temperature, gradient,
    and second derivatives (Hessian).
    """

    def __init__(self, model_id, name, description, formula_latex, param_keys, default_params, build_expr_fn):
        """
        Initialize the thermal model and pre-compile its calculus functions.
        
        Parameters:
            model_id (str): Short identifier (e.g. 'A', 'B', 'C', 'C2', 'D').
            name (str): Human-readable model title.
            description (str): Plain-English physical description for students.
            formula_latex (str): LaTeX representation of the formula.
            param_keys (list): List of parameter names in fixed order.
            default_params (dict): Default parameter values.
            build_expr_fn (callable): Function returning the symbolic SymPy expression T(x, y, ...).
        """
        self.model_id = model_id
        self.name = name
        self.description = description
        self.formula_latex = formula_latex
        self.param_keys = param_keys
        self.default_params = default_params.copy()

        # Define independent spatial variables (x, y)
        self.x_sym, self.y_sym = sp.symbols('x y', real=True)

        # Define symbolic parameter variables
        self.param_symbols = [sp.symbols(k, real=True) for k in self.param_keys]

        # Build the symbolic temperature formula T(x, y)
        self.T_sym = build_expr_fn(self.x_sym, self.y_sym, *self.param_symbols)

        # Calculus Step 1: Compute first-order partial derivatives (gradient components)
        # Tx = ∂T/∂x: rate of temperature change moving in the x-direction
        # Ty = ∂T/∂y: rate of temperature change moving in the y-direction
        self.Tx_sym = sp.diff(self.T_sym, self.x_sym)
        self.Ty_sym = sp.diff(self.T_sym, self.y_sym)

        # Calculus Step 2: Compute second-order partial derivatives (Hessian components)
        # Txx = ∂²T/∂x²: concavity in the x-direction
        # Tyy = ∂²T/∂y²: concavity in the y-direction
        # Txy = ∂²T/∂x∂y: mixed concavity (by Clairaut's theorem, Txy = Tyx for smooth functions)
        self.Txx_sym = sp.diff(self.Tx_sym, self.x_sym)
        self.Tyy_sym = sp.diff(self.Ty_sym, self.y_sym)
        self.Txy_sym = sp.diff(self.Tx_sym, self.y_sym)

        # Calculus Step 3: Compile into fast numerical NumPy functions
        # This caching ensures zero symbolic differentiation during interactive slider moves.
        arg_symbols = (self.x_sym, self.y_sym, *self.param_symbols)
        self._fn_T = sp.lambdify(arg_symbols, self.T_sym, modules='numpy')
        self._fn_Tx = sp.lambdify(arg_symbols, self.Tx_sym, modules='numpy')
        self._fn_Ty = sp.lambdify(arg_symbols, self.Ty_sym, modules='numpy')
        self._fn_Txx = sp.lambdify(arg_symbols, self.Txx_sym, modules='numpy')
        self._fn_Tyy = sp.lambdify(arg_symbols, self.Tyy_sym, modules='numpy')
        self._fn_Txy = sp.lambdify(arg_symbols, self.Txy_sym, modules='numpy')

    def _extract_param_tuple(self, params):
        """Extract parameters in the exact order expected by the compiled functions."""
        merged = self.default_params.copy()
        if params:
            merged.update(params)
        return tuple(merged[k] for k in self.param_keys)

    def evaluate_T(self, x, y, params=None):
        """
        Evaluate temperature T at position (x, y).
        
        Calculus interpretation:
        Evaluates the scalar temperature field T(x, y) in degrees Celsius.
        Works for both scalar points and 2D coordinate grid arrays.
        """
        p_vals = self._extract_param_tuple(params)
        raw = self._fn_T(x, y, *p_vals)
        return _ensure_array(raw, x)

    def evaluate_gradient(self, x, y, params=None):
        """
        Evaluate gradient vector ∇T = <Tx, Ty> at position (x, y).
        
        Calculus interpretation:
        The gradient points in the direction of greatest temperature increase.
        Its magnitude |∇T| represents the maximum rate of temperature increase per cm.
        Heat flux flows along -∇T (from hot to cold).
        """
        p_vals = self._extract_param_tuple(params)
        raw_tx = self._fn_Tx(x, y, *p_vals)
        raw_ty = self._fn_Ty(x, y, *p_vals)
        return _ensure_array(raw_tx, x), _ensure_array(raw_ty, x)

    def evaluate_hessian(self, x, y, params=None):
        """
        Evaluate second partial derivatives (Txx, Tyy, Txy) at position (x, y).
        
        Calculus interpretation:
        These second derivatives describe the local curvature of the temperature surface.
        They are used in the second derivative test to classify peaks, valleys, and saddle points:
        Discriminant D = Txx * Tyy - (Txy)².
        """
        p_vals = self._extract_param_tuple(params)
        raw_txx = self._fn_Txx(x, y, *p_vals)
        raw_tyy = self._fn_Tyy(x, y, *p_vals)
        raw_txy = self._fn_Txy(x, y, *p_vals)
        return _ensure_array(raw_txx, x), _ensure_array(raw_tyy, x), _ensure_array(raw_txy, x)


# ==============================================================================
# Model Definitions
# ==============================================================================

def _build_model_A(x, y, T_edge, T0, s, cx, cy, L):
    """
    Model A: Single Hotspot (Gaussian heat source).
    T(x, y) = T_edge + T0 * exp(-((x - cx)² + (y - cy)²) / s)
    """
    r_squared = (x - cx)**2 + (y - cy)**2
    return T_edge + T0 * sp.exp(-r_squared / s)


def _build_model_B(x, y, T_edge, T0, L):
    """
    Model B: Fixed Cold Edges (Fourier fundamental mode).
    T(x, y) = T_edge + T0 * sin(pi * x / L) * sin(pi * y / L)
    """
    return T_edge + T0 * sp.sin(sp.pi * x / L) * sp.sin(sp.pi * y / L)


def _build_model_C(x, y, T_edge, T0, L):
    """
    Model C: Sealed Edges (Smooth zero normal flux on boundaries).
    T(x, y) = T_edge + T0 * sin²(pi * x / L) * sin²(pi * y / L)
    """
    return T_edge + T0 * (sp.sin(sp.pi * x / L)**2) * (sp.sin(sp.pi * y / L)**2)


def _build_model_C2(x, y, T_edge, T0, L):
    """
    Model C2: True Insulated Edges (Neumann boundary condition ∂T/∂n = 0).
    T(x, y) = T_edge + T0 * cos(pi * x / L) * cos(pi * y / L)
    """
    return T_edge + T0 * sp.cos(sp.pi * x / L) * sp.cos(sp.pi * y / L)


def _build_model_D(x, y, T_edge, T1, s1, cx1, cy1, T2, s2, cx2, cy2, L):
    """
    Model D: Two Hotspots (Dual localized Gaussian heat sources).
    T(x, y) = T_edge + T1 * exp(-((x-cx1)²+(y-cy1)²)/s1) + T2 * exp(-((x-cx2)²+(y-cy2)²)/s2)
    """
    r1_sq = (x - cx1)**2 + (y - cy1)**2
    r2_sq = (x - cx2)**2 + (y - cy2)**2
    return T_edge + T1 * sp.exp(-r1_sq / s1) + T2 * sp.exp(-r2_sq / s2)


# Registry of all available models (pre-compiled once at startup)
MODELS = {
    'A': ThermalModel(
        model_id='A',
        name='Model A (Single Hotspot)',
        description='A single localized Gaussian heat source centered on the plate.',
        formula_latex=r'T(x, y) = T_{\text{edge}} + T_0 \exp\left(-\frac{(x - c_x)^2 + (y - c_y)^2}{s}\right)',
        param_keys=['T_edge', 'T0', 's', 'cx', 'cy', 'L'],
        default_params={'T_edge': 25.0, 'T0': 60.0, 's': 2.0, 'cx': 2.0, 'cy': 2.0, 'L': 4.0},
        build_expr_fn=_build_model_A,
    ),
    'B': ThermalModel(
        model_id='B',
        name='Model B (Fixed Cold Edges)',
        description='Heat distribution with edges fixed at constant baseline temperature.',
        formula_latex=r'T(x, y) = T_{\text{edge}} + T_0 \sin\left(\frac{\pi x}{L}\right) \sin\left(\frac{\pi y}{L}\right)',
        param_keys=['T_edge', 'T0', 'L'],
        default_params={'T_edge': 20.0, 'T0': 50.0, 'L': 4.0},
        build_expr_fn=_build_model_B,
    ),
    'C': ThermalModel(
        model_id='C',
        name='Model C (Sealed Edges)',
        description='Sealed boundary condition where normal derivatives smoothly vanish at the edges.',
        formula_latex=r'T(x, y) = T_{\text{edge}} + T_0 \sin^2\left(\frac{\pi x}{L}\right) \sin^2\left(\frac{\pi y}{L}\right)',
        param_keys=['T_edge', 'T0', 'L'],
        default_params={'T_edge': 40.0, 'T0': 30.0, 'L': 4.0},
        build_expr_fn=_build_model_C,
    ),
    'C2': ThermalModel(
        model_id='C2',
        name='Model C2 (True Insulated Edges)',
        description='Insulated boundary condition with zero normal temperature gradient at all boundaries.',
        formula_latex=r'T(x, y) = T_{\text{edge}} + T_0 \cos\left(\frac{\pi x}{L}\right) \cos\left(\frac{\pi y}{L}\right)',
        param_keys=['T_edge', 'T0', 'L'],
        default_params={'T_edge': 40.0, 'T0': 30.0, 'L': 4.0},
        build_expr_fn=_build_model_C2,
    ),
    'D': ThermalModel(
        model_id='D',
        name='Model D (Two Hotspots)',
        description='Dual localized heat sources representing two nearby microchips.',
        formula_latex=r'T(x, y) = T_{\text{edge}} + T_1 e^{-\frac{(x-c_{x1})^2+(y-c_{y1})^2}{s_1}} + T_2 e^{-\frac{(x-c_{x2})^2+(y-c_{y2})^2}{s_2}}',
        param_keys=['T_edge', 'T1', 's1', 'cx1', 'cy1', 'T2', 's2', 'cx2', 'cy2', 'L'],
        default_params={
            'T_edge': 25.0,
            'T1': 45.0,
            's1': 1.5,
            'cx1': 1.2,
            'cy1': 1.2,
            'T2': 45.0,
            's2': 1.5,
            'cx2': 2.8,
            'cy2': 2.8,
            'L': 4.0,
        },
        build_expr_fn=_build_model_D,
    ),
}


def get_model(model_id):
    """Retrieve a pre-compiled thermal model by its letter ID ('A', 'B', 'C', 'C2', 'D')."""
    if model_id not in MODELS:
        raise ValueError(f"Unknown model ID '{model_id}'. Available: {list(MODELS.keys())}")
    return MODELS[model_id]
