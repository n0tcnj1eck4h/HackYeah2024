from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, unique=False, nullable=False)
    positive = db.Column(db.Boolean, unique=False, nullable=False)
    site_id = db.Column(db.Integer, nullable=False)


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String, unique=True, nullable=False)
    date_added = db.Column(db.DateTime, unique=False, nullable=False)

    krs = db.Column(db.String, unique=False, nullable=True)
    nip = db.Column(db.String, unique=False, nullable=True)
    org_name = db.Column(db.String, unique=False, nullable=True)
    active_vat = db.Column(db.Boolean, unique=False, nullable=True)
    domain_registration = db.Column(db.DateTime, unique=False, nullable=True)
    # comments = db.relationship("Comments", backref="site", lazy=True)
