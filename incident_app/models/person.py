from incident_app import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), default='NC', nullable=False)
    pos = db.Column(db.String, nullable=True)
    seatbelt = db.Column(db.Boolean, default=True)
