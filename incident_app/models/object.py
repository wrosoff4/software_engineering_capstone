from incident_app import db


class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False)
    object_type = db.Column(db.String(25), nullable=False)
    is_ref1 = db.Column(db.Boolean, default=False, nullable=False)
    is_ref2 = db.Column(db.Boolean, default=False, nullable=False)
    north_or_rp1 = db.Column(db.Float, nullable=True, default=0)
    south_or_rp2 = db.Column(db.Float, nullable=True, default=0)
    east = db.Column(db.Float, nullable=True, default=0)
    west = db.Column(db.Float, nullable=True, default=0)
