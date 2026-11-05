# CalSymPy — MAT 112 Faculty Viva & Oral Examination Q&A Guide (VIVA_QA.md)
**Project**: CalSymPy (Team 4, Delta-T) — First-Year MAT 112 Engineering Mathematics & Python  
**Target Audience**: Students preparing for oral viva defense and faculty examination.  
**Style**: Exactly 2 to 3 concise, rigorous sentences per answer based strictly on the CalSymPy codebase.

---

### Section 1: Gradients, Directional Derivatives & Fourier's Law

#### Q1. Why does the gradient vector $\nabla T$ point in the direction of steepest temperature increase?
The directional derivative is given by $D_{\mathbf{u}} T = \nabla T \cdot \mathbf{u} = |\nabla T| \cos\theta$, where $\mathbf{u}$ is a unit vector. This dot product is maximized when $\cos\theta = 1$ ($\theta = 0$), meaning $\mathbf{u}$ is aligned directly with $\nabla T$. Therefore, $\nabla T$ points in the direction of maximum spatial rate of temperature increase, with magnitude $|\nabla T|$ representing that maximum rate.

#### Q2. Why is Fourier's Law of heat conduction written as $\mathbf{F} = -k \nabla T$ with a negative sign?
Heat naturally flows down the temperature gradient from hotter regions toward colder regions according to the Second Law of Thermodynamics. Because $\nabla T$ points in the direction of greatest temperature increase, the negative sign ensures that the heat flux vector field $\mathbf{F}$ points in the opposite direction toward lower temperatures. The scalar $k$ represents thermal conductivity in $\text{W/(m}\cdot\text{K)}$.

#### Q3. What physical units does CalSymPy use for gradient and heat flux, and how are they made consistent?
Coordinates $x$ and $y$ are in centimetres, so the raw gradient components $T_x$ and $T_y$ have units of $^\circ\text{C/cm}$. In `features.py` and `plots.py`, the gradient is multiplied by $100\,\text{cm/m}$ to obtain $^\circ\text{C/m}$ before multiplying by thermal conductivity $k$ in $\text{W/(m}\cdot\text{K)}$. This produces a heat flux magnitude in standard SI units of $\text{W/m}^2$.

#### Q4. What is the physical significance of the streamlines plotted in Tab 8?
Streamlines are continuous field curves that are tangent to the heat flux vector field $\mathbf{F} = -k\nabla T$ at every point across the plate. In steady state, they trace the continuous trajectories along which thermal energy conducts away from the hot microchips toward the cooled plate boundaries. Closely spaced streamlines indicate regions of high heat flux density.

#### Q5. What is the gradient value along the boundary edges of Model C, and why?
The edge gradient in Model C is zero because the boundary conditions are insulated ($\partial T/\partial n = 0$ on all four edges). As evaluated in `features.py` and verified in `selftest.py`, both $T_x$ and $T_y$ vanish along $x = 0, L$ and $y = 0, L$. This represents an ideal thermal boundary where no heat crosses the edge.

---

### Section 2: The Second Derivative Test & Critical Point Classification

#### Q6. What is the definition and geometric meaning of the Hessian discriminant $D$?
The discriminant is the determinant of the $2 \times 2$ Hessian matrix of second partial derivatives: $D = T_{xx} T_{yy} - (T_{xy})^2$. Geometrically, $D$ measures the Gaussian curvature of the two-dimensional temperature surface at a critical point. A positive $D$ indicates the surface curves in the same direction in all vertical slicing planes, while a negative $D$ indicates opposite curvatures.

#### Q7. What are the four possible outcomes of the Second Derivative Test in `calculus.py`?
If $D > 0$ and $T_{xx} < 0$, the point is concave down in all directions and is classified as a local maximum (peak). If $D > 0$ and $T_{xx} > 0$, the surface is concave up in all directions, representing a local minimum (valley). If $D < 0$, the surface bends up along one axis and down along another, forming a saddle point, while $D = 0$ is inconclusive.

#### Q8. Why does a negative discriminant ($D < 0$) guarantee a saddle point regardless of the sign of $T_{xx}$?
When $D = T_{xx} T_{yy} - (T_{xy})^2 < 0$, the product $T_{xx} T_{yy}$ must be smaller than $(T_{xy})^2$, meaning the eigenvalues of the Hessian matrix have opposite signs (one positive, one negative). This proves the surface possesses positive curvature along one principal direction and negative curvature along the perpendicular principal direction. Consequently, the point cannot be an extremum and must be a saddle.

#### Q9. Why does Clairaut's Theorem hold for all models implemented in CalSymPy?
Clairaut's Theorem states that mixed second partial derivatives are equal ($T_{xy} = T_{yx}$) if the second partial derivatives are continuous on an open domain. Because all five models in `models.py` are composed of smooth, infinitely differentiable elementary functions (exponentials, sines, and cosines), their derivatives are continuous everywhere. This allows `calculus.py` to evaluate only a single mixed derivative $T_{xy}$.

#### Q10. What does the Second Derivative Test conclude when $D = 0$, and how does CalSymPy handle it?
When $D = 0$, the test is inconclusive because second-order terms vanish or degenerate, leaving the local geometry indeterminate at order two. In `calculus.py`, the function `classify_critical_point` returns an explicit `"Inconclusive (D = 0)"` status rather than guessing. Determining whether such a point is an extremum would require inspecting higher-order Taylor expansion terms.

---

### Section 3: Mathematical Derivations & Analytical Specifics

#### Q11. Show the mathematical derivation of why $T_{xx} = -2T_0 / s$ at the peak of the Gaussian Model A.
Model A is $T(x,y) = T_{\text{edge}} + T_0 \exp(-r^2/s)$ where $r^2 = (x-c_x)^2 + (y-c_y)^2$. Differentiating gives $T_x = T_0 \exp(-r^2/s) \cdot (-2(x-c_x)/s)$, and a second derivative yields $T_{xx} = T_0 \exp(-r^2/s) \left[ \frac{4(x-c_x)^2}{s^2} - \frac{2}{s} \right]$. At the hotspot peak $x = c_x$ and $y = c_y$, the first term inside brackets vanishes and the exponential equals $1$, leaving exactly $T_{xx} = -2T_0 / s$.

#### Q12. Why does Model C2 exhibit a saddle point at the exact plate centre $(2, 2)$?
Model C2 is given by $T(x,y) = T_{\text{edge}} + T_0 \cos(\pi x / L) \cos(\pi y / L)$. At the centre $(2, 2)$ with $L=4$, the arguments are $\pi/2$, so the cosines equal $0$ while their derivatives equal $-1$. Evaluating the Hessian yields $T_{xx} = T_{yy} = 0$ and $T_{xy} = T_0 (\pi/L)^2 \approx 18.51$, giving $D = 0 \cdot 0 - (18.51)^2 = -342.4 < 0$, which proves the centre is an analytical saddle point.

#### Q13. Why does Model D have two equal maxima and an interior saddle point?
Model D models two identical microchip sources located symmetrically across the diagonal at $(1.2, 1.2)$ and $(2.8, 2.8)$ with equal amplitudes ($T_1 = T_2 = 45\,^\circ\text{C}$). The interaction of their decaying tails creates two symmetric local temperature peaks near $(1.267, 1.267)$ and $(2.733, 2.733)$ where $D > 0$ and $T_{xx} < 0$. Between them at the geometric centre $(2, 2)$, their thermal slopes cross to create a stationary saddle point where $T = 63.34\,^\circ\text{C}$ and $D = -1846.6 < 0$.

#### Q14. How does the 2D Newton-Raphson refinement in `features.py` locate exact peaks?
The routine treats peak finding as solving the nonlinear vector system $\nabla T(x, y) = \mathbf{0}$. From a coarse grid candidate, each iteration updates coordinates via $\mathbf{x}_{k+1} = \mathbf{x}_k - \mathbf{H}^{-1} \nabla T$, where $\mathbf{H}$ is the evaluated $2 \times 2$ Hessian matrix. This yields quadratic local convergence to the exact analytical stationary point within five iterations, independent of grid resolution.

#### Q15. Why does Model C2 have two tied global maxima at $(0,0)$ and $(4,4)$ instead of the centre?
In Model C2, the product of cosines $\cos(\pi x / 4) \cos(\pi y / 4)$ equals $+1$ when both coordinates are simultaneously $0$ or simultaneously $4$ ($\cos(0)\cos(0) = 1$ and $\cos(\pi)\cos(\pi) = 1$). Both opposite corners reach the maximum temperature of $T_{\text{edge}} + T_0 = 70.0\,^\circ\text{C}$. The clustering algorithm in `features.py` detects this spatial separation and classifies the plate as a tied multi-peak configuration.

---

### Section 4: Vector Divergence & Heat Flux Physics

#### Q16. Why is the divergence of the heat flux vector field equal to $-k \nabla^2 T$?
By Fourier's Law, the heat flux vector field is $\mathbf{F} = -k \nabla T = \langle -k T_x, -k T_y \rangle$. The divergence operator is the sum of spatial derivatives: $\operatorname{div} \mathbf{F} = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} = -k \frac{\partial^2 T}{\partial x^2} - k \frac{\partial^2 T}{\partial y^2} = -k (T_{xx} + T_{yy})$. Because the Laplacian is $\nabla^2 T = T_{xx} + T_{yy}$, this simplifies directly to $\operatorname{div} \mathbf{F} = -k \nabla^2 T$.

#### Q17. What is the physical meaning of positive versus negative divergence in Tab 8?
Divergence measures the net flux expanding outward per unit volume from an infinitesimal region. Where $\operatorname{div} \mathbf{F} > 0$ (at a hotspot where $\nabla^2 T < 0$), heat is generated and diverges outward, identifying the location of an active thermal source. Where $\operatorname{div} \mathbf{F} < 0$ (where $\nabla^2 T > 0$), heat is converging inward, identifying a thermal sink or cooling zone.

#### Q18. Why must the Laplacian be multiplied by $10,000$ when calculating divergence in $\text{W/m}^3$?
Plate coordinates $x$ and $y$ are measured in centimetres, which means second derivatives $T_{xx}$ and $T_{yy}$ have units of $^\circ\text{C/cm}^2$. Converting to standard SI units requires scaling by $(100\,\text{cm/m})^2 = 10,000\,\text{cm}^2/\text{m}^2$. Multiplying by thermal conductivity $k$ in $\text{W/(m}\cdot\text{K)}$ then produces the correct volumetric power density in $\text{W/m}^3$.

#### Q19. Does a steady-state temperature field without internal sources have zero divergence?
Yes, in a passive solid domain with no internal heat generation, steady-state conservation of energy requires $\operatorname{div} \mathbf{F} = 0$, which reduces to Laplace's equation $\nabla^2 T = 0$. In CalSymPy, the models represent plates with active, localized microchip heat dissipation, which is why $\nabla^2 T \neq 0$ and the divergence map highlights source regions.

#### Q20. Why does the divergence colorbar use a symmetric diverging colormap (`bwr`)?
A diverging blue-white-red colormap (`bwr`) places zero divergence at neutral white in the center of the color scale. Positive divergence values (sources) appear in vivid red, while negative values (sinks) appear in deep blue. Symmetrizing the scale between $-M$ and $+M$ prevents visual bias toward either sources or sinks.

---

### Section 5: Double Integration & Stored Thermal Energy

#### Q21. How is the continuous exact average temperature defined and calculated in `features.py`?
The exact average temperature is defined by the continuous double integral $T_{\text{avg}} = \frac{1}{\text{Area}} \iint_R T(x, y)\,dA = \frac{1}{L^2} \int_0^L \int_0^L T(x, y)\,dy\,dx$. In `features.py`, this integral is evaluated numerically using `scipy.integrate.dblquad` with strict relative tolerance ($10^{-4}$). Dividing the total integrated temperature by the surface area $L^2$ yields the exact continuous average in degrees Celsius.

#### Q22. Why does the discrete plain-grid mean differ from the exact double-integral average?
The plain arithmetic mean weights every sample point equally as a full grid cell. However, points along the 4 outer edges only represent half cells, and the 4 corner points represent quarter cells. Because boundary edges are cooler in Models A and B, the plain mean overcounts cold edge samples, resulting in a lower estimate than the true continuous integral.

#### Q23. Why does the trapezoid-rule average (`np.trapezoid`) agree much more closely with the double integral?
The two-dimensional trapezoidal rule correctly assigns boundary edges a weight of one-half and plate corners a weight of one-quarter. This geometric weighting accurately mirrors the continuous domain discretization used in formal calculus quadrature. As verified in `test_feature6_integral.py`, the trapezoid average closely matches the `scipy.integrate.dblquad` continuous result.

#### Q24. How is stored thermal energy computed from the double integral, and what are its units?
Stored thermal energy is calculated as $E = \rho \, c_p \, \tau \iint_R [T(x, y) - T_{\text{ambient}}]\,dA$, where $\rho$ is density in $\text{kg/m}^3$, $c_p$ is specific heat in $\text{J/(kg}\cdot\text{K)}$, and $\tau$ is thickness in metres. The spatial integral in $\text{cm}^2\cdot^\circ\text{C}$ is converted to $\text{m}^2\cdot\text{K}$ by multiplying by $10^{-4}\,\text{m}^2/\text{cm}^2$. The resulting product has units $[\text{kg/m}^3] \cdot [\text{J/(kg}\cdot\text{K)}] \cdot [\text{m}] \cdot [\text{m}^2\cdot\text{K}] = \text{Joules (J)}$.

#### Q25. Why is the specific heat capacity $c_p$ marked as approximate for FR-4 but exact for Copper?
Copper is a pure metallic element with a well-established, standardized specific heat capacity of $385.0\,\text{J/(kg}\cdot\text{K)}$. In contrast, FR-4 is an anisotropic woven fiberglass and epoxy composite whose exact heat capacity varies between $1000$ and $1200\,\text{J/(kg}\cdot\text{K)}$ depending on resin content and weave density. CalSymPy adopts the industry midpoint $1100\,\text{J/(kg}\cdot\text{K)}$ and explicitly flags it as an engineering approximation.

---

### Section 6: Optimization — Gradient Descent & Lagrange Multipliers

#### Q26. How does gradient descent relocate the heat source to cool the sensitive sensor?
The sensor temperature $T_s(\mathbf{c})$ depends on the heat source position $\mathbf{c} = \langle c_x, c_y \rangle$. The algorithm computes the spatial gradient of sensor temperature with respect to source coordinates, $\nabla_{\mathbf{c}} T_s$. It then iteratively updates source position along the negative gradient direction: $\mathbf{c}_{k+1} = \mathbf{c}_k - \alpha \nabla_{\mathbf{c}} T_s$, effectively pushing the heat source away from the sensor.

#### Q27. What mathematical condition does the method of Lagrange Multipliers impose along the rail?
For the temperature function $T(x, y)$ subject to the linear constraint $g(x, y) = ax + by - c = 0$, an extremum requires $\nabla T = \lambda \nabla g$. Because $\nabla g = \langle a, b \rangle$, the gradient vector $\nabla T$ must be parallel to the normal vector of the constraint line. Expressed as an orthogonality condition, this requires the $2 \times 2$ cross determinant $T_x b - T_y a$ to equal zero.

#### Q28. What is the fundamental operational difference between Gradient Descent and Lagrange Multipliers in this app?
Gradient Descent is an unconstrained iterative numerical algorithm that searches an open 2D area by taking discrete steps down the negative gradient. In contrast, Lagrange Multipliers is a constrained analytical method that solves a coupled algebraic system to find exact extrema restricted strictly to a 1D path ($ax + by = c$). CalSymPy uses gradient descent for 2D component relocation and Lagrange multipliers for 1D mounting rail analysis.

#### Q29. How does `features.py` verify the analytical Lagrange Multipliers solution?
After SymPy solves the simultaneous system $T_x b - T_y a = 0$ and $ax + by = c$, `features.py` discretizes the line segment into 201 points and evaluates temperature numerically along the rail. The maximum temperature from the numerical 1D grid search is compared against the analytical candidate. Both values are reported side-by-side in Tab 12 and logged in unit tests.

#### Q30. Why must the updated coordinates in Gradient Descent be clipped to margins?
If left unconstrained, stepping along $-\nabla_{\mathbf{c}} T_s$ would eventually drive the heat source off the physical circuit board entirely. The function `np.clip` enforces realistic mechanical packaging constraints by restricting the source center to $[\text{margin}, L - \text{margin}]$ (default $0.3\,\text{cm}$ to $3.7\,\text{cm}$). This guarantees the physical microchip remains physically mounted on the plate.

---

### Section 7: Numerical Methods, Lambdify & Benchmarking

#### Q31. Why does `sp.lambdify` execute so much faster than SymPy `.subs().evalf()` in the live benchmark?
SymPy's `.subs().evalf()` traverses a symbolic expression tree and evaluates arbitrary-precision arithmetic in interpreted Python for each point individually. In contrast, `sp.lambdify` translates the symbolic expression once into compiled C-level NumPy vector instructions that evaluate all $N \times N$ array points simultaneously. Tab 9 benchmarks this difference directly using `time.perf_counter()`, typically demonstrating orders-of-magnitude acceleration.

#### Q32. Why is symbolic differentiation performed only once at startup in `models.py` rather than on slider updates?
Symbolic differentiation via `sp.diff` is computationally expensive and introduces noticeable UI latency if triggered on every slider movement. By compiling $T$, $\nabla T$, and the Hessian once into NumPy functions during application startup, slider changes only evaluate fast numerical math. This guarantees smooth, real-time reactive updates across all 10 dashboard tabs.

#### Q33. Why did NumPy 2.0 rename `np.trapz` to `np.trapezoid`, and how does CalSymPy maintain compatibility?
NumPy 2.0 standardized function naming conventions, deprecating abbreviated names like `trapz` in favor of full English words (`trapezoid`). CalSymPy maintains compatibility across all NumPy versions by using `getattr(np, 'trapezoid', getattr(np, 'trapz', None))`. This ensures the code executes identically on NumPy 1.x and NumPy 2.x environments.

#### Q34. How does `benchmark.py` ensure the benchmark test in `test_feature9_benchmark.py` is robust and never flakes?
Rather than asserting a fragile, hardcoded speedup multiplier that could fail on slow continuous-integration runners, the benchmark measures real wall-clock seconds. The test asserts that both SymPy and NumPy return numerical temperature grids that agree to within $10^{-10}$, and that the speedup ratio is strictly greater than $1.0\times$. This verifies algorithmic compilation without asserting rigid timing numbers.

#### Q35. What is the role of `pandas` across CalSymPy, and where is it used?
Pandas provides beginner-friendly, structured tabular data management in three core areas: the Tab 4 multi-model comparison table, the Tab 10 CSV summary report, and the Tab 10 coordinate grid export. It allows students and faculty to export clean data frames with column headers (`Section`, `Metric`, `Value`, `Units`) and seamless `.to_csv()` logging.

---

### Section 8: Engineering Limitations, Assumptions & Conventions

#### Q36. What is the steady-state assumption, and why does CalSymPy not use time-stepping PDEs?
CalSymPy deliberately models steady-state thermal behavior where $\frac{\partial T}{\partial t} = 0$, meaning heat generated by components is balanced by boundary heat loss. In MAT 112, first-year students study multivariable calculus (partial derivatives, gradients, double integrals), not partial differential equations or finite-difference time-stepping. This pedagogical choice keeps every line of code explainable using MAT 112 course concepts.

#### Q37. Are Models B, C, and C2 derived from physical point sources, or are they idealized closed-form distributions?
Models B, C, and C2 are idealized closed-form Fourier harmonic test fields chosen to study specific mathematical boundary conditions (Dirichlet fixed edges, Neumann insulated edges, and mixed saddle modes). They are not derived from specific physical point sources or Green's functions. Only Models A and D represent localized Gaussian heat sources representing microchips.

#### Q38. Where do the risk thresholds ($70\,^\circ\text{C}$ and $90\,^\circ\text{C}$) in `risk.py` come from?
The thresholds are engineering heuristics informed by commercial semiconductor junction limits ($T_{j\text{Max}} \approx 95\text{--}105\,^\circ\text{C}$ for Intel, AMD, and ARM silicon), rather than a rigid legal standard. Maintaining board surface temperatures below $70\,^\circ\text{C}$ guarantees a comfortable $25\text{--}35\,^\circ\text{C}$ safety margin, while exceeding $90\,^\circ\text{C}$ leaves minimal headroom and triggers severe thermal throttling.

#### Q39. Why does CalSymPy assume uniform, isotropic material properties for the plate?
Assuming constant thermal conductivity $k$, density $\rho$, and specific heat $c_p$ simplifies Fourier's law to $\mathbf{F} = -k\nabla T$ and the thermal energy integral to $E = \rho c_p \tau \iint \Delta T\,dA$. Real printed circuit boards have copper trace layers that introduce anisotropic, spatially variable conduction. Treating the plate as uniform isotropic material isolates core calculus principles without drowning students in tensor calculus.

#### Q40. Why must the Self-Test tab evaluate models strictly at default parameters?
The faculty self-test matrix verifies theoretical "known values" (such as $T(2,2) = 85.00\,^\circ\text{C}$ for Model A and $D = -1846.6$ for Model D) that are mathematically derived from factory default parameters. If the self-test evaluated at current slider values, moving a slider would cause all benchmark checks to show false failures. Isolating the self-test preserves independent theoretical verification at all times.
