# CalSymPy — Faculty Viva Questions & Answers (VIVA_QUESTIONS.md)
**Course**: MAT 112 Engineering Mathematics & Python  
**Project**: CalSymPy v2 (Team 4, Delta-T)  
**Scope**: Strictly covers the 4 project files (`models.py`, `calculus.py`, `plots.py`, `main.py`) and `check_with_sympy.py`.

---

### Q1. What does the gradient vector $\nabla T$ represent physically and mathematically?
**Answer**: Mathematically, the gradient is the vector of first partial derivatives $\nabla T = \langle T_x, T_y \rangle$. Physically, it points in the direction of steepest temperature increase, and its magnitude $|\nabla T| = \sqrt{T_x^2 + T_y^2}$ gives the maximum rate of temperature change per centimetre.

### Q2. How did you derive the partial derivatives of Model A by hand?
**Answer**: For $T = T_{\text{edge}} + T_0 \exp(-r^2/s)$ with $r^2 = (x-c_x)^2 + (y-c_y)^2$, we applied the chain rule to the exponential function: $\frac{\partial}{\partial x}\exp(-u) = -\exp(-u)\frac{\partial u}{\partial x}$. Since $\frac{\partial}{\partial x}(r^2/s) = \frac{2(x-c_x)}{s}$, this gives $T_x = T_0 \exp(-r^2/s) \cdot \left(-\frac{2(x-c_x)}{s}\right)$.

### Q3. How did you derive the second partial derivative $T_{xx}$ for Model A?
**Answer**: We applied the product rule to $T_x = f \cdot g$, where $f = T_0 \exp(-r^2/s)$ and $g = -\frac{2(x-c_x)}{s}$. Differentiating each part gives $f_x = f \cdot (-\frac{2(x-c_x)}{s})$ and $g_x = -\frac{2}{s}$. Combining them yields $T_{xx} = f_x g + f g_x = T_0 \exp(-r^2/s) \left[ \frac{4(x-c_x)^2}{s^2} - \frac{2}{s} \right]$.

### Q4. Why is $T_{xy} = T_{yx}$ in your code?
**Answer**: By Clairaut's Theorem, mixed second partial derivatives are equal if the second partial derivatives are continuous. All three plate models are built from smooth exponential, sine, and cosine functions that are infinitely differentiable everywhere on the plate, so $T_{xy}$ and $T_{yx}$ are identical.

### Q5. What is the formula for the Hessian discriminant $D$, and what does it measure?
**Answer**: The discriminant is $D = T_{xx} T_{yy} - (T_{xy})^2$. It measures the Gaussian curvature of the 2D surface at a point, telling us whether the surface curves in the same direction along all slices ($D > 0$) or in opposite directions ($D < 0$).

### Q6. What does $D > 0$ and $T_{xx} < 0$ mean in the second derivative test?
**Answer**: $D > 0$ means the surface curves in the same direction in all vertical slicing planes, and $T_{xx} < 0$ indicates that the surface is concave downward. Together, these conditions prove that the critical point is a local maximum (a peak).

### Q7. What does $D < 0$ mean in the second derivative test?
**Answer**: When $D < 0$, the surface curves upward along one direction and downward along another direction. This forms a mountain pass geometry, meaning the critical point is a saddle point.

### Q8. What happens if $D = 0$?
**Answer**: If $D = 0$, the second derivative test is inconclusive. The quadratic terms vanish or degenerate, so second derivatives alone cannot determine whether the point is an extremum or a saddle.

### Q9. Why does Model A at defaults have $D = 3600$ at $(2, 2)$?
**Answer**: At the center $(2, 2)$, $x = c_x$ and $y = c_y$, so the squared distance $r^2 = 0$ and $\exp(0) = 1$. The formulas give $T_{xx} = 60 \cdot (-2/2) = -60$, $T_{yy} = -60$, and $T_{xy} = 0$. Therefore, $D = (-60) \cdot (-60) - 0^2 = 3600$, confirming $(2, 2)$ is a true maximum.

### Q10. How does your code calculate the average temperature without `scipy.integrate.dblquad`?
**Answer**: We use a two-variable midpoint Riemann sum over the square $[0, L] \times [0, L]$. We divide the plate into a grid of small squares of size $\Delta x \times \Delta y$, sum the temperature at the center of each cell multiplied by cell area $\Delta A$, and divide the total by the plate area $L^2$.

### Q11. Why do you use midpoint evaluation in the double integral Riemann sum?
**Answer**: Evaluating at cell centers $(x_i + \Delta x/2, y_j + \Delta y/2)$ is the midpoint rule, which gives second-order accuracy ($O(\Delta x^2)$). It converges much faster and more symmetrically to the true analytical integral than a simple left-endpoint sum.

### Q12. What is the tangent plane, and how is it used in `calculus.py`?
**Answer**: The tangent plane is the linear approximation of the temperature surface at a base point $(a, b)$, given by $L(x, y) = T(a, b) + T_x(a, b)(x - a) + T_y(a, b)(y - b)$. It approximates temperature values very close to $(a, b)$ using only the local slopes.

### Q13. How does the degree-2 Taylor polynomial improve upon the tangent plane?
**Answer**: The tangent plane is only a flat linear approximation. The degree-2 Taylor polynomial adds quadratic curvature terms: $\frac{1}{2} T_{xx}(x-a)^2 + T_{xy}(x-a)(y-b) + \frac{1}{2} T_{yy}(y-b)^2$, which captures how the surface bends near peaks and valleys.

### Q14. How does gradient descent move the chip away from the hotspot?
**Answer**: The gradient $\nabla T$ points in the direction of greatest temperature increase (toward the heat source). To cool the chip down, gradient descent updates position by stepping in the opposite direction along the negative gradient: $x_{k+1} = x_k - \alpha T_x$ and $y_{k+1} = y_k - \alpha T_y$.

### Q15. Why do you clamp coordinates during gradient descent?
**Answer**: If unconstrained, stepping along the negative gradient could push the chip off the physical edge of the circuit board. Clamping with `min` and `max` keeps the chip inside the physical plate boundaries with a safe margin.

### Q16. How does `find_hottest_point` search the plate?
**Answer**: It uses two nested for-loops across $x$ and $y$ on an evenly spaced grid of points. It compares each point's temperature to a running variable `best_t`, updating `best_x`, `best_y`, and `best_t` whenever a warmer temperature is found.

### Q17. What are your temperature risk thresholds, and where do they come from?
**Answer**: Peak temperatures below $70^\circ\text{C}$ are classified as Low risk, between $70^\circ\text{C}$ and $90^\circ\text{C}$ as Medium risk, and above $90^\circ\text{C}$ as High risk. As noted in the code comment, these thresholds are our own engineering choice informed by commercial silicon limits (chips begin throttling around $95\text{--}105^\circ\text{C}$).

### Q18. What does `check_with_sympy.py` do, and why is SymPy kept separate?
**Answer**: `check_with_sympy.py` defines symbolic formulas with SymPy and calculates symbolic derivatives using `sp.diff`. It evaluates them at sample coordinates to verify that our hand-derived numerical functions in `models.py` have zero algebraic errors, while keeping the main code completely free of SymPy dependencies.

### Q19. Why does Model B have zero gradient at $(2, 2)$?
**Answer**: Model B is $T = 20 + 50 \sin(\pi x / 4) \sin(\pi y / 4)$. At $(2, 2)$, the arguments are $\pi/2$. Since $\cos(\pi/2) = 0$, both $T_x \propto \cos(\pi x/4)$ and $T_y \propto \cos(\pi y/4)$ become exactly zero, confirming $(2, 2)$ is a stationary critical point.

### Q20. What is Model C, and how are its derivatives calculated?
**Answer**: Model C represents two Gaussian microchips on the same plate, modeled as the sum of two exponential bell curves. Because differentiation is a linear operation, its derivatives are simply the sum of the derivatives of each individual Gaussian source.

### Q21. What does the quiver plot in `plots.py` show?
**Answer**: The quiver plot draws directional arrows at a grid of points across the plate. Each arrow points along $\langle T_x, T_y \rangle$, illustrating the vector field of steepest temperature rise toward the hotspots.

### Q22. How is pandas used in `main.py`?
**Answer**: In option 7, pandas creates a structured two-column DataFrame containing key results (`Metric` and `Value`). It allows exporting the summary directly to a clean CSV file using `df.to_csv()`.

### Q23. Why did you not use `lambdify` or lambda functions in this version?
**Answer**: Lambda functions and `sp.lambdify` are advanced Python shortcuts that hide the mathematics inside compiled wrapper objects. Writing the formulas by hand with standard Python functions makes every algebraic step transparent, readable, and directly explainable by a first-year student.

### Q24. What is the single class in your project, and why was it included?
**Answer**: The single class is `Plate` in `models.py`. It serves as a simple data holder for plate parameters (dimensions, edge temperature, hotspot position) and provides convenient helper methods (`get_temp`, `get_grad`, `get_hessian`) to avoid passing a long list of arguments to every function.

### Q25. What are the main physical assumptions and limitations of your project?
**Answer**: The model assumes steady-state heat conduction (no time variable $t$), uniform material properties, and idealized closed-form temperature distributions. Real electronic boards have transient warm-up cycles, complex copper trace layers, and convection cooling that would require time-dependent PDEs.
