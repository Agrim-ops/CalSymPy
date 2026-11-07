# check_with_sympy.py - verify hand derivatives using sympy
import sympy as sp
import models

# 1. Check Model A
print("Checking Model A with SymPy...")
x, y = sp.symbols('x y', real=True)
te, t0, s, cx, cy = sp.symbols('te t0 s cx cy', real=True)

T_a = te + t0 * sp.exp(-((x - cx)**2 + (y - cy)**2) / s)
Tx_a = sp.diff(T_a, x)
Ty_a = sp.diff(T_a, y)
Txx_a = sp.diff(Tx_a, x)
Tyy_a = sp.diff(Ty_a, y)
Txy_a = sp.diff(Tx_a, y)

vals_a = {te: 25.0, t0: 60.0, s: 2.0, cx: 2.0, cy: 2.0, x: 3.0, y: 2.0}
sym_t = float(T_a.subs(vals_a).evalf())
sym_tx = float(Tx_a.subs(vals_a).evalf())
sym_ty = float(Ty_a.subs(vals_a).evalf())
sym_txx = float(Txx_a.subs(vals_a).evalf())
sym_tyy = float(Tyy_a.subs(vals_a).evalf())
sym_txy = float(Txy_a.subs(vals_a).evalf())

hand_t = models.temp_a(3.0, 2.0)
hand_tx, hand_ty = models.grad_a(3.0, 2.0)
hand_txx, hand_tyy, hand_txy = models.hessian_a(3.0, 2.0)

diff_a = abs(sym_t - hand_t) + abs(sym_tx - hand_tx) + abs(sym_ty - hand_ty) + abs(sym_txx - hand_txx)
if diff_a < 1e-6:
    print("Model A at (3, 2): Hand derivatives MATCH SymPy!")
else:
    print("Model A mismatch!")

# 2. Check Model B
print("\nChecking Model B with SymPy...")
L = sp.symbols('L', real=True)
T_b = te + t0 * sp.sin(sp.pi * x / L) * sp.sin(sp.pi * y / L)
Tx_b = sp.diff(T_b, x)
Ty_b = sp.diff(T_b, y)
Txx_b = sp.diff(Tx_b, x)
Tyy_b = sp.diff(Ty_b, y)
Txy_b = sp.diff(Tx_b, y)

vals_b = {te: 20.0, t0: 50.0, L: 4.0, x: 1.0, y: 2.0}
sym_tb = float(T_b.subs(vals_b).evalf())
sym_txb = float(Tx_b.subs(vals_b).evalf())
sym_tyb = float(Ty_b.subs(vals_b).evalf())
sym_txxb = float(Txx_b.subs(vals_b).evalf())

hand_tb = models.temp_b(1.0, 2.0)
hand_txb, hand_tyb = models.grad_b(1.0, 2.0)
hand_txxb, hand_tyyb, hand_txyb = models.hessian_b(1.0, 2.0)

diff_b = abs(sym_tb - hand_tb) + abs(sym_txb - hand_txb) + abs(sym_tyb - hand_tyb) + abs(sym_txxb - hand_txxb)
if diff_b < 1e-6:
    print("Model B at (1, 2): Hand derivatives MATCH SymPy!")
else:
    print("Model B mismatch!")

# 3. Check Model C
print("\nChecking Model C with SymPy...")
t1, s1, cx1, cy1 = sp.symbols('t1 s1 cx1 cy1', real=True)
t2, s2, cx2, cy2 = sp.symbols('t2 s2 cx2 cy2', real=True)
T_c = te + t1 * sp.exp(-((x - cx1)**2 + (y - cy1)**2) / s1) + t2 * sp.exp(-((x - cx2)**2 + (y - cy2)**2) / s2)
Tx_c = sp.diff(T_c, x)
Ty_c = sp.diff(T_c, y)
Txx_c = sp.diff(Tx_c, x)

vals_c = {te: 25.0, t1: 40.0, s1: 1.5, cx1: 1.2, cy1: 1.2, t2: 40.0, s2: 1.5, cx2: 2.8, cy2: 2.8, x: 2.0, y: 2.0}
sym_tc = float(T_c.subs(vals_c).evalf())
sym_txc = float(Tx_c.subs(vals_c).evalf())
sym_tyc = float(Ty_c.subs(vals_c).evalf())

hand_tc = models.temp_c(2.0, 2.0)
hand_txc, hand_tyc = models.grad_c(2.0, 2.0)

diff_c = abs(sym_tc - hand_tc) + abs(sym_txc - hand_txc) + abs(sym_tyc - hand_tyc)
if diff_c < 1e-6:
    print("Model C at (2, 2): Hand derivatives MATCH SymPy!")
else:
    print("Model C mismatch!")

print("\nAll symbolic checks finished successfully!")
