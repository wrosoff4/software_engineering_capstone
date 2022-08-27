import unittest

from incident_app import app_factory, db
from incident_app.models.user import User
from incident_app.models.incident import Incident


class IncidentModelTest(unittest.TestCase):
    def setUp(self):
        self.app = app_factory()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_primary_relation(self):
        u1 = User(id=2345, name='Thing One', email='thing1@drsuess.com', role=1)  # noqa
        u1.set_password('asdfghg')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1, User.query.get(u1.id))
        i1 = Incident(officer=u1.id, location='Castle Hayne',
                      county='New Hanover', severity=2)
        db.session.add(i1)
        db.session.commit()
        self.assertEqual(2345, i1.officer)
        self.assertEqual(1, len(u1.incidents.all()))
        self.assertEqual(i1, u1.incidents.all()[0])

    def test_assisting_relation(self):
        u1 = User(id=2345, name='Thing One', email='thing1@drsuess.com', role=1)  # noqa
        u1.set_password('asdfghg')
        u2 = User(id=6789, name='Thing Two', email='thing2@drsuess.com', role=1)
        u2.set_password('asdfghh')
        u3 = User(id=1112, name='Thing Three', email='thing3@drsuess.com', role=2)
        u3.set_password('asdfghcdvh')
        u4 = User(id=1314, name='Thing Four', email='thing4@drsuess.com', role=2)
        u4.set_password('asdfghcdsdfvh')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()
        self.assertEqual(u1, User.query.get(u1.id))
        self.assertEqual(u2, User.query.get(u2.id))
        self.assertEqual(u3, User.query.get(u3.id))
        i1 = Incident(officer=u1.id, location='Castle Hayne',
                      county='New Hanover', severity=2)
        db.session.add(i1)
        db.session.commit()
        u2.assists.append(i1)
        self.assertEqual(1, len(i1.secondary_officers))
        self.assertEqual('Thing Two', i1.secondaries_string())
        i1.secondary_officers.append(u3)
        self.assertEqual(2, len(i1.secondary_officers))
        self.assertEqual(1, len(u3.assists))
        self.assertEqual('Thing Two, Thing Three', i1.secondaries_string())
        self.assertTrue(u3.is_assisting(i1))
        self.assertTrue(u2.is_assisting(i1))
        self.assertFalse(u4.is_assisting(i1))
        self.assertEqual(2, len(i1.secondary_officers))
        u4.add_assist(i1)
        self.assertEqual(3, len(i1.secondary_officers))
        u4.remove_assist(i1)
        self.assertEqual(2, len(i1.secondary_officers))
        self.assertFalse(u4.is_assisting(i1))
