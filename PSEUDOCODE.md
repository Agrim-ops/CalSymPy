# PSEUDOCODE - CalSymPy (Team 4, Delta-T)

## 1. Temperature, Model A (one hotspot)
1. Take x, y and the values T_edge, T0, s, cx, cy
2. Find r2 = (x - cx)^2 + (y - cy)^2
3. Find the hotspot factor e = exp(-r2 / s)
4. Temperature = T_edge + T0 * e
5. Return the temperature

## 2. Derivatives, Model A (worked out by hand)
1. Find e as above
2. Tx = T0 * e * (-2 * (x - cx) / s)
3. Ty = T0 * e * (-2 * (y - cy) / s)
4. Txx = T0 * e * (4 * (x - cx)^2 / s^2 - 2 / s)
5. Tyy = T0 * e * (4 * (y - cy)^2 / s^2 - 2 / s)
6. Txy = T0 * e * (4 * (x - cx) * (y - cy) / s^2)
7. Return Tx, Ty, Txx, Tyy, Txy

## 3. Model B (cold edges)
1. Find a = pi / L
2. Temperature = T_edge + T0 * sin(a*x) * sin(a*y)
3. Tx = T0 * a * cos(a*x) * sin(a*y)
4. Ty = T0 * a * sin(a*x) * cos(a*y)
5. Txx = -T0 * a^2 * sin(a*x) * sin(a*y)
6. Tyy = -T0 * a^2 * sin(a*x) * sin(a*y)
7. Txy = T0 * a^2 * cos(a*x) * cos(a*y)

## 4. Gradient and its size
1. Get Tx and Ty at the point
2. Magnitude = square root of (Tx^2 + Ty^2)
3. Return Tx, Ty and the magnitude

## 5. Second derivative test
1. Get Txx, Tyy and Txy at the point
2. D = Txx * Tyy - Txy^2
3. If D is clearly above 0 and Txx is below 0, answer "Local Maximum"
4. Else if D is above 0 and Txx is above 0, answer "Local Minimum"
5. Else if D is below 0, answer "Saddle Point"
6. Else (D is about 0), answer "Inconclusive"
7. Return Txx, Tyy, Txy, D and the answer

## 6. Hottest point (grid search)
1. Set best_temp to a very low number
2. Make n_grid equally spaced values from 0 to L
3. For each x value
4.    For each y value
5.       Find the temperature at (x, y)
6.       If it is higher than best_temp, save it and save x, y
7. Return best x, best y and best_temp

## 7. Average temperature (midpoint Riemann sum)
1. Split the plate into n by n small squares
2. Set dx = L / n and dy = L / n, and total = 0
3. For each column i and each row j
4.    Take the middle of the square: x = (i + 0.5) * dx, y = (j + 0.5) * dy
5.    Add temperature(x, y) * dx * dy to total
6. Average = total / (L * L)
7. Return the average

## 8. Tangent plane and Taylor polynomial at (a, b)
1. Find dx = x - a and dy = y - b
2. Get T, Tx, Ty, Txx, Tyy, Txy at (a, b)
3. Tangent plane = T + Tx * dx + Ty * dy
4. Taylor degree 2 = tangent plane + 0.5 * (Txx*dx^2 + 2*Txy*dx*dy + Tyy*dy^2)
5. Return the value

## 9. Gradient descent (moving the chip to a cooler place)
1. Start at (x, y) and save the start in a path list
2. Repeat for the chosen number of steps (default 40):
   1. Get Tx and Ty at (x, y)
   2. Find magnitude = sqrt(Tx^2 + Ty^2)
   3. If magnitude > 0:
      Move downhill by unit step: x = x - step_size * (Tx / magnitude), y = y - step_size * (Ty / magnitude)
   4. Keep x and y between 0.2 and L - 0.2 (clamp)
   5. Add the new point to the path
3. Return the path and the temperature at the last point

## 10. Best placement search (closest safe location)
1. Check the temperature at the start position (start_x, start_y)
2. If start temperature is already below the limit (default 70):
   Return start_x, start_y, start temperature, and distance 0
3. Set up a grid inside safe margins from 0.2 to L - 0.2
4. Scan all grid points (x, y) with two loops:
   1. Find temperature T at (x, y)
   2. If T < limit:
      Compute distance from start: sqrt((x - start_x)^2 + (y - start_y)^2)
      If distance is smaller than best distance so far, save (x, y, T, distance)
5. If a safe point was found, return its coordinates, temperature and distance
6. If no point on the plate is below the limit, return None

## 11. Risk level
1. If temperature is below 70, answer "Low"
2. Else if temperature is 90 or below, answer "Medium"
3. Else answer "High"
(Intel says the maximum junction temperature usually lies between about 100 and 110 degrees C, depending on the product. Our 70 and 90 degree limits are our own rule of thumb with a safety margin.)

## 12. Cooling suggestions
1. Find the risk level of the peak temperature
2. If Low, add "no action needed" to the list
3. Else find drop = peak - 69.9, rounded to 1 decimal
4. Add: peak must fall by at least drop degrees to reach Low
5. Add option 1: reduce the chip heating T0 by drop
6. Add option 2: cool the plate edges and surroundings (T_edge) by drop
7. If High, also add: use a heat sink or fan, and move heat-sensitive parts away
8. Return the list

## 13. Console program
1. Create a plate with Model A
2. Repeat until the user chooses 0
3.    Show the menu and read the choice
4.    Choice 1: change model or parameters (reject values that are not numbers or not above 0 for s and L)
5.    Choice 2: draw the heat map
6.    Choice 3: ask for x, y, check they are inside the plate, print T, gradient and the D test
7.    Choice 4: hottest point, risk level and suggestions
8.    Choice 5: average temperature
9.    Choice 6: gradient descent, best placement search, and optional plot
10.   Choice 7: save the report to csv or txt
