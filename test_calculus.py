# test_calculus.py - plain unit checks with assert statements
import models
import calculus

print("Running calculus tests...")

# 1. Test Model A at defaults
plate_a = models.Plate("A")

# Center point (2, 2)
t_center = plate_a.get_temp(2.0, 2.0)
assert abs(t_center - 85.0) < 1e-4, "Model A T(2,2) should be 85"

tx, ty, mag = calculus.gradient(plate_a, 2.0, 2.0)
assert abs(tx) < 1e-4 and abs(ty) < 1e-4, "Model A gradient at (2,2) should be 0"

txx, tyy, txy, d, classification = calculus.second_derivative_test(plate_a, 2.0, 2.0)
assert abs(txx - (-60.0)) < 1e-4, "Txx at (2,2) should be -60"
assert abs(tyy - (-60.0)) < 1e-4, "Tyy at (2,2) should be -60"
assert abs(txy) < 1e-4, "Txy at (2,2) should be 0"
assert abs(d - 3600.0) < 1e-4, "D at (2,2) should be 3600"
assert classification == "Local Maximum", "Classification should be Local Maximum"

# Point (3, 2)
t_32 = plate_a.get_temp(3.0, 2.0)
assert abs(t_32 - 61.39) < 0.01, "Model A T(3,2) should be approximately 61.39"

# 2. Test Model B
plate_b = models.Plate("B")
t_b_center = plate_b.get_temp(2.0, 2.0)
assert abs(t_b_center - 70.0) < 1e-4, "Model B T(2,2) should be 70"

# 3. Test average temperature double integral
avg_t = calculus.average_temperature(plate_a, n_steps=60)
assert 45.0 < avg_t < 48.0, "Model A average temp should be around 46.5"

# 4. Test tangent plane and Taylor polynomial
# Near (2, 2), tangent plane is flat at 85
tan_val = calculus.tangent_plane(plate_a, 2.0, 2.0, 2.05, 2.05)
assert abs(tan_val - 85.0) < 1e-4

# Taylor degree 2 includes curvature
tay_val = calculus.taylor_degree_2(plate_a, 2.0, 2.0, 2.1, 2.1)
actual_val = plate_a.get_temp(2.1, 2.1)
assert abs(tay_val - actual_val) < 0.01, "Taylor degree 2 should closely approximate actual value"

# 5. Test gradient descent moves downhill
path, final_t = calculus.gradient_descent(plate_a, 1.5, 1.5, step_size=0.08, steps=20)
start_t = plate_a.get_temp(1.5, 1.5)
assert final_t < start_t, "Gradient descent must cool down the chip"

# 6. Test grid hottest point finder
hx, hy, ht = calculus.find_hottest_point(plate_a, n_grid=40)
assert abs(hx - 2.0) < 0.15 and abs(hy - 2.0) < 0.15
assert abs(ht - 85.0) < 0.2

# 7. Test risk levels
assert calculus.get_risk_level(50.0) == "Low"
assert calculus.get_risk_level(75.0) == "Medium"
assert calculus.get_risk_level(95.0) == "High"

print("All calculus tests passed successfully!")
