from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# create discipline model: id, name


class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"<Discipline {self.name}>"


# create tournament model: id, name, date, discipline as foreign key , location, max_participants
class Tournament(db.Model):
    def __init__(self, id_tournament, name, date, location, discipline, status):
        self.id_tournament = id_tournament
        self.name = name
        self.date_only = date.strftime('%Y-%m-%d')
        self.time = date.strftime('%H:%M')
        self.location = location
        self.status = status
        self.discipline = discipline

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(80), unique=False, nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey(
        'discipline.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Tournament {self.name}>"


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey(
        'tournament.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    result = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return f"<Result {self.result}>"


class Player():
    def __init__(self, id_player, username, rank, score):
        self.id_player = id_player
        self.username = username
        self.rank = rank
        self.score = score

    def __repr__(self):
        return f"<Player {self.name}>"
