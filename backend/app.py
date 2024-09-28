from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from queue import ScrapeQueue


app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        CELERY_BROKER_URL="redis://localhost",
        RESULT_BACKEND="redis://localhost",
        TASK_IGNORE_RESULT=True,
    ),
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI="sqlite:///site.db",
)

db = SQLAlchemy()
db.init_app(app)

queue = ScrapeQueue()
queue.start_thread()


with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.post("/queue")
def add_site_to_queue():
    url = request.form.get("url", type=str)
    if url is None:
        return "Bad request", 400

    return {"task_id": result.id}
