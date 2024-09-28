from app import db
import sqlalchemy as sq


class SiteQueueItem(db.Model):
    id = sq.Column(sq.Integer, primary_key=True)
    url = sq.Column(sq.String, unique=False, nullable=False)
    date_added = sq.Column(sq.DateTime, unique=False, nullable=False)
    #
    # def __repr__(self):
    #     return f"ID : {self.id}, URL: {self.url}"
