# Football Central

A modern ESPN-inspired football news website built with Python Flask.

## Features

- Responsive homepage
- Featured story
- Trending news
- Match cards
- Category pages
- Individual article pages
- Newsletter UI
- Mobile navigation
- Custom 404 page

## Run on Windows

1. Install Python from https://python.org
2. Open this folder in VS Code.
3. Open Terminal.
4. Run:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

5. Open:

```text
http://127.0.0.1:5000
```

## Run on macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Add news

Open `app.py` and add another item inside the `ARTICLES` list.

## Change website name

Search for `Football Central` in the project files and replace it with your website name.

## Important

This project uses sample text and external Unsplash images. Replace sample content with your own licensed news, images and data before publishing.


## Upload to GitHub in your browser

1. Create a new empty GitHub repository.
2. Open the repository.
3. Select **Add file > Upload files**.
4. Upload the project files and folders, not the ZIP file itself.
5. Commit the changes.

## Publish online with Render

GitHub stores the code, but GitHub Pages cannot run this Flask server.

1. Sign in to Render.
2. Select **New > Web Service**.
3. Connect your GitHub account and select this repository.
4. Render can read `render.yaml`, or use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Deploy the web service.
