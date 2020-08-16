from flask_sqlalchemy import SQLAlchemy
from extensions import db


class Team(db.Model):

    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Team {self.name}>'


class Result(db.Model):

    __tablename__ = 'result'
    stage = db.Column(db.String(50), nullable=False)
    home_team = db.Column(db.String(200), nullable=False)
    away_team = db.Column(db.String(200), nullable=False)
    home_score = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer, nullable=False)
    match_time = db.Column(db.DateTime, nullable=False)
    match_uuid = db.Column(db.String(200), primary_key=True, nullable=False)

    #home_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    #home_team = db.relationship('Team', backref=db.backref('team', lazy=True))
    #away_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    #away_team = db.relationship('Team', backref=db.backref('team', lazy=True))

    def __repr__(self):
        return f'<Result {self.match_uuid}>'
    
    def serialize(self):
        return {
            'match_uuid': self.match_uuid,
            'stage': self.stage,
            'home_team': self.home_team,
            'away_team': self.away_team,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'match_time': self.match_time,
        }
