import unittest

from incident_app import db, app_factory
from incident_app.models.incident import Incident
from incident_app.models.object import Object
from incident_app.models.user import User


class ObjectsModelTest(unittest.TestCase):
    def setUp(self):
        self.app = app_factory()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_relationship(self):
        u = User(id=6789, name='Thing Two', email='thing2@drsuess.com', role=1)
        u.set_password('thingone')
        db.session.add(u)
        db.session.commit()
        test_u = User.query.all()[0]
        self.assertEqual(u, test_u)
        i = Incident(severity=2, officer=u.id)
        db.session.add(i)
        db.session.commit()
        test_i = Incident.query.all()[0]
        self.assertEqual(i, test_i)
        o = Object(incident_id=i.id, is_ref1=True,
                   object_type='Tree')
        db.session.add(o)
        db.session.commit()
        test_o = Object.query.all()[0]
        self.assertEqual(o, test_o)
        self.assertEqual(1, len(test_i.objects.all()))
        o2 = Object(incident_id=i.id, is_ref2=True,
                    object_type='Guard Rail')
        db.session.add(o2)
        db.session.commit()
        test_o2 = Object.query.all()[1]
        self.assertEqual(o2, test_o2)
        self.assertEqual(2, len(test_i.objects.all()))
        self.assertEqual(test_i, test_o.incident)
        self.assertEqual(test_i, test_o2.incident)


if __name__ == '__main__':
    unittest.main(verbosity=2)
