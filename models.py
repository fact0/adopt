from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
DEFAULT_IMAGE = 'https://files.catbox.moe/oo5ikc.jpg'


def connect_db(app):
    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Pet Model"""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer)
    photo_url = db.Column(db.Text, default=DEFAULT_IMAGE)
    photo = db.Column(db.Text)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)
