# Using Partial Derivatives and Matplotlib in Python to Visualize Heat Distribution on a Surface

Team 4 (Delta-T), Mathematics and Python Programming  
CalSymPy project

## What this project does

This program models how temperature is spread over a flat square plate, for example a circuit board with a chip on it. It uses calculus to find the hottest point, the direction heat changes fastest, the average temperature, and a better place to put a heat-sensitive part. It shows the results as heat maps and also gives simple cooling suggestions. The temperature depends only on position (x, y), so there is no time variable.

## Team

| Member | Role |
| --- | --- |
| Anvesha Misra | Project Manager |
| Swastik Mishra | Researcher |
| Manvi Singh | Mathematical Modeler |
| Advitiya Sharma | Pseudocode Formulator |
| Tanmay Singh | Code Developer |
| Agrim Goel | Program Deployer and Tester |
| Pari Raj | Information Analyst |

## The two models

The plate has side length L = 4 cm. Both models are fixed formulas that we chose to give realistic shapes. They are not solutions of the heat equation.

Model A (single hotspot): one chip at (cx, cy) heats the area around it.

    T(x, y) = T_edge + T0 * exp(-((x - cx)^2 + (y - cy)^2) / s)

Default values: T_edge = 25, T0 = 60, s = 2, cx = cy = 2. The peak is 85 degrees C at (2, 2).

Model B (cold edges): the edges are kept at T_edge and the plate is hottest in the middle.

    T(x, y) = T_edge + T0 * sin(pi*x/L) * sin(pi*y/L)

Default values: T_edge = 20, T0 = 50. The peak is 70 degrees C at (2, 2).

## Calculus used

- Partial derivatives Tx and Ty, and the gradient vector with its magnitude. The gradient points in the direction where temperature rises fastest.
- Second partial derivatives Txx, Tyy and Txy, and the second derivative test D = Txx * Tyy - Txy^2. D > 0 with Txx < 0 is a maximum, D > 0 with Txx > 0 is a minimum, D < 0 is a saddle point, and D = 0 is inconclusive.
- Double integral for the average temperature, calculated with a midpoint Riemann sum.
- Tangent plane (linear approximation) and a degree 2 Taylor polynomial around a point.
- Gradient descent: a chip is moved step by step in the direction of -gradient so it ends up in a cooler place.

All derivatives are worked out by hand and written as formulas in models.py. SymPy is used only in check_with_sympy.py to confirm the hand formulas.

## Risk level and cooling suggestions

The peak temperature is classified as Low (below 70 degrees C), Medium (70 to 90) or High (above 90). These limits are our own choice, so they are only rules of thumb. For Medium and High, the program says how many degrees the peak must drop to reach Low and lists simple options such as reducing the chip heating, cooling the edges, adding a heat sink or fan, or moving the part. This is a set of if/else rules, not engineering advice.

## How to run

Install the libraries:

    pip install -r requirements.txt

Console version:

    python main.py

Web version:

    streamlit run app.py

Checks:

    python check_with_sympy.py
    python test_calculus.py

Live link: (add after deployment)

## Files

- models.py: the two temperature models, their hand-derived derivatives, and the Plate class
- calculus.py: gradient, second derivative test, average temperature, tangent plane, Taylor polynomial, gradient descent, hottest point search, risk level, cooling suggestions
- plots.py: heat map and gradient descent plots with Matplotlib
- main.py: console menu
- app.py: Streamlit web page (a thin layer on top of the same functions)
- check_with_sympy.py: compares hand derivatives with SymPy
- test_calculus.py: tests with assert statements
- PSEUDOCODE.md: pseudo-code for the main algorithms
- TEST_REPORT.md: tests we ran and the bugs found and fixed
- DEPLOY.md: how the web app was deployed
- notebooks/colab_backup.ipynb: backup copy that runs on Google Colab

## Libraries

NumPy, Matplotlib, Pandas and SymPy are used for the project. Streamlit is used only for the web page.

## Limitations

- The plate is a simple, flat, uniform square and the temperature is steady (it does not change with time).
- The two models are idealised shapes and have not been compared with real measurements.
- The risk limits and the cooling advice are our own simple rules.
- The average temperature is an approximation and gets more accurate when more steps are used.
