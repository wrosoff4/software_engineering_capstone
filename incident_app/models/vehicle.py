from incident_app import db


class AssociatedVehicle(db.Model):
    incident_id = db.Column(db.ForeignKey('incident.id'), primary_key=True)
    vehicle_id = db.Column(db.ForeignKey('vehicle.id'), primary_key=True)
    damage = db.Column(db.String, default='')
    skid_before = db.Column(db.Float, default=0)
    skid_after = db.Column(db.Float, default=0)
    airbag_front = db.Column(db.Boolean, default=False)
    airbag_side = db.Column(db.Boolean, default=False)
    incident = db.relationship('Incident', back_populates='vehicles')
    vehicle = db.relationship('Vehicle', back_populates='incidents')


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), default='NC', nullable=False)
    plate = db.Column(db.String(10), nullable=False)
    num_occupants = db.Column(db.Integer, nullable=False, default=1)
    make = db.Column(db.String(25), nullable=False)
    model = db.Column(db.String(25), nullable=False)
    color = db.Column(db.String(25), nullable=False)
    weight = db.Column(db.Float)
    incidents = db.relationship("AssociatedVehicle", back_populates='vehicle')

    def __repr__(self):
        return f'<Vehicle> License:{self.state}/{self.plate}'

    def associate_incident(self, incident, data=None):
        if not self.is_associated(incident):  # noqa
            if data:
                va = AssociatedVehicle(incident_id=incident.id,
                                       vehicle_id=self.id,
                                       damage=data[0], skid_before=data[1],
                                       skid_after=data[2], airbag_front=data[3],
                                       airbag_side=data[4])
                db.session.add(va)
            else:
                db.session.add(AssociatedVehicle(incident_id=incident.id,
                                                 vehicle_id=self.id))
            db.session.commit()

    def is_associated(self, incident):
        res = AssociatedVehicle.query.filter_by(vehicle_id=self.id,
                                                incident_id=incident.id).all()
        return len(res) > 0
