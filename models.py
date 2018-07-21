from app import db

class PocketEntry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, unique=True, nullable=False)
    url = db.Column(db.String(255), unique=True, nullable=False)
    thumbnail_url = db.Column(db.String(450))
    content_domain = db.Column(db.String(50))
    content_title = db.Column(db.String(150))
    content_excerpt = db.Column(db.String(400))
    created_date = db.Column(db.DateTime, nullable=False)
