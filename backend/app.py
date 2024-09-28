from datetime import datetime
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_mapping(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI="sqlite:///site.db",
)

db = SQLAlchemy()
from models import Site, Comment

db.init_app(app)

from scrapequeue import ScrapeQueue

queue = ScrapeQueue(app)
queue.start_thread()


with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.post("/api/site")
def add_site_to_queue():
    url = request.form.get("url", type=str)
    if url is None:
        return "Bad request", 400

    queue.push(url)
    return ""


@app.get("/api/site/<path:url>")
def check_task_status(url: str):
    task = queue.task_status(url)
    return {"state": task[0].name, "data": "data will be here eventually"}


@app.post("/api/site/<path:url>")
def comment(url: str):
    site = Site.query.filter_by(url=url).first()
    if site is None:
        return "Site not found", 404

    content = request.form.get("content", type=str)
    is_positive = request.form.get("positive", type=bool)
    if content is None or is_positive is None:
        return "Invalid request", 400

    new_comment = Comment(
        content=content,
        positive=is_positive,
        site_id=site.id,
    )

    db.session.add(new_comment)
    db.session.commit()

    return ""
