from enum import unique
from application import db

class Anime(db.Model):
    anime_id = db.Column(db.Integer, primary_key = True)
    anime_name = db.Column(db.String(20))
    anime_desc = db.Column(db.String(100))
    anime_status = db.Column(db.String(4))
    released_date = db.Column(db.Date)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.uid'))
    def __str__(self):
        return f"{self.anime_status} {self.anime_name}: {self.anime_desc}. released on  {self.released_date}."

class User(db.Model):
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    animes = db.relationship('Anime', backref='user')
    def __str__(self):
        return f" {self.username},{self.uid}"