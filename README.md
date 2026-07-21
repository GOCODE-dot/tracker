# Consensual Location Sharing App

A small, honest location-sharing tool for two people who both agree to it.
No hidden tracking — the sharer must click a visible "Yes, share my location"
button, approve their browser's own location permission prompt, and can stop
sharing at any time.

## What you need

1. **Python 3.9+**
2. **A free Google Maps API key** (for the map on your dashboard):
   - Go to https://console.cloud.google.com/
   - Create a project (or use an existing one)
   - Enable the **"Maps JavaScript API"**
   - Go to "Credentials" → "Create Credentials" → "API key"
   - Copy the key
   - Open `templates/dashboard.html` and replace `YOUR_API_KEY_HERE` with it
   - (Recommended) Restrict the key to your domain/IP in the Google Cloud
     console so it can't be used elsewhere.
   - Google's free tier covers this kind of light personal use, but check
     current pricing at https://mapsplatform.google.com/pricing/

## Install & run

```bash
pip install -r requirements.txt
python app.py
```

This starts a server on port 5000.

- **Her link:** `http://<your-ip-or-domain>:5000/her`
- **Your dashboard:** `http://<your-ip-or-domain>:5000/dashboard`

## Deploying to Railway (free, works from any phone)

Railway gives you a public HTTPS URL automatically — no card required for
small personal projects on their free usage tier, no server to manage.

**1. Push this folder to a GitHub repo**
- Create a new repo on https://github.com/new
- In this folder, run:
  ```bash
  git init
  git add .
  git commit -m "initial commit"
  git branch -M main
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```

**2. Deploy on Railway**
- Go to https://railway.app and sign in with GitHub
- Click **New Project → Deploy from GitHub repo**
- Pick the repo you just pushed
- Railway auto-detects Python, installs `requirements.txt`, and starts the
  app using the included `Procfile` — nothing else to configure
- Once it finishes building, click the deployment → **Settings → Networking
  → Generate Domain** to get a public URL like
  `https://your-app.up.railway.app`

**3. Share the links**
- Her link: `https://your-app.up.railway.app/her`
- Your dashboard: `https://your-app.up.railway.app/dashboard`

Both work directly from any phone browser — no app install needed. Railway
serves everything over HTTPS automatically, which is required for phones to
allow location access.

**Note on redeploys:** the location data is stored in memory, so it resets
if the app restarts (e.g. after you push a new change). That's expected —
just have her tap "Yes, share" again after a redeploy.

## How it works

- She opens `/her`, clicks the button, and her browser asks her to confirm
  location permission — two separate, visible consent steps.
- While sharing is on, her coordinates are sent to the server every few
  seconds and stored in memory (nothing is written to disk in this version).
- She can hit "Stop sharing" any time, which clears her last known location
  immediately.
- You open `/dashboard` and see her live position on a Google Map, with a
  clear "Sharing is ON / Not sharing" indicator — you always know the state,
  not just her.

## Notes / things to consider adding

- **Auth**: right now anyone with the dashboard link can view the location.
  For real use, add a simple password or login.
- **Persistence**: switch the in-memory `state` dict to a small SQLite table
  if you want history instead of just "current location."
- **Location history**: currently only the latest point is kept. You could
  log each update with a timestamp for a trail on the map.
