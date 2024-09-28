from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, unique=False, nullable=False)
    positive = db.Column(db.Boolean, unique=False, nullable=False)
    site_id = db.Column(db.Integer, nullable=False)


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    trust_score = db.Column(db.Integer, unique=False, nullable=False)
    date_added = db.Column(db.DateTime, unique=False, nullable=False)
    # comments = db.relationship("Comments", backref="site", lazy=True)
