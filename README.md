# GoalStream Flask Website

## Features

- Modern responsive football website
- Match cards with live and upcoming filters
- HLS `.m3u8` and MP4 video player
- Different stream URL for each match
- News list and article pages
- Upload news with an image
- SQLite database
- Delete published news
- Ready for GitHub + Render deployment

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

News upload page:

```text
http://127.0.0.1:5000/admin/news
```

## Change a match stream

Open `templates/index.html`.

Find:

```html
onclick="openPlayer('Real Madrid vs Barcelona', 'STREAM_URL')"
```

Replace `STREAM_URL` with your authorized `.m3u8` or `.mp4` URL.

## Deploy with GitHub and Render

1. Upload this project to a GitHub repository.
2. In Render, create a Web Service from the repository.
3. Build command:

```text
pip install -r requirements.txt
```

4. Start command:

```text
gunicorn app:app
```

## Important

The admin page currently has no login protection. Add authentication before using it publicly.

Use only legally licensed video streams and news content you are allowed to publish.


## Real live scores

This version supports API-Football live results.

Create an API key and set this environment variable:

```text
API_FOOTBALL_KEY=your_key_here
```

### Windows PowerShell

```powershell
$env:API_FOOTBALL_KEY="your_key_here"
python app.py
```

### macOS / Linux

```bash
export API_FOOTBALL_KEY="your_key_here"
python app.py
```

### Render

In your Render service, open **Environment** and add:

```text
API_FOOTBALL_KEY
```

Paste your API-Football key as the value, then redeploy.

The browser requests `/api/live-scores` every 60 seconds. Your API key remains on the Python server and is not exposed in the HTML.

Without a key, the site shows clearly labeled demo scores.
