# check_with_sympy.py - verify hand derivatives using sympy
import sympy as sp
import models

# 1. Check Model A at off-axis point (3.0, 2.5)
print("Checking Model A with SymPy...")
x, y = sp.symbols('x y', real=True)
te, t0, s, cx, cy = sp.symbols('te t0 s cx cy', real=True)
T_a = te + t0 * sp.exp(-((x - cx)**2 + (y - cy)**2) / s)
Tx_a = sp.diff(T_a, x)
Ty_a = sp.diff(T_a, y)
Txx_a = sp.diff(Tx_a, x)
Tyy_a = sp.diff(Ty_a, y)
Txy_a = sp.diff(Tx_a, y)
vals_a = {te: 25.0, t0: 60.0, s: 2.0, cx: 2.0, cy: 2.0, x: 3.0, y: 2.5}

assert abs(float(T_a.subs(vals_a).evalf()) - models.temp_a(3.0, 2.5)) < 1e-5, "Model A: T mismatch!"
assert abs(float(Tx_a.subs(vals_a).evalf()) - models.grad_a(3.0, 2.5)[0]) < 1e-5, "Model A: Tx mismatch!"
assert abs(float(Ty_a.subs(vals_a).evalf()) - models.grad_a(3.0, 2.5)[1]) < 1e-5, "Model A: Ty mismatch!"
assert abs(float(Txx_a.subs(vals_a).evalf()) - models.hessian_a(3.0, 2.5)[0]) < 1e-5, "Model A: Txx mismatch!"
assert abs(float(Tyy_a.subs(vals_a).evalf()) - models.hessian_a(3.0, 2.5)[1]) < 1e-5, "Model A: Tyy mismatch!"
assert abs(float(Txy_a.subs(vals_a).evalf()) - models.hessian_a(3.0, 2.5)[2]) < 1e-5, "Model A: Txy mismatch!"
print("Model A at (3.0, 2.5): MATCH")

# 2. Check Model B at off-axis point (1.0, 1.5)
print("\nChecking Model B with SymPy...")
L = sp.symbols('L', real=True)
T_b = te + t0 * sp.sin(sp.pi * x / L) * sp.sin(sp.pi * y / L)
Tx_b = sp.diff(T_b, x)
Ty_b = sp.diff(T_b, y)
Txx_b = sp.diff(Tx_b, x)
Tyy_b = sp.diff(Ty_b, y)
Txy_b = sp.diff(Tx_b, y)
vals_b = {te: 20.0, t0: 50.0, L: 4.0, x: 1.0, y: 1.5}

assert abs(float(T_b.subs(vals_b).evalf()) - models.temp_b(1.0, 1.5)) < 1e-5, "Model B: T mismatch!"
assert abs(float(Tx_b.subs(vals_b).evalf()) - models.grad_b(1.0, 1.5)[0]) < 1e-5, "Model B: Tx mismatch!"
assert abs(float(Ty_b.subs(vals_b).evalf()) - models.grad_b(1.0, 1.5)[1]) < 1e-5, "Model B: Ty mismatch!"
assert abs(float(Txx_b.subs(vals_b).evalf()) - models.hessian_b(1.0, 1.5)[0]) < 1e-5, "Model B: Txx mismatch!"
assert abs(float(Tyy_b.subs(vals_b).evalf()) - models.hessian_b(1.0, 1.5)[1]) < 1e-5, "Model B: Tyy mismatch!"
assert abs(float(Txy_b.subs(vals_b).evalf()) - models.hessian_b(1.0, 1.5)[2]) < 1e-5, "Model B: Txy mismatch!"
print("Model B at (1.0, 1.5): MATCH")
print("\nAll symbolic checks finished successfully!")
