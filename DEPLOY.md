# Deployment Guide (Render)

**Project**: CalSymPy (Team 4, Delta-T)  
**Target Platform**: Render (Web Service)

## 1. Running Locally
To test the web application on your local machine:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

## 2. Deploying to Render
1. Push your repository to GitHub.
2. Sign in to Render (https://render.com) and click **New +** -> **Web Service**.
3. Select your GitHub repository (`CalSymPy`).
4. Configure the service settings:
   - **Name**: `calsympy-heat-map`
   - **Region**: Closest region (e.g. Singapore or Frankfurt)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Set Python version under **Environment Variables** (Render also reads `runtime.txt`):
   - `PYTHON_VERSION`: `3.12.10`
6. Click **Deploy Web Service**.
7. Once the build completes, the live URL will appear at the top of the dashboard:
   `https://calsympy-heat-map.onrender.com`

## 3. Free-Tier Sleep Notice
- On Render's free tier, the web service sleeps after 15 minutes of inactivity.
- The first visit after sleeping takes about 45 to 60 seconds to wake up (cold start). Subsequent requests respond immediately.
