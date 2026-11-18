# test_calculus.py - plain unit checks with assert statements
import models
import calculus

print("Running calculus tests...")
# 1. Model A tests
plate_a = models.Plate("A")
assert abs(plate_a.get_temp(2.0, 2.0) - 85.0) < 1e-4, "T(2,2) should be 85"
tx, ty, mag = calculus.gradient(plate_a, 2.0, 2.0)
assert abs(tx) < 1e-4 and abs(ty) < 1e-4, "Gradient at (2,2) should be 0"
txx, tyy, txy, d, classification = calculus.second_derivative_test(plate_a, 2.0, 2.0)
assert abs(txx - (-60.0)) < 1e-4 and abs(tyy - (-60.0)) < 1e-4
assert abs(txy) < 1e-4 and abs(d - 3600.0) < 1e-4 and classification == "Local Maximum"
assert abs(plate_a.get_temp(3.0, 2.0) - 61.39) < 0.01

# 2. Model B tests
plate_b = models.Plate("B")
assert abs(plate_b.get_temp(2.0, 2.0) - 70.0) < 1e-4, "Model B T(2,2) should be 70"

# 3. Double integral average temperature
avg_t = calculus.average_temperature(plate_a, n_steps=60)
assert 45.0 < avg_t < 48.0, "Average temp should be around 46.5"

# 4. Tangent plane and Taylor polynomial
assert abs(calculus.tangent_plane(plate_a, 2.0, 2.0, 2.05, 2.05) - 85.0) < 1e-4
t_base = plate_a.get_temp(3.0, 2.0)
tx_base, ty_base = plate_a.get_grad(3.0, 2.0)
expected_tan = t_base + tx_base * 0.05
assert abs(calculus.tangent_plane(plate_a, 3.0, 2.0, 3.05, 2.0) - expected_tan) < 1e-5
tay_val = calculus.taylor_degree_2(plate_a, 2.0, 2.0, 2.1, 2.1)
assert abs(tay_val - plate_a.get_temp(2.1, 2.1)) < 0.01

# 5. Gradient descent downhill cooling
path, final_t = calculus.gradient_descent(plate_a, 1.5, 1.5)
assert final_t < plate_a.get_temp(1.5, 1.5)
step1_dist = ((path[1][0] - path[0][0]) ** 2 + (path[1][1] - path[0][1]) ** 2) ** 0.5
assert step1_dist < 0.15, "First step should move less than 0.15 cm"

# 6. Grid hottest point and risk level
hx, hy, ht = calculus.find_hottest_point(plate_a, n_grid=40)
assert abs(hx - 2.0) < 0.15 and abs(hy - 2.0) < 0.15 and abs(ht - 85.0) < 0.2
assert calculus.get_risk_level(50.0) == "Low" and calculus.get_risk_level(75.0) == "Medium" and calculus.get_risk_level(95.0) == "High"

# 7. Cooling suggestions
tips_low = " ".join(calculus.cooling_suggestions(50.0)).lower()
assert "no action" in tips_low
tips_med = " ".join(calculus.cooling_suggestions(85.0))
assert "15.1" in tips_med
tips_high = " ".join(calculus.cooling_suggestions(100.0)).lower()
assert "heat sink or fan" in tips_high

# 8. Best placement search
best_15 = calculus.find_best_placement(plate_a, 1.5, 1.5)
assert best_15 is not None and best_15[2] < 70.0 and best_15[3] > 0.0
best_03 = calculus.find_best_placement(plate_a, 0.3, 0.3)
assert best_03 is not None and abs(best_03[3]) < 1e-5
assert calculus.find_best_placement(plate_a, 1.5, 1.5, limit=10.0) is None

print("All calculus tests passed successfully!")
