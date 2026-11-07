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
sym_ta = float(T_a.subs(vals_a).evalf())
sym_txa = float(Tx_a.subs(vals_a).evalf())
sym_tya = float(Ty_a.subs(vals_a).evalf())
sym_txxa = float(Txx_a.subs(vals_a).evalf())
sym_tyya = float(Tyy_a.subs(vals_a).evalf())
sym_txya = float(Txy_a.subs(vals_a).evalf())

hand_ta = models.temp_a(3.0, 2.5)
hand_txa, hand_tya = models.grad_a(3.0, 2.5)
hand_txxa, hand_tyya, hand_txya = models.hessian_a(3.0, 2.5)

assert abs(sym_ta - hand_ta) < 1e-5, "Model A: T mismatch!"
assert abs(sym_txa - hand_txa) < 1e-5, "Model A: Tx mismatch!"
assert abs(sym_tya - hand_tya) < 1e-5, "Model A: Ty mismatch!"
assert abs(sym_txxa - hand_txxa) < 1e-5, "Model A: Txx mismatch!"
assert abs(sym_tyya - hand_tyya) < 1e-5, "Model A: Tyy mismatch!"
assert abs(sym_txya - hand_txya) < 1e-5, "Model A: Txy mismatch!"
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
sym_tb = float(T_b.subs(vals_b).evalf())
sym_txb = float(Tx_b.subs(vals_b).evalf())
sym_tyb = float(Ty_b.subs(vals_b).evalf())
sym_txxb = float(Txx_b.subs(vals_b).evalf())
sym_tyyb = float(Tyy_b.subs(vals_b).evalf())
sym_txyb = float(Txy_b.subs(vals_b).evalf())

hand_tb = models.temp_b(1.0, 1.5)
hand_txb, hand_tyb = models.grad_b(1.0, 1.5)
hand_txxb, hand_tyyb, hand_txyb = models.hessian_b(1.0, 1.5)

assert abs(sym_tb - hand_tb) < 1e-5, "Model B: T mismatch!"
assert abs(sym_txb - hand_txb) < 1e-5, "Model B: Tx mismatch!"
assert abs(sym_tyb - hand_tyb) < 1e-5, "Model B: Ty mismatch!"
assert abs(sym_txxb - hand_txxb) < 1e-5, "Model B: Txx mismatch!"
assert abs(sym_tyyb - hand_tyyb) < 1e-5, "Model B: Tyy mismatch!"
assert abs(sym_txyb - hand_txyb) < 1e-5, "Model B: Txy mismatch!"
print("Model B at (1.0, 1.5): MATCH")

# 3. Check Model C at off-axis point (2.0, 1.5)
print("\nChecking Model C with SymPy...")
t1, s1, cx1, cy1 = sp.symbols('t1 s1 cx1 cy1', real=True)
t2, s2, cx2, cy2 = sp.symbols('t2 s2 cx2 cy2', real=True)
T_c = te + t1 * sp.exp(-((x - cx1)**2 + (y - cy1)**2) / s1) + t2 * sp.exp(-((x - cx2)**2 + (y - cy2)**2) / s2)
Tx_c = sp.diff(T_c, x)
Ty_c = sp.diff(T_c, y)
Txx_c = sp.diff(Tx_c, x)
Tyy_c = sp.diff(Ty_c, y)
Txy_c = sp.diff(Tx_c, y)

vals_c = {te: 25.0, t1: 40.0, s1: 1.5, cx1: 1.2, cy1: 1.2, t2: 40.0, s2: 1.5, cx2: 2.8, cy2: 2.8, x: 2.0, y: 1.5}
sym_tc = float(T_c.subs(vals_c).evalf())
sym_txc = float(Tx_c.subs(vals_c).evalf())
sym_tyc = float(Ty_c.subs(vals_c).evalf())
sym_txxc = float(Txx_c.subs(vals_c).evalf())
sym_tyyc = float(Tyy_c.subs(vals_c).evalf())
sym_txyc = float(Txy_c.subs(vals_c).evalf())

hand_tc = models.temp_c(2.0, 1.5)
hand_txc, hand_tyc = models.grad_c(2.0, 1.5)
hand_txxc, hand_tyyc, hand_txyc = models.hessian_c(2.0, 1.5)

assert abs(sym_tc - hand_tc) < 1e-5, "Model C: T mismatch!"
assert abs(sym_txc - hand_txc) < 1e-5, "Model C: Tx mismatch!"
assert abs(sym_tyc - hand_tyc) < 1e-5, "Model C: Ty mismatch!"
assert abs(sym_txxc - hand_txxc) < 1e-5, "Model C: Txx mismatch!"
assert abs(sym_tyyc - hand_tyyc) < 1e-5, "Model C: Tyy mismatch!"
assert abs(sym_txyc - hand_txyc) < 1e-5, "Model C: Txy mismatch!"
print("Model C at (2.0, 1.5): MATCH")

print("\nAll symbolic checks finished successfully!")
