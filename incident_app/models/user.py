from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
from incident_app import db, login_manager

# Users -> Users (M:N)
supervises = db.Table('supervises',
                      db.Column('supervisor', db.ForeignKey('user.id')),
                      db.Column('supervisee', db.ForeignKey('user.id')),
                      )

assisting = db.Table('assisting',
                     db.Column('officer', db.ForeignKey('user.id')),
                     db.Column('incident', db.ForeignKey('incident.id')))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    incidents = db.relationship('Incident', backref='creator',
                                lazy='dynamic')
    # assists = db.relationship('Incident', backref='assisting', lazy='dynamic', foreign_keys=[id])
    assists = db.relationship('Incident',
                              secondary=assisting,
                              back_populates='secondary_officers')
    supervising = db.relationship(
        'User', secondary=supervises,
        primaryjoin=(getattr(supervises.c, 'supervisor') == id),
        secondaryjoin=(getattr(supervises.c, 'supervisee') == id),
        backref='supervised_by', lazy='dynamic'
    )

    def __repr__(self):
        return f'<User> -> Name: {self.name}; Role: {self.role}'  # noqa

    def __str__(self):
        return f"ID:{self.id} Name:{self.name}"

    def set_password(self, text: str):
        if self.password is None:
            self.password = pbkdf2_sha256.hash(text)
        else:
            if self.verify_password(text):
                raise ValueError('The new password matches the old password.')
            self.password = pbkdf2_sha256.hash(text)

    def verify_password(self, text: str):
        if pbkdf2_sha256.verify(text, self.password):
            return True
        else:
            return False

    def is_supervising(self, user):
        return self.supervising.filter(
            getattr(supervises.c, 'supervisor') == self.id,
            getattr(supervises.c, 'supervisee') == user.id
        ).count() > 0

    def add_supervisee(self, user):
        if not self.is_supervising(user):
            self.supervising.append(user)
            users = user.supervising.all()
            if users:
                for u in users:
                    if u not in self.supervising.all():
                        self.supervising.append(u)
            db.session.commit()

    def remove_supervisee(self, user):
        if self.is_supervising(user):
            self.supervising.remove(user)
            db.session.commit()

    def is_assisting(self, incident):
        if self.id == incident.officer:
            return True
        return incident in self.assists

    def add_assist(self, incident):
        if not self.is_assisting(incident):
            self.assists.append(incident)
            db.session.commit()

    def remove_assist(self, incident):
        if self.is_assisting(incident):
            self.assists.remove(incident)
            db.session.commit()
