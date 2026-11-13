# CalSymPy Web UI & Deployment Viva Q&A (APP_VIVA.md)
**Course**: MAT 112 Engineering Mathematics & Python  
**Project**: CalSymPy v2 (Team 4, Delta-T)  
**Scope**: 12 Most Likely Examiner / Faculty Viva Questions on `app.py`, Streamlit Architecture, and Cloud Deployment.

---

### Q1. Why did you choose Streamlit for this web interface instead of Tkinter, Gradio, or Flask?
**Answer**: Streamlit allows writing pure top-to-bottom Python scripts without HTML, CSS, JavaScript, callback boilerplate, or object-oriented GUI hierarchies. Unlike Tkinter (which is desktop-only and cannot run in a browser or cloud container), Streamlit deploys seamlessly to the cloud. Compared to Flask/Django, it eliminates routing tables and template engines while providing native, reactive widgets.

### Q2. How does Streamlit's execution model work when a user moves a slider or inputs a number?
**Answer**: Streamlit uses an immediate-mode reactive execution lifecycle. Every time a user interacts with a widget (changing a value or clicking a button), Streamlit re-executes the entire `app.py` script from top to bottom (line 1 to line 71) using the updated widget states.

### Q3. How does the web interface mathematically prevent division by zero or non-physical plate parameters?
**Answer**: By enforcing minimum bounds directly in the widget definitions: `min_value=0.1` for dispersion parameter $s$ and `min_value=1.0` for plate side length $L$. Because Streamlit's `st.number_input` restricts user entry to $\ge \text{min\_value}$, neither $s$ nor $L$ can ever be zero or negative, completely preventing `ZeroDivisionError`.

### Q4. Why did you add `show=False` to `plots.py`, and how does `st.pyplot(fig)` differ from `plt.show()`?
**Answer**: In desktop environments, `plt.show()` opens a blocking GUI window that halts code execution until closed. On a headless cloud web server, `plt.show()` would freeze the application or crash. Adding `show=False` returns the Matplotlib `Figure` object directly, allowing Streamlit's `st.pyplot(fig)` to serialize it into an SVG/PNG stream and render it directly in the client's web browser.

### Q5. What happens if a user enters point lookup coordinates outside the plate?
**Answer**: An `if-else` condition checks whether $x$ or $y$ is strictly less than 0 or greater than $L$. If out of bounds, `st.warning()` displays an informative message alerting the user and suppresses the calculus evaluation, preventing misleading mathematical evaluations outside the physical boundary.

### Q6. Does the web interface re-evaluate the double integral and grid search on every slider change, and is it fast enough?
**Answer**: Yes, on every rerun it computes the 2D midpoint Riemann sum ($80 \times 80 = 6,400$ cells) and the grid search ($50 \times 50 = 2,500$ points). Because the functions in `models.py` and `calculus.py` are vectorized with NumPy, both calculations take only ~15 to 20 milliseconds combined, making the interface completely smooth and responsive without requiring complex background caching.

### Q7. How does the "Move chip" button behave during Streamlit reruns?
**Answer**: Streamlit's `st.button("Move chip")` returns `True` only during the single script rerun triggered immediately after the user clicks the button. In that run, the app executes `calculus.gradient_descent`, extracts the 30-step downhill trajectory, displays the final cooled temperature, and plots the path overlay via `plots.plot_descent_path`. On subsequent edits to other widgets, the button returns `False` unless clicked again.

### Q8. How does the report download work without saving temporary files to the server's hard drive?
**Answer**: We construct a pandas DataFrame from our in-memory metrics and call `df.to_csv(index=False)`, which produces a CSV string stored entirely in RAM. `st.download_button` transfers this in-memory string directly through the HTTP response to the user's browser, eliminating disk I/O, server write permission errors, and temporary file accumulation.

### Q9. What command starts the web application in production on Render, and why are `--server.port` and `--server.address` required?
**Answer**: The command is:
`streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- `--server.port $PORT`: Render dynamically assigns a port number via the `$PORT` environment variable; the app must bind to this port rather than the default 8501.
- `--server.address 0.0.0.0`: Binds the server to all network interfaces so incoming traffic from Render's reverse proxy can reach the container.

### Q10. Why is the `PYTHON_VERSION` environment variable pinned in Render's configuration?
**Answer**: Render's default environment might otherwise provision an older or mismatched Python runtime (e.g. Python 3.10). Pinning `PYTHON_VERSION = 3.12.10` ensures complete parity with our local testing environment and guarantees that all pinned library wheels in `requirements.txt` install cleanly.

### Q11. What is the free-tier sleep phenomenon on Render, and what causes cold-start latency?
**Answer**: To conserve resources, Render's free tier automatically suspends (spins down) web services that receive no HTTP traffic for 15 minutes. When a new user accesses the URL, Render spins up a fresh container and runs the start command, causing an initial "cold start" delay of 45–60 seconds. Once the container is awake, response times return to sub-second speeds.

### Q12. How does the design maintain a strict separation of concerns between `app.py` and the core calculus modules?
**Answer**: `app.py` contains zero multivariable calculus equations or algorithms. It acts strictly as a graphical presentation controller: collecting user inputs, passing them into the `Plate` data object, requesting results from `calculus.py` (`gradient`, `second_derivative_test`, `average_temperature`, `gradient_descent`), and rendering the outputs. This ensures that the core mathematics in `models.py` and `calculus.py` remains completely modular, testable, and reusable across both console (`main.py`) and web (`app.py`) interfaces.
