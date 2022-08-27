import unittest

from incident_app import db, app_factory
from incident_app.models.user import User
from incident_app.user_management import add_user, get_user, remove_user


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = app_factory()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_hashing(self):
        u = User(name='Tester McGavin')
        password = 'alksdfjoiejlasdf09qr'
        u.set_password(password)
        self.assertFalse(u.verify_password('testPassword'))
        self.assertTrue(u.verify_password(password))
        with self.assertRaises(ValueError):
            u.set_password(password)

    def test_add_and_get(self):
        u1 = User(id=2345, name='Thing One', email='thing1@drsuess.com', role=1)
        u2 = User(id=6789, name='Thing Two', email='thing2@drsuess.com', role=1)
        u1.set_password('thingone')
        self.assertTrue(add_user(u1))
        self.assertTrue(get_user(u1.id) == u1)
        with self.assertRaises(ValueError):
            add_user(u2)
            get_user(u2.id)
            get_user(-1)
        u2.set_password('thingtwo')
        self.assertTrue(add_user(u2))
        self.assertFalse(get_user(u2.id) is None)
        self.assertTrue(get_user(u2.id) == u2)

    def test_remove(self):
        u1 = User(id=9876, name='Sam I Am', email='samiam@drsuess.com', role=1)
        u2 = User(id=5432, name='Guy Am I', email='guyami@drsuess.com', role=1)
        u1.set_password('aPassword')
        u2.set_password('bPassword')
        self.assertTrue(add_user(u1))
        with self.assertRaises(ValueError):
            remove_user(u2.id)
            remove_user(-1)
            remove_user(u1)
        self.assertTrue(add_user(u2))
        self.assertTrue(remove_user(u2.id))
        self.assertTrue(remove_user(u1.id))
        with self.assertRaises(ValueError):
            get_user(u1.id)
            get_user(u2.id)

    def test_supervising(self):
        u1 = User(id=9876, name='Sam I Am', email='samiam@drsuess.com', role=1, password='testing')
        u2 = User(id=5432, name='Guy Am I', email='guyami@drsuess.com', role=2, password='testing')
        u3 = User(id=1928, name='The Lorax', email='ispeakforthetrees@drsuess.com', role=1, password='testing')
        u4 = User(id=2837, name='Once-ler', email='thneeds@drsuess.com', role=2, password='testing')
        self.assertTrue(add_user(u1))
        self.assertTrue(add_user(u2))
        self.assertTrue(add_user(u3))
        self.assertTrue(add_user(u4))
        assert len(u1.supervising.all()) == 0
        assert len(u2.supervising.all()) == 0
        assert len(u3.supervising.all()) == 0
        assert len(u4.supervising.all()) == 0
        u2.add_supervisee(u1)
        u4.add_supervisee(u3)
        assert len(u2.supervising.all()) == 1
        assert len(u4.supervising.all()) == 1
        u4.add_supervisee(u2)
        self.assertListEqual(u4.supervising.all(), [u3, u2, u1])
        u4.remove_supervisee(u2)
        self.assertListEqual(u4.supervising.all(), [u3, u1])
        u4.add_supervisee(u2)
        self.assertListEqual(u4.supervising.all(), [u3, u1, u2])
        remove_user(u2.id)
        self.assertListEqual(u4.supervising.all(), [u3, u1])
        assert len(u1.supervising.all()) == 0
        assert len(u3.supervising.all()) == 0


if __name__ == '__main__':
    unittest.main(verbosity=2)
