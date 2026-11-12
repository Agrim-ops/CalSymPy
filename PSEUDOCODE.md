# CalSymPy Algorithm Pseudocode

This document outlines the core algorithms and flows in CalSymPy in plain, numbered steps without Python syntax. Each section is limited to a maximum of 12 lines.

---

## 1. Hand-Derived Derivatives (Model A - Gaussian Hotspot)
1. Calculate squared distance from hotspot center: r^2 = (x - cx)^2 + (y - cy)^2.
2. Evaluate exponential decay factor: E = T0 * exp(-r^2 / s).
3. Compute temperature: T = T_edge + E.
4. Apply chain rule for x derivative: Tx = E * (-2 * (x - cx) / s).
5. Apply chain rule for y derivative: Ty = E * (-2 * (y - cy) / s).
6. Apply product rule for second x derivative: Txx = E * [4 * (x - cx)^2 / s^2 - 2 / s].
7. Apply product rule for second y derivative: Tyy = E * [4 * (y - cy)^2 / s^2 - 2 / s].
8. Differentiate Tx with respect to y: Txy = E * [4 * (x - cx) * (y - cy) / s^2].

---

## 2. Hand-Derived Derivatives (Model B - Sine Plate)
1. Normalize coordinates across plate: u = pi * x / L and v = pi * y / L.
2. Compute temperature: T = T_edge + T0 * sin(u) * sin(v).
3. Differentiate with respect to x: Tx = T0 * (pi / L) * cos(u) * sin(v).
4. Differentiate with respect to y: Ty = T0 * (pi / L) * sin(u) * cos(v).
5. Differentiate Tx with respect to x: Txx = -T0 * (pi / L)^2 * sin(u) * sin(v).
6. Differentiate Ty with respect to y: Tyy = -T0 * (pi / L)^2 * sin(u) * sin(v).
7. Differentiate Tx with respect to y: Txy = T0 * (pi / L)^2 * cos(u) * cos(v).

---

## 3. Gradient and D-Test (Second Derivative Test)
1. Calculate first partial derivatives Tx and Ty at coordinates (x, y).
2. Construct gradient vector [Tx, Ty] indicating the direction of steepest increase.
3. Compute gradient magnitude as square root of (Tx^2 + Ty^2).
4. Calculate second partial derivatives Txx, Tyy, and mixed partial Txy.
5. Compute Hessian discriminant D = Txx * Tyy - (Txy)^2.
6. If D is positive and Txx is negative, classify as Local Maximum.
7. If D is positive and Txx is positive, classify as Local Minimum.
8. If D is negative, classify as Saddle Point.
9. If D is zero, classify test as Inconclusive.

---

## 4. Hottest-Point Grid Search
1. Initialize highest recorded temperature to a large negative number.
2. Divide plate length L into N equal intervals with spacing dx = L / N.
3. Outer loop: step coordinate x across grid from 0 to L by dx.
4. Inner loop: step coordinate y across grid from 0 to L by dx.
5. Calculate temperature T at each grid intersection (x, y).
6. If current T is greater than highest recorded temperature:
7. Update highest recorded temperature to T.
8. Record current (x, y) coordinates as the hottest location.
9. Output peak temperature and hottest coordinates after full scan completes.

---

## 5. Midpoint Riemann Sum Average (Double Integral)
1. Choose number of grid intervals N along each axis of the square plate.
2. Calculate interval width dx = L / N and dy = L / N.
3. Calculate area of each small rectangular cell: dA = dx * dy.
4. Initialize accumulated temperature sum to zero.
5. Outer loop: for index i from 0 to N - 1, find midpoint x = (i + 0.5) * dx.
6. Inner loop: for index j from 0 to N - 1, find midpoint y = (j + 0.5) * dy.
7. Evaluate temperature T at midpoint (x, y) and add T * dA to accumulated sum.
8. Compute total plate area as L * L.
9. Divide accumulated sum by total area to get the average plate temperature.

---

## 6. Tangent Plane and Degree-2 Taylor Polynomial
1. Choose expansion base point (a, b) and evaluation point (x, y).
2. Compute displacements from base point: dx = x - a and dy = y - b.
3. Evaluate base temperature T(a, b) and gradient components Tx, Ty at (a, b).
4. Linear tangent plane: compute L(x, y) = T(a, b) + Tx * dx + Ty * dy.
5. Evaluate second partial derivatives Txx, Tyy, and Txy at (a, b).
6. Quadratic curvature term: 0.5 * Txx * dx^2 + Txy * dx * dy + 0.5 * Tyy * dy^2.
7. Degree-2 Taylor polynomial: sum linear tangent plane and quadratic curvature term.

---

## 7. Gradient Descent (Cooling Chip Relocation)
1. Set starting chip location (x, y), learning rate step size, and step limit.
2. Record initial chip location in the trajectory path list.
3. Loop from 1 to step limit:
4. Calculate temperature gradient components Tx and Ty at current position.
5. Update position downhill along negative gradient: x = x - step_size * Tx.
6. Update position downhill along negative gradient: y = y - step_size * Ty.
7. Clamp x and y to remain within safe plate margins between 0.2 and L - 0.2.
8. Append new position (x, y) to trajectory path list.
9. Evaluate final temperature at stopping position and output total cooling achieved.

---

## 8. Risk Level Classification
1. Receive peak plate temperature T in degrees Celsius.
2. If temperature T is strictly less than 70 degrees Celsius:
3. Assign risk classification "Low" (safe operating temperature).
4. If temperature T is between 70 and 90 degrees Celsius inclusive:
5. Assign risk classification "Medium" (elevated thermal stress).
6. If temperature T is strictly greater than 90 degrees Celsius:
7. Assign risk classification "High" (exceeds thermal limit, cooling required).
8. Return assigned risk level.
