from datetime import datetime

from incident_app import db
from incident_app.models.vehicle import AssociatedVehicle
from incident_app.models.user import assisting


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crash_sequence = db.Column(db.String(15), unique=True, nullable=True)
    date = db.Column(db.String(15), nullable=False, default=datetime.now().strftime('%m/%d/%Y'))
    time = db.Column(db.String(10), nullable=False, default=datetime.now().strftime('%H:%M'))
    county = db.Column(db.String(25))
    location = db.Column(db.String(25))
    severity = db.Column(db.Integer, nullable=False)
    num_vehicles = db.Column(db.Integer, nullable=False, default=1)
    num_pedestrians = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='Open')
    photos_taken = db.Column(db.Boolean, default=False)
    photographer = db.Column(db.String, nullable=True)
    # foreign key for incidents relationship
    officer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    secondary_officers = db.relationship('User',
                                         secondary=assisting,
                                         back_populates='assists')
    vehicles = db.relationship("AssociatedVehicle", back_populates='incident')
    objects = db.relationship('Object', backref='incident', lazy='dynamic')

    def associate_vehicle(self, vehicle, data=None):
        if not self.is_associated(vehicle):  # noqa
            if data:
                va = AssociatedVehicle(incident_id=self.id,
                                       vehicle_id=vehicle.id,
                                       damage=data[0], skid_before=data[1],
                                       skid_after=data[2], airbag_front=data[3],
                                       airbag_side=data[4])
                db.session.add(va)
            else:
                db.session.add(AssociatedVehicle(incident_id=self.id,
                                                 vehicle_id=vehicle.id))
            db.session.commit()

    def is_associated(self, vehicle):
        res = AssociatedVehicle.query.filter_by(incident_id=self.id, vehicle_id=vehicle.id).all()
        return len(res) > 0

    def secondaries_string(self):
        res = ''
        lst = self.secondary_officers
        if len(lst) == 0:
            return str(None)
        for i in range(len(lst)):
            if i < (len(lst) - 1):
                res += f"{lst[i].name}, "
            else:
                res += f"{lst[i].name}"
        return res

    def __repr__(self):
        return f'<Incident> -> ID: {self.id} ' \
               f'Officer: ({db.session.merge(self.creator)})'
