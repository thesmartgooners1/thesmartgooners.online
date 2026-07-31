from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
from pathlib import Path
import sqlite3
import uuid
import os
import requests
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "football.db"
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                league TEXT NOT NULL,
                summary TEXT NOT NULL,
                content TEXT NOT NULL,
                image TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        count = db.execute("SELECT COUNT(*) AS total FROM news").fetchone()["total"]
        if count == 0:
            db.execute("""
                INSERT INTO news (title, league, summary, content)
                VALUES (?, ?, ?, ?)
            """, (
                "Welcome to GoalStream",
                "General",
                "Your football website is ready for live matches and news.",
                "Use the admin page to publish your own football news. "
                "You can upload an image, choose a league, add a short summary, "
                "and write the full article."
            ))
        db.commit()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )



def demo_live_matches():
    """Fallback cards so the interface can be tested without an API key."""
    return [
        {
            "id": "demo-1",
            "league": "Demo League",
            "league_logo": "",
            "status": "LIVE",
            "minute": 67,
            "home": {"name": "Real Madrid", "logo": "", "score": 2},
            "away": {"name": "Barcelona", "logo": "", "score": 1},
            "kickoff": "",
            "is_demo": True
        },
        {
            "id": "demo-2",
            "league": "Demo League",
            "league_logo": "",
            "status": "LIVE",
            "minute": 32,
            "home": {"name": "Liverpool", "logo": "", "score": 1},
            "away": {"name": "Arsenal", "logo": "", "score": 1},
            "kickoff": "",
            "is_demo": True
        }
    ]


def fetch_api_football_live():
    """
    Reads live fixtures from API-Football.
    Set API_FOOTBALL_KEY in your environment.
    """
    api_key = os.getenv("API_FOOTBALL_KEY", "").strip()

    if not api_key:
        return demo_live_matches(), "demo"

    response = requests.get(
        "https://v3.football.api-sports.io/fixtures",
        params={"live": "all"},
        headers={"x-apisports-key": api_key},
        timeout=12
    )
    response.raise_for_status()
    payload = response.json()

    matches = []
    for item in payload.get("response", []):
        fixture = item.get("fixture", {})
        league = item.get("league", {})
        teams = item.get("teams", {})
        goals = item.get("goals", {})
        status = fixture.get("status", {})

        matches.append({
            "id": fixture.get("id"),
            "league": league.get("name", "Football"),
            "league_logo": league.get("logo", ""),
            "status": status.get("short", "LIVE"),
            "minute": status.get("elapsed"),
            "home": {
                "name": teams.get("home", {}).get("name", "Home"),
                "logo": teams.get("home", {}).get("logo", ""),
                "score": goals.get("home")
            },
            "away": {
                "name": teams.get("away", {}).get("name", "Away"),
                "logo": teams.get("away", {}).get("logo", ""),
                "score": goals.get("away")
            },
            "kickoff": fixture.get("date", ""),
            "is_demo": False
        })

    return matches, "live"


@app.get("/api/live-scores")
def live_scores():
    try:
        matches, source = fetch_api_football_live()
        return {
            "ok": True,
            "source": source,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "matches": matches
        }
    except requests.RequestException as error:
        return {
            "ok": False,
            "source": "demo",
            "message": "Live provider is unavailable; showing demo data.",
            "error": str(error),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "matches": demo_live_matches()
        }, 200


@app.route("/")
def home():
    with get_db() as db:
        latest_news = db.execute(
            "SELECT * FROM news ORDER BY created_at DESC LIMIT 6"
        ).fetchall()
    return render_template("index.html", latest_news=latest_news)


@app.route("/news")
def news_list():
    search = request.args.get("q", "").strip()
    with get_db() as db:
        if search:
            news_items = db.execute(
                """
                SELECT * FROM news
                WHERE title LIKE ? OR league LIKE ? OR summary LIKE ?
                ORDER BY created_at DESC
                """,
                (f"%{search}%", f"%{search}%", f"%{search}%")
            ).fetchall()
        else:
            news_items = db.execute(
                "SELECT * FROM news ORDER BY created_at DESC"
            ).fetchall()
    return render_template("news.html", news_items=news_items, search=search)


@app.route("/news/<int:news_id>")
def news_detail(news_id):
    with get_db() as db:
        article = db.execute(
            "SELECT * FROM news WHERE id = ?", (news_id,)
        ).fetchone()

        if article is None:
            abort(404)

        related = db.execute(
            """
            SELECT * FROM news
            WHERE id != ? AND league = ?
            ORDER BY created_at DESC
            LIMIT 3
            """,
            (news_id, article["league"])
        ).fetchall()

    return render_template(
        "news_detail.html",
        article=article,
        related=related
    )


@app.route("/admin/news", methods=["GET", "POST"])
def admin_news():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        league = request.form.get("league", "").strip()
        summary = request.form.get("summary", "").strip()
        content = request.form.get("content", "").strip()
        image = request.files.get("image")

        if not title or not league or not summary or not content:
            flash("Please complete every required field.", "error")
            return redirect(url_for("admin_news"))

        image_name = None

        if image and image.filename:
            if not allowed_file(image.filename):
                flash("Please upload PNG, JPG, JPEG, WEBP, or GIF.", "error")
                return redirect(url_for("admin_news"))

            extension = secure_filename(image.filename).rsplit(".", 1)[1].lower()
            image_name = f"{uuid.uuid4().hex}.{extension}"
            image.save(UPLOAD_FOLDER / image_name)

        with get_db() as db:
            db.execute(
                """
                INSERT INTO news (title, league, summary, content, image)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, league, summary, content, image_name)
            )
            db.commit()

        flash("News article published.", "success")
        return redirect(url_for("news_list"))

    with get_db() as db:
        news_items = db.execute(
            "SELECT * FROM news ORDER BY created_at DESC"
        ).fetchall()

    return render_template("admin_news.html", news_items=news_items)


@app.post("/admin/news/<int:news_id>/delete")
def delete_news(news_id):
    with get_db() as db:
        article = db.execute(
            "SELECT * FROM news WHERE id = ?", (news_id,)
        ).fetchone()

        if article is None:
            abort(404)

        if article["image"]:
            image_path = UPLOAD_FOLDER / article["image"]
            if image_path.exists():
                image_path.unlink()

        db.execute("DELETE FROM news WHERE id = ?", (news_id,))
        db.commit()

    flash("News article deleted.", "success")
    return redirect(url_for("admin_news"))


@app.errorhandler(413)
def too_large(_error):
    flash("The image is too large.", "error")
    return redirect(url_for("admin_news"))


app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
