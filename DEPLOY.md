# Deployment Guide (Streamlit Community Cloud)

**Project**: CalSymPy (Team 4, Delta-T)  
**Target Platform**: Streamlit Community Cloud

## 1. Running Locally
To test the web application on your local machine:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

## 2. Deploying to Streamlit Community Cloud
1. Push your repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
3. Click **New app**.
4. Select your repository settings:
   - **Repository**: Your GitHub repo (e.g. `Agrim-ops/CalSymPy`)
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. In **Advanced settings**, set the Python version to **3.12**.
6. Click **Deploy!**.
7. Streamlit Cloud will install dependencies from `requirements.txt` and launch the web app.
