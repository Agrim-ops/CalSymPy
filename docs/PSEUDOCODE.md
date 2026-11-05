# CalSymPy — Algorithmic Pseudocode
**Project**: CalSymPy (Team 4, Delta-T) — MAT 112 Engineering Mathematics & Python  
**Purpose**: Plain-English algorithmic descriptions of the calculus methods implemented across the codebase.

---

## 1. Building a Thermal Model and Lambdify Cache (models.py)
1. Define continuous spatial coordinates x and y, and parameter variables, as exact mathematical symbols.
2. Formulate the analytical closed-form temperature function T(x, y) symbolically.
3. Differentiate T symbolically with respect to x and y to obtain analytical first partial derivatives Tx and Ty.
4. Differentiate Tx and Ty to compute analytical second partial derivatives Txx, Tyy, and mixed partial Txy.
5. Compile all six symbolic formulas into high-speed numerical array functions using NumPy array backends.
6. Store compiled functions in memory at startup so interactive slider updates require zero repeated differentiation.

---

## 2. Multi-Peak Finding with Newton-Raphson Refinement (features.py)
1. Discretize the plate into a uniform two-dimensional coordinate grid of points.
2. Evaluate temperature at every grid point using the pre-compiled numerical temperature function.
3. Identify all grid locations having temperature within a small tolerance of the maximum grid value.
4. Cluster nearby candidates into distinct physical peaks separated by at least ten percent of the plate width.
5. For each interior candidate, iteratively evaluate the gradient vector and two-by-two Hessian matrix.
6. Compute the inverted Hessian step direction and update coordinates until displacement falls below tolerance.
7. Return the final refined peak coordinates, exact peak temperatures, and boundary flags.

---

## 3. Second Derivative Test (Hessian D-Test) (calculus.py)
1. Check whether first partial derivatives Tx and Ty are both approximately zero to verify a critical point.
2. Evaluate second partial derivatives Txx, Tyy, and mixed second partial derivative Txy at the point.
3. Calculate the Hessian discriminant D by multiplying Txx by Tyy and subtracting the square of Txy.
4. If D is strictly greater than zero and Txx is strictly negative, classify the point as a local maximum peak.
5. If D is strictly greater than zero and Txx is strictly positive, classify the point as a local minimum valley.
6. If D is strictly less than zero, classify the point as a saddle point regardless of the sign of Txx.
7. If D is exactly zero, classify the test as inconclusive, requiring higher-order analysis.

---

## 4. Semiconductor Thermal Risk Classification (risk.py)
1. Accept the peak or point temperature value in degrees Celsius as a numerical input.
2. Round the input temperature to one decimal place to avoid floating-point edge-case jitter.
3. Compare the rounded temperature against the fifty-degree junction safety margin threshold of seventy degrees.
4. If the rounded temperature is strictly below seventy degrees, assign the Low Risk level and green badge.
5. If the temperature is between seventy and ninety degrees inclusive, assign Moderate Risk and yellow badge.
6. If the temperature is strictly above ninety degrees, assign High Risk and red badge.
7. Attach pre-written non-technical plain-English explanations and technical junction margin statements.

---

## 5. Double-Integral Average and Stored Thermal Energy (features.py)
1. Compute the surface area of the square plate by squaring the plate side length.
2. Perform two-dimensional continuous double numerical integration of T(x, y) over the plate using adaptive quadrature.
3. Divide the double integral result by the plate area to obtain the continuous exact average temperature.
4. Compute the arithmetic mean and two-dimensional trapezoidal rule over a discrete grid for comparison.
5. Calculate temperature rise by integrating the difference between T(x, y) and ambient temperature across the plate.
6. Convert the integrated temperature difference from square centimetres to square metres by multiplying by 1e-4.
7. Multiply the integral by material density, specific heat capacity, and plate thickness to compute energy in Joules.

---

## 6. Gradient Descent Heat Source Relocation (features.py)
1. Define the sensitive component fixed position and the initial movable heat source position.
2. Derive the analytical gradient of sensor temperature with respect to the source position coordinates.
3. Compute initial temperature at the sensitive component produced by the current heat source position.
4. For each iteration, evaluate the source coordinate gradient vector using the current source position.
5. Step the source coordinates in the opposite direction of the gradient scaled by a user-selected step size.
6. Restrict the updated source coordinates within allowed mechanical margins inside the plate boundary.
7. Terminate iterations when the Euclidean step size drops below tolerance or maximum iterations are reached.

---

## 7. Lagrange Multipliers for Constrained Rail Extrema (features.py)
1. Express the straight mounting rail as a linear constraint equation ax + by = c.
2. Formulate the Lagrange condition requiring the temperature gradient to be parallel to the rail normal vector.
3. Set the cross-product determinant of the temperature gradient and rail normal to zero: Tx*b - Ty*a = 0.
4. Solve the system composed of the orthogonality equation and the rail constraint simultaneously using SymPy.
5. Retain only real-valued coordinate solutions that lie within the physical boundaries of the plate.
6. Discretize the line segment within the plate into points and compute temperature along the line as a cross-check.
7. Select the valid analytical point yielding the highest temperature as the hottest point on the rail.
