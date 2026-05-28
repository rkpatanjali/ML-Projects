# Deployment Guide for Windows

## Quick Summary
You have two parts to deploy:
1. **Backend API** (FastAPI) → Cloud Run
2. **Frontend** (Streamlit) → Streamlit Cloud OR Firebase Hosting

---

## OPTION A: Easiest (Recommended for Beginners)

### Deploy Backend to Google Cloud Run (Free Tier)
1. Install Google Cloud CLI: https://cloud.google.com/sdk/docs/install-sdk
2. In PowerShell:
```powershell
gcloud init
gcloud auth login
gcloud config set project boston-housing-ml
gcloud run deploy boston-housing-api --source . --platform managed --region us-central1 --allow-unauthenticated
```

3. Copy the service URL (looks like: `https://boston-housing-api-xxxxx.a.run.app`)

### Deploy Frontend to Streamlit Cloud
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your GitHub repo and file: `streamlit_app/app.py`
5. Update API URL in [streamlit_app/app.py](streamlit_app/app.py):

Replace:
```python
response = requests.post(
    "http://127.0.0.1:8000/predict",
```

With:
```python
response = requests.post(
    "https://YOUR-SERVICE-URL/predict",
```

---

## OPTION B: Using Docker + Vercel/Railway

These are even simpler - just connect GitHub and they auto-deploy.

---

## Commands to Run (Copy-Paste)

### 1. First Time Setup
```powershell
npm install -g firebase-tools
gcloud init
firebase login
```

### 2. Deploy
```powershell
firebase deploy
```

---

## Troubleshooting

### Firebase deploy fails
- Make sure you're in project root directory
- Run: `firebase --version` (should show version number)
- Run: `firebase list` (should show your project)

### Build errors
- Delete folder: `mlenv`
- Delete folder: `.firebase`
- Try again

### Port conflicts
- Your app runs on port 8000
- Streamlit runs on port 8501
- Make sure nothing is using these ports

---

## Still Stuck?
Ask me for help with specific error messages!
