import unittest

from incident_app import app_factory, db
from incident_app.models.incident import Incident
from incident_app.models.user import User
from incident_app.models.vehicle import Vehicle, AssociatedVehicle


class VehicleAssociationTest(unittest.TestCase):
    def setUp(self):
        self.app = app_factory()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_add(self):
        u1 = User(id=2345, name='Thing One', email='thing1@drsuess.com', role=1)  # noqa
        u1.set_password('asdfghg')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1, User.query.get(u1.id))
        i1 = Incident(officer=u1.id, location='Castle Hayne',
                      county='New Hanover', severity=2)
        i2 = Incident(officer=u1.id, severity=3)
        db.session.add(i1)
        db.session.add(i2)
        db.session.commit()
        self.assertEqual(i1, Incident.query.get(i1.id))
        self.assertEqual(i2, Incident.query.get(i2.id))  # noqa
        v1 = Vehicle(plate="ABC-1234", weight=6000, num_occupants=1,
                     make="Toyota", model="Corolla", color="Black")
        v2 = Vehicle(plate="DEF-5678", weight=7689, num_occupants=2,
                     make="Honda", model="Civic", color="White")
        v3 = Vehicle(plate="JK-5678", weight=4568, num_occupants=1,
                     make="Mazda", model="Miada", color="Yellow")
        db.session.add(v1)
        db.session.add(v2)
        db.session.add(v3)
        db.session.commit()
        data = ['front left,front middle',
                32.5, 15.2, 1, 0]
        va1 = AssociatedVehicle(vehicle_id=v1.id, incident_id=i1.id,
                                damage=data[0], skid_before=data[1],
                                skid_after=data[2], airbag_front=data[3],
                                airbag_side=data[4])
        db.session.add(va1)
        db.session.commit()
        self.assertEqual(v1, va1.vehicle)
        self.assertEqual(v1.id, va1.vehicle_id)
        self.assertEqual(1, len(v1.incidents))
        self.assertEqual(i1, va1.incident)
        self.assertEqual(i1.id, va1.incident_id)
        self.assertEqual(1, len(i1.vehicles))
        self.assertEqual(v1, i1.vehicles[0].vehicle)
        self.assertEqual(i1, v1.incidents[0].incident)
