# CalSymPy Deployment Guide (DEPLOY.md)
**Course**: MAT 112 Engineering Mathematics & Python  
**Project**: CalSymPy v2 (Team 4, Delta-T)  
**Target Platform**: Render (Web Service)

---

## 1. Overview
This guide explains how to run the CalSymPy Streamlit web application (`app.py`) locally and how to deploy it to the cloud on **Render** so that anyone with a web browser can interact with the heat distribution models.

---

## 2. Running the App Locally

To test or present the web application on your local machine:
```bash
# Ensure your virtual environment is active
.\.venv\Scripts\activate

# Launch the Streamlit web interface
streamlit run app.py
```
Streamlit will automatically open your default browser to `http://localhost:8501`.

---

## 3. Prerequisites for Cloud Deployment
1. A **GitHub repository** containing the project files (`app.py`, `models.py`, `calculus.py`, `plots.py`, `requirements.txt`, and `runtime.txt`).
2. A free account on **Render** (https://render.com).

---

## 4. Step-by-Step Render Setup

### Step 1: Create a New Web Service
1. Log in to your Render Dashboard.
2. Click **New +** in the top navigation bar and select **Web Service**.
3. Connect your GitHub account and choose the repository containing CalSymPy.

### Step 2: Configure Service Settings
Fill in the basic settings:
- **Name**: `calsympy-heat-map` (or any unique name).
- **Region**: Choose the closest region (e.g., Singapore, Frankfurt, or Oregon).
- **Branch**: `trimmed` (or `main` if merged).
- **Root Directory**: Leave blank if repository root.
- **Runtime**: `Python 3`.

### Step 3: Build and Start Commands
Enter the exact build and execution commands:
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  streamlit run app.py --server.port $PORT --server.address 0.0.0.0
  ```

### Step 4: Python Version Setting
Render automatically detects the Python version specified in `runtime.txt` (`python-3.12.10`). You can also explicitly verify under **Environment Variables**:
- **Key**: `PYTHON_VERSION`
- **Value**: `3.12.10`

### Step 5: Deploy
Click **Create Web Service**. Render will clone the repository, install dependencies from `requirements.txt`, and start the Streamlit server. Once the build finishes, your live URL will appear at the top of the page (e.g., `https://calsympy-heat-map.onrender.com`).

---

## 5. Important Notes & Free-Tier Limitations

> [!WARNING]
> **Free-Tier Inactivity Sleep (Cold Starts)**:
> - Render free-tier web services automatically spin down (sleep) after **15 minutes of inactivity** to conserve server resources.
> - When a user visits the URL after the service has spun down, the first request triggers a cold boot. It typically takes **45 to 60 seconds** for the container to wake up and serve the page.
> - Once awake, the application responds smoothly and instantly to all slider and button interactions.

> [!NOTE]
> **Memory & Port Handling**:
> - Streamlit runs on port 8501 by default, but cloud providers assign dynamic ports via the `$PORT` environment variable. The `--server.port $PORT --server.address 0.0.0.0` flag ensures the server listens on all network interfaces and binds correctly to Render's internal routing.
> - Memory usage stays well below Render's 512 MB free RAM ceiling because calculations are performed with lightweight NumPy arrays without heavy external dependencies.
