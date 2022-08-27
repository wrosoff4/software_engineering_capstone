import unittest

from incident_app import db, app_factory
from incident_app.models.incident import Incident
from incident_app.models.user import User
from incident_app.models.vehicle import Vehicle


class VehicleModelCase(unittest.TestCase):
    def setUp(self):
        self.app = app_factory()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_vehicle(self):
        v1 = Vehicle(plate="ABC-1234", weight=6000, num_occupants=1,
                     make="Toyota", model="Corolla", color="Black")
        v2 = Vehicle(plate="DEF-5678", weight=7689, num_occupants=2,
                     make="Honda", model="Civic", color="White")
        db.session.add(v1)
        db.session.add(v2)
        q1 = Vehicle.query.filter_by(plate="ABC-1234").first()
        q2 = Vehicle.query.filter_by(plate="DEF-5678").first()
        self.assertEqual(v1, q1)
        self.assertEqual(v2, q2)

    def test_association(self):
        u1 = User(id=2345, name='Thing One', email='thing1@drsuess.com', role=1)  # noqa
        u1.set_password('asdfghg')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1, User.query.get(u1.id))
        i1 = Incident(officer=u1.id, location='Castle Hayne',
                      county='New Hanover', severity=2)
        i2 = Incident(officer=u1.id, severity=3)
        i3 = Incident(officer=u1.id, severity=2)
        db.session.add(i1)
        db.session.add(i2)
        db.session.add(i3)
        db.session.commit()
        self.assertEqual(i1, Incident.query.get(i1.id))  # noqa
        v1 = Vehicle(plate="ABC-1234", weight=6000, num_occupants=1,  # noqa
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
        v1.associate_incident(i1, data)
        v2.associate_incident(i2)
        v3.associate_incident(i2, data)
        i3.associate_vehicle(v3)
        self.assertFalse(v1.is_associated(i2))
        self.assertTrue(v1.is_associated(i1))
        self.assertTrue(v2.is_associated(i2))
        self.assertTrue(v3.is_associated(i2))
        self.assertEqual(1, len(i1.vehicles))
        self.assertEqual(2, len(i2.vehicles))
        v1.associate_incident(i2)
        self.assertTrue(v1.is_associated(i2))
        self.assertEqual(3, len(i2.vehicles))
        self.assertEqual(1, len(i1.vehicles))
        self.assertTrue(i1.is_associated(v1))
        self.assertTrue(i2.is_associated(v2))
        self.assertTrue(i2.is_associated(v3))
        self.assertTrue(i3.is_associated(v3))


if __name__ == '__main__':
    unittest.main(verbosity=2)
