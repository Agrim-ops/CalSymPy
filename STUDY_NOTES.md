# CalSymPy — Student Study Notes (STUDY_NOTES.md)
**Course**: MAT 112 Engineering Mathematics & Python  
**Project**: CalSymPy v2 (Team 4, Delta-T)

---

## 1. `models.py` Functions

### `temp_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0)`
- **What it does**: Computes the temperature at coordinates $(x, y)$ for a single Gaussian hotspot.
- **Formula or idea**: $T(x, y) = T_{\text{edge}} + T_0 \exp\left(-\frac{(x - c_x)^2 + (y - c_y)^2}{s}\right)$.
- **Example**:
```python
import models
t = models.temp_a(2.0, 2.0)
print("Center temp:", t)
```

### `grad_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0)`
- **What it does**: Evaluates the first partial derivatives $T_x$ and $T_y$ by hand for Model A.
- **Formula or idea**: By chain rule on exponential, $T_x = T_0 \exp(-r^2/s) \cdot \left(-\frac{2(x - c_x)}{s}\right)$ and $T_y = T_0 \exp(-r^2/s) \cdot \left(-\frac{2(y - c_y)}{s}\right)$.
- **Example**:
```python
import models
tx, ty = models.grad_a(3.0, 2.0)
print("Slopes at (3, 2):", tx, ty)
```

### `hessian_a(x, y, t_edge=25.0, t0=60.0, s=2.0, cx=2.0, cy=2.0)`
- **What it does**: Evaluates the unmixed and mixed second partial derivatives ($T_{xx}, T_{yy}, T_{xy}$) by hand for Model A.
- **Formula or idea**: By product rule, $T_{xx} = T_0 \exp(-r^2/s) \left(\frac{4(x-c_x)^2}{s^2} - \frac{2}{s}\right)$ and $T_{xy} = T_0 \exp(-r^2/s) \left(\frac{4(x-c_x)(y-c_y)}{s^2}\right)$.
- **Example**:
```python
import models
txx, tyy, txy = models.hessian_a(2.0, 2.0)
print("Curvatures at peak:", txx, tyy, txy)
```

### `temp_b(x, y, t_edge=20.0, t0=50.0, L=4.0)`
- **What it does**: Computes the temperature on a plate with fixed cold edges using a 2D sine pattern.
- **Formula or idea**: $T(x, y) = T_{\text{edge}} + T_0 \sin\left(\frac{\pi x}{L}\right) \sin\left(\frac{\pi y}{L}\right)$.
- **Example**:
```python
import models
t = models.temp_b(2.0, 2.0)
print("Model B center temp:", t)
```

### `grad_b(x, y, t_edge=20.0, t0=50.0, L=4.0)`
- **What it does**: Computes the analytical first partial derivatives of Model B.
- **Formula or idea**: $T_x = T_0 \frac{\pi}{L} \cos\left(\frac{\pi x}{L}\right) \sin\left(\frac{\pi y}{L}\right)$ and $T_y = T_0 \frac{\pi}{L} \sin\left(\frac{\pi x}{L}\right) \cos\left(\frac{\pi y}{L}\right)$.
- **Example**:
```python
import models
tx, ty = models.grad_b(1.0, 2.0)
print("Model B slopes at (1, 2):", tx, ty)
```

### `hessian_b(x, y, t_edge=20.0, t0=50.0, L=4.0)`
- **What it does**: Computes the second partial derivatives of Model B.
- **Formula or idea**: $T_{xx} = -T_0 (\frac{\pi}{L})^2 \sin(\frac{\pi x}{L})\sin(\frac{\pi y}{L})$, $T_{yy} = -T_0 (\frac{\pi}{L})^2 \sin(\frac{\pi x}{L})\sin(\frac{\pi y}{L})$, and $T_{xy} = T_0 (\frac{\pi}{L})^2 \cos(\frac{\pi x}{L})\cos(\frac{\pi y}{L})$.
- **Example**:
```python
import models
txx, tyy, txy = models.hessian_b(2.0, 2.0)
print("Model B peak Hessian:", txx, tyy, txy)
```

### `temp_c(x, y, t_edge=25.0, t1=40.0, s1=1.5, cx1=1.2, cy1=1.2, t2=40.0, s2=1.5, cx2=2.8, cy2=2.8)`
- **What it does**: Computes the temperature resulting from two separate Gaussian microchips on one board.
- **Formula or idea**: Sum of two Gaussian functions: $T = T_{\text{edge}} + T_1 \exp(-r_1^2 / s_1) + T_2 \exp(-r_2^2 / s_2)$.
- **Example**:
```python
import models
t = models.temp_c(1.2, 1.2)
print("Model C near chip 1:", t)
```

### `grad_c(x, y, t_edge=25.0, t1=40.0, s1=1.5, cx1=1.2, cy1=1.2, t2=40.0, s2=1.5, cx2=2.8, cy2=2.8)`
- **What it does**: Computes the combined gradient vector from two Gaussian heat sources.
- **Formula or idea**: Linearity of differentiation: the gradient of a sum equals the sum of the individual gradients ($\nabla T = \nabla T_1 + \nabla T_2$).
- **Example**:
```python
import models
tx, ty = models.grad_c(2.0, 2.0)
print("Model C slopes at midpoint:", tx, ty)
```

### `hessian_c(x, y, t_edge=25.0, t1=40.0, s1=1.5, cx1=1.2, cy1=1.2, t2=40.0, s2=1.5, cx2=2.8, cy2=2.8)`
- **What it does**: Evaluates the second partial derivatives for the two-hotspot configuration.
- **Formula or idea**: Sum of the second partial derivatives of both Gaussian sources ($T_{xx} = T_{xx1} + T_{xx2}$, etc.).
- **Example**:
```python
import models
txx, tyy, txy = models.hessian_c(2.0, 2.0)
print("Model C saddle Hessian:", txx, tyy, txy)
```

### `Plate(model="A")`
- **What it does**: Simple class storing current plate dimensions, parameters, and providing helper methods for temperature and derivatives.
- **Formula or idea**: Object-oriented data container bundling plate parameters with `get_temp(x, y)`, `get_grad(x, y)`, and `get_hessian(x, y)`.
- **Example**:
```python
import models
p = models.Plate("A")
print("Current plate side length:", p.L)
```

---

## 2. `calculus.py` Functions

### `gradient(plate, x, y)`
- **What it does**: Calculates the partial derivatives and Euclidean gradient magnitude at $(x, y)$.
- **Formula or idea**: $\nabla T = \langle T_x, T_y \rangle$ and $|\nabla T| = \sqrt{T_x^2 + T_y^2}$.
- **Example**:
```python
import models, calculus
p = models.Plate("A")
tx, ty, mag = calculus.gradient(p, 3.0, 2.0)
```

### `second_derivative_test(plate, x, y)`
- **What it does**: Classifies a critical point as a maximum, minimum, or saddle point using the Hessian determinant.
- **Formula or idea**: $D = T_{xx} T_{yy} - (T_{xy})^2$. If $D > 0$ and $T_{xx} < 0 \implies$ Maximum; if $D > 0$ and $T_{xx} > 0 \implies$ Minimum; if $D < 0 \implies$ Saddle Point.
- **Example**:
```python
import models, calculus
p = models.Plate("A")
txx, tyy, txy, d, classification = calculus.second_derivative_test(p, 2.0, 2.0)
```

### `average_temperature(plate, n_steps=80)`
- **What it does**: Calculates the average temperature across the plate using a 2D Riemann sum.
- **Formula or idea**: $T_{\text{avg}} = \frac{1}{L^2} \iint_R T(x, y)\,dA \approx \frac{1}{L^2} \sum_{i} \sum_{j} T(x_i, y_j) \Delta x \Delta y$.
- **Example**:
```python
import models, calculus
p = models.Plate("A")
avg = calculus.average_temperature(p)
```

### `tangent_plane(plate, a, b, x, y)`
- **What it does**: Approximates the temperature near $(a, b)$ using the tangent plane linearisation.
- **Formula or idea**: $L(x, y) = T(a, b) + T_x(a, b)(x - a) + T_y(a, b)(y - b)$.
- **Example**:
```python
import models, calculus
p = models.Plate("A")
t_approx = calculus.tangent_plane(p, 2.0, 2.0, 2.05, 2.05)
```

### `taylor_degree_2(plate, a, b, x, y)`
- **What it does**: Approximates the temperature near $(a, b)$ using a degree-2 Taylor polynomial including surface curvature.
- **Formula or idea**: $P_2(x, y) = L(x, y) + \frac{1}{2} T_{xx}(x - a)^2 + T_{xy}(x - a)(y - b) + \frac{1}{2} T_{yy}(y - b)^2$.
- **Example**:
```python
import models, calculus
p = models.Plate("A")
t_taylor = calculus.taylor_degree_2(p, 2.0, 2.0, 2.1, 2.1)
```

### `gradient_descent(plate, start_x, start_y, step_size=0.08, steps=30)`
- **What it does**: Moves a temperature-sensitive chip away from the hotspot by iteratively stepping down the negative gradient.
- **Formula or idea**: $x_{k+1} = x_k - \alpha T_x$ and $y_{k+1} = y_k - \alpha T_y$ (stepping in the direction of steepest temperature drop).
- **Example**:
```python
import models, calculus
p = models.Plate("A")
path, final_temp = calculus.gradient_descent(p, 1.5, 1.5)
```

### `find_hottest_point(plate, n_grid=50)`
- **What it does**: Searches a discrete 2D grid using nested loops to locate the hottest point on the plate.
- **Formula or idea**: Compares temperatures at all $(x_i, y_j)$ grid samples and records the maximum value and coordinates.
- **Example**:
```python
import models, calculus
p = models.Plate("A")
hx, hy, ht = calculus.find_hottest_point(p)
```

### `get_risk_level(temp)`
- **What it does**: Assigns an operational safety category based on component peak temperature.
- **Formula or idea**: If $T < 70^\circ\text{C} \implies$ Low; if $70 \le T \le 90^\circ\text{C} \implies$ Medium; if $T > 90^\circ\text{C} \implies$ High.
- **Example**:
```python
import calculus
risk = calculus.get_risk_level(85.0)
print("Risk is:", risk)
```

---

## 3. `plots.py` Functions

### `plot_heatmap(plate, n_grid=50)`
- **What it does**: Generates and displays a 2D false-color temperature heatmap with overlaid contour lines.
- **Formula or idea**: Discretizes $[0, L] \times [0, L]$ using `np.meshgrid` and displays scalar temperature field via `plt.imshow` and `plt.contour`.
- **Example**:
```python
import models, plots
p = models.Plate("A")
plots.plot_heatmap(p)
```

### `plot_quiver(plate, n_grid=12)`
- **What it does**: Displays gradient vectors across the plate as directional arrows showing the path of steepest ascent.
- **Formula or idea**: Arrows at $(x, y)$ pointing along vector $\langle T_x, T_y \rangle$ via `plt.quiver`.
- **Example**:
```python
import models, plots
p = models.Plate("A")
plots.plot_quiver(p)
```

### `plot_descent_path(plate, path, n_grid=50)`
- **What it does**: Plots the trajectory taken by gradient descent overlaid on the plate temperature map.
- **Formula or idea**: Traces line connecting discrete positions $(x_k, y_k)$ from initial hot location to cooled final location.
- **Example**:
```python
import models, calculus, plots
p = models.Plate("A")
path, t_final = calculus.gradient_descent(p, 1.5, 1.5)
plots.plot_descent_path(p, path)
```

---

## 4. `main.py` Functions

### `show_menu()`
- **What it does**: Prints the console options menu (0 to 7) to standard output.
- **Formula or idea**: Text user interface navigation options.
- **Example**:
```python
import main
main.show_menu()
```

### `option_choose_model(plate)`
- **What it does**: Prompts user to pick Model A, B, or C and optionally change baseline parameters ($T_{\text{edge}}, T_0, s$).
- **Formula or idea**: Updates the active `Plate` instance settings based on console input.
- **Example**:
```python
import models, main
p = models.Plate()
# main.option_choose_model(p)  # Interactive input
```

### `option_lookup(plate)`
- **What it does**: Prompts user for a coordinate pair $(x, y)$ and displays exact $T$, gradient, and D-test classification.
- **Formula or idea**: Point-based analytical multivariable calculus evaluation.
- **Example**:
```python
import models, main
p = models.Plate("A")
# main.option_lookup(p)  # Interactive input
```

### `option_hottest(plate)`
- **What it does**: Runs grid search to report the hottest plate position, peak temperature, and risk level.
- **Formula or idea**: Grid extremum finding and heuristic threshold classification.
- **Example**:
```python
import models, main
p = models.Plate("A")
main.option_hottest(p)
```

### `option_average(plate)`
- **What it does**: Computes and displays the average plate temperature using a 2D Riemann sum double integral.
- **Formula or idea**: Continuous mean value approximation: $\frac{1}{\text{Area}}\iint_R T\,dA$.
- **Example**:
```python
import models, main
p = models.Plate("A")
main.option_average(p)
```

### `option_descent(plate)`
- **What it does**: Simulates cooling a chip by stepping away from the heat source along $-\nabla T$ and optionally plots the path.
- **Formula or idea**: Iterative gradient descent optimization.
- **Example**:
```python
import models, main
p = models.Plate("A")
# main.option_descent(p)  # Interactive input
```

### `option_save_report(plate)`
- **What it does**: Exports key calculus metrics to a `.csv` file via pandas or a `.txt` file.
- **Formula or idea**: Tabular data logging of engineering results using `pandas.DataFrame.to_csv`.
- **Example**:
```python
import models, main
p = models.Plate("A")
# main.option_save_report(p)  # Interactive input
```

### `main()`
- **What it does**: Master application controller executing the while loop until user enters 0.
- **Formula or idea**: Standard console application lifecycle loop.
- **Example**:
```python
import main
# main.main()  # Starts interactive menu loop
```
