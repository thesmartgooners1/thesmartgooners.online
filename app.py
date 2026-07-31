from flask import Flask, render_template, abort
from datetime import datetime

app = Flask(__name__)

ARTICLES = [
    {
        "id": 1,
        "title": "Premier League clubs prepare for the new season",
        "summary": "Managers are finalizing squads, tactics and preseason plans ahead of the opening fixtures.",
        "category": "Premier League",
        "image": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=1200&q=80",
        "author": "Football Desk",
        "date": "August 1, 2026",
        "featured": True,
        "content": [
            "Premier League clubs are entering the final stage of preseason preparation as managers assess fitness, tactics and squad depth.",
            "Supporters are watching transfer activity closely, while coaching teams focus on building consistency before competitive fixtures begin.",
            "The opening weeks may provide an early indication of which teams are ready to challenge at the top of the table."
        ]
    },
    {
        "id": 2,
        "title": "Transfer window: Five deals to watch",
        "summary": "Several leading clubs remain active as negotiations continue across Europe.",
        "category": "Transfers",
        "image": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=1200&q=80",
        "author": "Transfer Team",
        "date": "August 1, 2026",
        "featured": False,
        "content": [
            "The transfer market remains active, with clubs looking for late additions in attack, midfield and defence.",
            "Contract terms, medical checks and negotiations between clubs can all influence whether a deal is completed.",
            "Fans should rely on official club announcements before treating any reported transfer as confirmed."
        ]
    },
    {
        "id": 3,
        "title": "Champions League contenders strengthen squads",
        "summary": "Europe's biggest clubs are adding depth ahead of another demanding campaign.",
        "category": "Champions League",
        "image": "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?auto=format&fit=crop&w=1200&q=80",
        "author": "European Football",
        "date": "July 31, 2026",
        "featured": False,
        "content": [
            "Champions League contenders are balancing domestic ambitions with the demands of European competition.",
            "Squad depth is especially important because clubs may face multiple fixtures in a short period.",
            "Recruitment decisions made during preseason could have a major impact later in the campaign."
        ]
    },
    {
        "id": 4,
        "title": "Young players impress during preseason",
        "summary": "Academy prospects are making the most of opportunities with senior teams.",
        "category": "Youth",
        "image": "https://images.unsplash.com/photo-1517466787929-bc90951d0974?auto=format&fit=crop&w=1200&q=80",
        "author": "Academy Watch",
        "date": "July 31, 2026",
        "featured": False,
        "content": [
            "Preseason offers young players a valuable chance to train and play alongside established first-team professionals.",
            "Strong performances can help academy prospects earn more opportunities during the competitive season.",
            "Managers will also consider consistency, discipline and tactical understanding when assessing young talent."
        ]
    },
    {
        "id": 5,
        "title": "Tactical trends shaping modern football",
        "summary": "High pressing, flexible formations and quick transitions continue to influence elite teams.",
        "category": "Analysis",
        "image": "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?auto=format&fit=crop&w=1200&q=80",
        "author": "Tactics Lab",
        "date": "July 30, 2026",
        "featured": False,
        "content": [
            "Modern football teams often change shape depending on whether they have possession.",
            "Coaches increasingly value players who can perform multiple tactical roles and make quick decisions under pressure.",
            "The best tactical systems are adapted to the strengths of the squad rather than copied without adjustment."
        ]
    }
]

MATCHES = [
    {"home": "Arsenal", "away": "Chelsea", "time": "19:30", "status": "Upcoming"},
    {"home": "Liverpool", "away": "Manchester City", "time": "22:00", "status": "Upcoming"},
    {"home": "Barcelona", "away": "Real Madrid", "time": "01:30", "status": "Upcoming"},
]

@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

@app.route("/")
def home():
    featured = next((a for a in ARTICLES if a["featured"]), ARTICLES[0])
    latest = [a for a in ARTICLES if a["id"] != featured["id"]]
    return render_template("index.html", featured=featured, articles=latest, matches=MATCHES)

@app.route("/article/<int:article_id>")
def article(article_id):
    item = next((a for a in ARTICLES if a["id"] == article_id), None)
    if not item:
        abort(404)
    related = [a for a in ARTICLES if a["id"] != article_id][:3]
    return render_template("article.html", article=item, related=related)

@app.route("/category/<category>")
def category(category):
    items = [a for a in ARTICLES if a["category"].lower() == category.lower()]
    return render_template("category.html", category=category, articles=items)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
