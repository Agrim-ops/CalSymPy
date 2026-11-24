# CalSymPy: Blocked Pseudocode for PPT Slides (`blocked_pseudocode.md`)

> **Course**: MAT 112 Engineering Mathematics & Python Programming  
> **Team 4 (Delta-T)**: Circuit Board Thermal Distribution & Multivariable Calculus  
> **Purpose**: Visual, modular, slide-ready pseudocode blocks for PowerPoint presentation slides.

---

## Slide Layout Guide
- **Slide 1**: Mathematical Modeling & Surface Calculus (Blocks 1, 2, 3)
- **Slide 2**: Spatial Integration & Thermal Optimization (Blocks 4, 5, 6)
- **Alternative 16:9 Master Slide**: All 6 blocks placed in a 3×2 grid layout.

---

### BLOCK 1: Thermal Surface Modeling
```text
+-----------------------------------------------------------------------+
| MODULE 1: Surface Temperature Evaluation [T(x, y)]                    |
+-----------------------------------------------------------------------+
| INPUT : Model in {"A", "B"}, Coordinates (x, y), Params (T0, T_edge, s)|
| OUTPUT: Surface temperature T in degrees Celsius                      |
+-----------------------------------------------------------------------+
| BEGIN                                                                 |
|   IF Model == "A" THEN  // Gaussian Hotspot Model                     |
|       r_sq <- (x - cx)^2 + (y - cy)^2                                 |
|       T <- T_edge + T0 * EXP(-r_sq / s)                               |
|   ELSE                  // Sinusoidal Standing Wave Model             |
|       k <- PI / L                                                     |
|       T <- T_edge + T0 * SIN(k * x) * SIN(k * y)                      |
|   END IF                                                              |
|   RETURN T                                                            |
| END                                                                   |
+-----------------------------------------------------------------------+
```

---

### BLOCK 2: Vector Gradient & Rate of Steepest Rise
```text
+-----------------------------------------------------------------------+
| MODULE 2: Gradient Vector & Magnitude [grad(x, y)]                    |
+-----------------------------------------------------------------------+
| INPUT : Plate object, Coordinates (x, y)                              |
| OUTPUT: Directional vector <Tx, Ty> and scalar magnitude ||grad T||   |
+-----------------------------------------------------------------------+
| BEGIN                                                                 |
|   // Compute analytical first partial derivatives via Chain Rule      |
|   Tx <- d/dx [ T(x, y) ]       // Rate of temperature change along x  |
|   Ty <- d/dy [ T(x, y) ]       // Rate of temperature change along y  |
|                                                                       |
|   grad_vector <- <Tx, Ty>      // Compass direction of steepest heat  |
|   magnitude   <- SQRT(Tx^2 + Ty^2) // Steepness of ascent (C/cm)      |
|                                                                       |
|   RETURN Tx, Ty, magnitude                                            |
| END                                                                   |
+-----------------------------------------------------------------------+
```

---

### BLOCK 3: Hessian Curvature & Second Derivative D-Test
```text
+-----------------------------------------------------------------------+
| MODULE 3: Critical Point Classification [Second Derivative Test]     |
+-----------------------------------------------------------------------+
| INPUT : Plate object, Coordinates (x, y)                              |
| OUTPUT: Discriminant D, Geometric Classification                     |
+-----------------------------------------------------------------------+
| BEGIN                                                                 |
|   // Compute second partial derivatives (Hessian matrix elements)     |
|   Txx <- d2/dx2 [ T ],  Tyy <- d2/dy2 [ T ],  Txy <- d2/dxdy [ T ]   |
|   D <- (Txx * Tyy) - (Txy^2)   // Hessian determinant                 |
|                                                                       |
|   IF magnitude >= 0.01 THEN                                           |
|       RETURN D, "Not a critical point (gradient is non-zero)"         |
|   ELSE IF ABS(D) < 1e-6 THEN                                          |
|       RETURN D, "Inconclusive (flat / higher-order contact)"          |
|   ELSE IF D < 0.0 THEN                                                |
|       RETURN D, "Saddle Point (mountain pass / Pringles shape)"       |
|   ELSE IF Txx < 0.0 THEN                                              |
|       RETURN D, "Local Maximum (hotspot peak)"                        |
|   ELSE                                                                |
|       RETURN D, "Local Minimum (cooling well)"                        |
|   END IF                                                              |
| END                                                                   |
+-----------------------------------------------------------------------+
```

---

### BLOCK 4: Spatial Average via 2D Midpoint Riemann Sum
```text
+-----------------------------------------------------------------------+
| MODULE 4: Spatial Double Integration [Average Temperature]            |
+-----------------------------------------------------------------------+
| INPUT : Plate object, Discretization resolution N (default 80)        |
| OUTPUT: Global spatial average temperature T_avg                      |
+-----------------------------------------------------------------------+
| BEGIN                                                                 |
|   dx <- L / N                  // Grid cell step size (0.05 cm)       |
|   total_sum <- 0.0                                                    |
|                                                                       |
|   FOR i = 0 TO (N - 1) DO                                             |
|       x_mid <- (i + 0.5) * dx  // Midpoint x-coordinate               |
|       FOR j = 0 TO (N - 1) DO                                         |
|           y_mid <- (j + 0.5) * dx                                     |
|           T_cell <- EVALUATE_TEMP(plate, x_mid, y_mid)                |
|           total_sum <- total_sum + (T_cell * dx * dx)                 |
|       END FOR                                                         |
|   END FOR                                                             |
|                                                                       |
|   T_avg <- total_sum / (L^2)   // Normalize by total board area       |
|   RETURN T_avg                                                        |
| END                                                                   |
+-----------------------------------------------------------------------+
```

---

### BLOCK 5: Autonomous Downhill Chip Relocation
```text
+-----------------------------------------------------------------------+
| MODULE 5: Downhill Relocation [Gradient Descent with Clamping]         |
+-----------------------------------------------------------------------+
| INPUT : Start position (x0, y0), Step size eta (0.1 cm), Steps (40)   |
| OUTPUT: Trajectory path [(x, y)...], Final temperature                |
+-----------------------------------------------------------------------+
| BEGIN                                                                 |
|   (curr_x, curr_y) <- (x0, y0)                                        |
|   path <- [ (curr_x, curr_y) ]                                        |
|                                                                       |
|   FOR step = 1 TO MaxSteps DO                                         |
|       Tx, Ty, mag <- COMPUTE_GRADIENT(plate, curr_x, curr_y)          |
|       IF mag > 0.0 THEN                                               |
|           // Step along unit negative gradient (downhill)             |
|           curr_x <- curr_x - eta * (Tx / mag)                         |
|           curr_y <- curr_y - eta * (Ty / mag)                         |
|       END IF                                                          |
|       // Physical margin safety clamping [0.2 cm, L - 0.2 cm]         |
|       curr_x <- MAX(0.2, MIN(L - 0.2, curr_x))                        |
|       curr_y <- MAX(0.2, MIN(L - 0.2, curr_y))                        |
|       path.APPEND( (curr_x, curr_y) )                                 |
|   END FOR                                                             |
|                                                                       |
|   final_temp <- EVALUATE_TEMP(plate, curr_x, curr_y)                  |
|   RETURN path, final_temp                                             |
| END                                                                   |
+-----------------------------------------------------------------------+
```

---

### BLOCK 6: Constrained Optimal Component Placement
```text
+-----------------------------------------------------------------------+
| MODULE 6: Constrained Safe Haven Placement [Best Placement]           |
+-----------------------------------------------------------------------+
| INPUT : Initial point (x0, y0), Thermal limit (70 C), Grid N (60)     |
| OUTPUT: Closest safe coordinate (x*, y*), Temperature, Distance       |
+-----------------------------------------------------------------------+
| BEGIN                                                                 |
|   IF EVALUATE_TEMP(plate, x0, y0) < limit THEN                        |
|       RETURN x0, y0, EVALUATE_TEMP(plate, x0, y0), 0.0                |
|   END IF                                                              |
|                                                                       |
|   best_candidate <- NULL                                              |
|   step_size <- (L - 0.4) / N                                          |
|                                                                       |
|   FOR i = 0 TO N DO                                                   |
|       FOR j = 0 TO N DO                                               |
|           x_cand <- 0.2 + (i * step_size)                             |
|           y_cand <- 0.2 + (j * step_size)                             |
|           T_cand <- EVALUATE_TEMP(plate, x_cand, y_cand)              |
|                                                                       |
|           IF T_cand < limit THEN                                      |
|               dist <- SQRT((x_cand - x0)^2 + (y_cand - y0)^2)         |
|               IF best_candidate IS NULL OR dist < best_candidate.dist |
|                   best_candidate <- (x_cand, y_cand, T_cand, dist)    |
|               END IF                                                  |
|           END IF                                                      |
|       END FOR                                                         |
|   END FOR                                                             |
|                                                                       |
|   RETURN best_candidate                                               |
| END                                                                   |
+-----------------------------------------------------------------------+
```

---

### MASTER PIPELINE BLOCK: End-to-End System Integration
```text
+=======================================================================+
| MASTER PIPELINE: CalSymPy Autonomous Circuit Board Thermal Management |
+=======================================================================+
| 1. INITIALIZE plate with geometry L=4.0 cm, parameters (T_edge, T0, s) |
| 2. COMPILE symbolic partial derivatives into fast NumPy callables     |
| 3. SWEEP plate grid to locate global peak: (hx, hy) at Peak_Temp      |
| 4. CLASSIFY thermal risk: Low (<70 C), Medium (70-90 C), High (>90 C) |
| 5. EVALUATE critical point stability via Hessian Discriminant D       |
| 6. INTEGRATE surface temperature via 2D Riemann sum to find T_avg     |
| 7. IF chip overheats at (x0, y0):                                     |
|       a. EXECUTE downhill gradient descent with board clamping        |
|       b. COMPUTE nearest placement below 70 C threshold               |
| 8. RENDER thermal heatmap, descent path, and target marker in UI      |
+=======================================================================+
```
