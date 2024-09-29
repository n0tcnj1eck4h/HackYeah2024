from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse


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


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/")
def index_post():
    domain = request.form.get("domain", type=str)
    if domain is None:
        return "Bad request", 400

    queue.push(domain)
    return redirect("/site/" + domain)


@app.get("/site/<path:domain>")
def site(domain: str):
    site = Site.query.filter_by(domain=domain).first()
    if site is None:
        return "404", 404
    comments = Comment.query.filter_by(site_id=site.id).all()
    return render_template("results.html", site=site, comments=comments)


@app.post("/site/<path:domain>")
def post_comment(domain: str):
    content = request.form.get("content", type=str)
    if content is None:
        return "bad request", 400

    vote = request.form.get("xd", type=str)
    if vote not in ["unsafe", "safe", "unsure"]:
        return "bad request", 400

    site = Site.query.filter_by(domain=domain).first()
    if site is None:
        return "404", 404

    comment = Comment()
    comment.content = content
    comment.vote = vote
    comment.site_id = site.id
    db.session.add(comment)
    db.session.commit()
    return redirect("/site/" + domain)


# API ROUTES
# @app.post("/api/site")
# def add_site_to_queue():
#     url = request.form.get("url", type=str)
#     if url is None:
#         return "Bad request", 400
#
#     urlp = urlparse(url)
#     domain = urlp.netloc
#
#     queue.push(domain)
#     return "oki"
#
#
# @app.get("/api/site/<path:url>")
# def check_task_status(url: str):
#     task = queue.task_status(url)
#     return {"state": task[0].name, "data": "data will be here eventually"}
#
#
# @app.post("/api/site/<path:url>")
# def comment(url: str):
#     urlp = urlparse(url)
#     domain = urlp.netloc
#     site = Site.query.filter_by(domain=domain).first()
#     if site is None:
#         return "Site not found", 404
#
#     content = request.form.get("content", type=str)
#     is_positive = request.form.get("positive", type=bool)
#     if content is None or is_positive is None:
#         return "Invalid request", 400
#
#     new_comment = Comment()
#     new_comment.content = content
#     new_comment.positive = is_positive
#     new_comment.site_id = site.id
#
#     db.session.add(new_comment)
#     db.session.commit()
#
#     return "ok :)"
