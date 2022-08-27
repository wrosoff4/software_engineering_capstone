import unittest

from incident_app import app_factory, db
from incident_app.models.incident import Incident
from incident_app.models.user import User
from incident_app.workflow_manager import action_permission, draw_permission
from tests.unit.workflow_measure import test_list


# Created by Terrence Hernandez

# RUN TEST: Execute this file to conduct the unit test for the workflow_manager component


class Testing(unittest.TestCase):

    def setUp(self):
        self.app = app_factory()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_action_permission_trooper(self):
        # Create new TROOPER users
        t1 = User(id=1111, name="Trooper One", email="trooper_one@gmail.com", role=1)
        t2 = User(id=9999, name="Trooper Two", email="trooper_two@gmail.com", role=1)

        t1.set_password("trooperOne")
        t2.set_password("trooperTwo")

        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()

        # Create incidents to add to the db session
        inc1 = Incident(id=1, crash_sequence="20211110001B1", date="11/11/2021", time="19:01", county="Wake",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="Open", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc2 = Incident(id=2, crash_sequence="20211110002B1", date="11/11/2021", time="19:02", county="Hope",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc3 = Incident(id=3, crash_sequence="20211110003B1", date="11/11/2021", time="19:03", county="Brunswick",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc4 = Incident(id=4, crash_sequence="20211110004B1", date="11/11/2021", time="19:04", county="Onslow",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc5 = Incident(id=5, crash_sequence="20211110005B1", date="11/11/2021", time="19:05", county="Pender",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc6 = Incident(id=6, crash_sequence="20211110006B1", date="11/11/2021", time="19:06", county="Halfmoon",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc7 = Incident(id=7, crash_sequence="20211110007B1", date="11/11/2021", time="19:07", county="Sampson",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc8 = Incident(id=8, crash_sequence="20211110008B1", date="11/11/2021", time="19:08", county="Mars",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc9 = Incident(id=9, crash_sequence="20211110009B1", date="11/11/2021", time="19:09", county="Dutchess",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        # Add TROOPER 2 as assisting office to each incident
        t2.add_assist(inc1)
        t2.add_assist(inc2)
        t2.add_assist(inc3)
        t2.add_assist(inc4)
        t2.add_assist(inc5)
        t2.add_assist(inc6)
        t2.add_assist(inc7)
        t2.add_assist(inc8)
        t2.add_assist(inc9)
        db.session.commit()

        # Add Incidents to db session
        db.session.add(inc1)
        db.session.add(inc2)
        db.session.add(inc3)
        db.session.add(inc4)
        db.session.add(inc5)
        db.session.add(inc6)
        db.session.add(inc7)
        db.session.add(inc8)
        db.session.add(inc9)
        db.session.commit()

        # Query the db to get each incident
        i1 = Incident.query.filter_by(id=1).first()
        i2 = Incident.query.filter_by(id=2).first()
        i3 = Incident.query.filter_by(id=3).first()
        i4 = Incident.query.filter_by(id=4).first()
        i5 = Incident.query.filter_by(id=5).first()
        i6 = Incident.query.filter_by(id=6).first()
        i7 = Incident.query.filter_by(id=7).first()
        i8 = Incident.query.filter_by(id=8).first()
        i9 = Incident.query.filter_by(id=9).first()

        # Test that each incident is accurately in the db
        self.assertEqual(inc1, i1)
        self.assertEqual(inc2, i2)
        self.assertEqual(inc3, i3)
        self.assertEqual(inc4, i4)
        self.assertEqual(inc5, i5)
        self.assertEqual(inc6, i6)
        self.assertEqual(inc7, i7)
        self.assertEqual(inc8, i8)
        self.assertEqual(inc9, i9)

        # Testing of PRIMARY TROOPER viewing privileges
        self.assertEqual(action_permission(1111, "view", 1, 1111), True)
        self.assertEqual(action_permission(1111, "view", 2, 1111), True)
        self.assertEqual(action_permission(1111, "view", 3, 1111), False)
        self.assertEqual(action_permission(1111, "view", 4, 1111), True)
        self.assertEqual(action_permission(1111, "view", 5, 1111), True)
        self.assertEqual(action_permission(1111, "view", 6, 1111), True)
        self.assertEqual(action_permission(1111, "view", 7, 1111), False)
        self.assertEqual(action_permission(1111, "view", 8, 1111), True)
        self.assertEqual(action_permission(1111, "view", 9, 1111), True)
        self.assertEqual(action_permission(1111, "view", 0, 12), False)

        # Testing of ASSISTING TROOPER viewing privileges
        self.assertEqual(action_permission(9999, "view", 1, 1111), True)
        self.assertEqual(action_permission(9999, "view", 2, 1111), True)
        self.assertEqual(action_permission(9999, "view", 3, 1111), False)
        self.assertEqual(action_permission(9999, "view", 4, 1111), True)
        self.assertEqual(action_permission(9999, "view", 5, 1111), True)
        self.assertEqual(action_permission(9999, "view", 6, 1111), True)
        self.assertEqual(action_permission(9999, "view", 7, 1111), False)
        self.assertEqual(action_permission(9999, "view", 8, 1111), True)
        self.assertEqual(action_permission(9999, "view", 9, 1111), True)
        self.assertEqual(action_permission(9999, "view", 0, 12), False)

        # Testing of PRIMARY TROOPER editing privileges
        self.assertEqual(action_permission(1111, "edit", 1, 1111), True)
        self.assertEqual(action_permission(1111, "edit", 2, 1111), True)
        self.assertEqual(action_permission(1111, "edit", 3, 1111), False)
        self.assertEqual(action_permission(1111, "edit", 4, 1111), False)
        self.assertEqual(action_permission(1111, "edit", 5, 1111), True)
        self.assertEqual(action_permission(1111, "edit", 6, 1111), False)
        self.assertEqual(action_permission(1111, "edit", 7, 1111), False)
        self.assertEqual(action_permission(1111, "edit", 8, 1111), False)
        self.assertEqual(action_permission(1111, "edit", 9, 1111), True)
        self.assertEqual(action_permission(1111, "edit", 0, 12), False)

        # Testing of ASSISTING TROOPER editing privileges
        self.assertEqual(action_permission(9999, "edit", 1, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 2, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 3, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 4, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 5, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 6, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 7, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 8, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 9, 1111), False)
        self.assertEqual(action_permission(9999, "edit", 0, 12), False)

        # Testing of PRIMARY TROOPER printing privileges
        self.assertEqual(action_permission(1111, "print", 1, 1111), False)
        self.assertEqual(action_permission(1111, "print", 2, 1111), False)
        self.assertEqual(action_permission(1111, "print", 3, 1111), False)
        self.assertEqual(action_permission(1111, "print", 4, 1111), False)
        self.assertEqual(action_permission(1111, "print", 5, 1111), False)
        self.assertEqual(action_permission(1111, "print", 6, 1111), False)
        self.assertEqual(action_permission(1111, "print", 7, 1111), False)
        self.assertEqual(action_permission(1111, "print", 8, 1111), True)
        self.assertEqual(action_permission(1111, "print", 9, 1111), False)
        self.assertEqual(action_permission(1111, "print", 0, 12), False)

        # Testing of ASSISTING TROOPER printing privileges
        self.assertEqual(action_permission(9999, "print", 1, 1111), False)
        self.assertEqual(action_permission(9999, "print", 2, 1111), False)
        self.assertEqual(action_permission(9999, "print", 3, 1111), False)
        self.assertEqual(action_permission(9999, "print", 4, 1111), False)
        self.assertEqual(action_permission(9999, "print", 5, 1111), False)
        self.assertEqual(action_permission(9999, "print", 6, 1111), False)
        self.assertEqual(action_permission(9999, "print", 7, 1111), False)
        self.assertEqual(action_permission(9999, "print", 8, 1111), False)
        self.assertEqual(action_permission(9999, "print", 9, 1111), False)
        self.assertEqual(action_permission(9999, "print", 0, 12), False)

    def test_action_permission_supervisor(self):
        # Create new SUPERVISOR users
        s1 = User(id=2222, name="Supervisor One", email="supervisor_one@gmail.com", role=2)
        s2 = User(id=7777, name="Supervisor Two", email="supervisor_two@gmail.com", role=2)

        s1.set_password("supervisor_one")
        s2.set_password("supervisor_two")

        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        # Create incidents to add to the db session
        inc1 = Incident(id=1, crash_sequence="20211110001B1", date="11/11/2021", time="19:01", county="Wake",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="Open", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc2 = Incident(id=2, crash_sequence="20211110002B1", date="11/11/2021", time="19:02", county="Hope",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc3 = Incident(id=3, crash_sequence="20211110003B1", date="11/11/2021", time="19:03", county="Brunswick",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc4 = Incident(id=4, crash_sequence="20211110004B1", date="11/11/2021", time="19:04", county="Onslow",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc5 = Incident(id=5, crash_sequence="20211110005B1", date="11/11/2021", time="19:05", county="Pender",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc6 = Incident(id=6, crash_sequence="20211110006B1", date="11/11/2021", time="19:06", county="Halfmoon",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc7 = Incident(id=7, crash_sequence="20211110007B1", date="11/11/2021", time="19:07", county="Sampson",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc8 = Incident(id=8, crash_sequence="20211110008B1", date="11/11/2021", time="19:08", county="Mars",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc9 = Incident(id=9, crash_sequence="20211110009B1", date="11/11/2021", time="19:09", county="Dutchess",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        # Add SUPERVISOR 2 as assisting office for each incident
        s2.add_assist(inc1)
        s2.add_assist(inc2)
        s2.add_assist(inc3)
        s2.add_assist(inc4)
        s2.add_assist(inc5)
        s2.add_assist(inc6)
        s2.add_assist(inc7)
        s2.add_assist(inc8)
        s2.add_assist(inc9)
        db.session.commit()

        # Add Incidents to db session
        db.session.add(inc1)
        db.session.add(inc2)
        db.session.add(inc3)
        db.session.add(inc4)
        db.session.add(inc5)
        db.session.add(inc6)
        db.session.add(inc7)
        db.session.add(inc8)
        db.session.add(inc9)
        db.session.commit()

        # Query the db to get each incident
        i1 = Incident.query.filter_by(id=1).first()
        i2 = Incident.query.filter_by(id=2).first()
        i3 = Incident.query.filter_by(id=3).first()
        i4 = Incident.query.filter_by(id=4).first()
        i5 = Incident.query.filter_by(id=5).first()
        i6 = Incident.query.filter_by(id=6).first()
        i7 = Incident.query.filter_by(id=7).first()
        i8 = Incident.query.filter_by(id=8).first()
        i9 = Incident.query.filter_by(id=9).first()

        # Test that each incident is accurately in the db
        self.assertEqual(inc1, i1)
        self.assertEqual(inc2, i2)
        self.assertEqual(inc3, i3)
        self.assertEqual(inc4, i4)
        self.assertEqual(inc5, i5)
        self.assertEqual(inc6, i6)
        self.assertEqual(inc7, i7)
        self.assertEqual(inc8, i8)
        self.assertEqual(inc9, i9)

        # Testing of PRIMARY SUPERVISOR viewing privileges
        self.assertEqual(action_permission(2222, "view", 1, 1111), True)
        self.assertEqual(action_permission(2222, "view", 2, 1111), True)
        self.assertEqual(action_permission(2222, "view", 3, 1111), True)
        self.assertEqual(action_permission(2222, "view", 4, 1111), True)
        self.assertEqual(action_permission(2222, "view", 5, 1111), True)
        self.assertEqual(action_permission(2222, "view", 6, 1111), True)
        self.assertEqual(action_permission(2222, "view", 7, 1111), False)
        self.assertEqual(action_permission(2222, "view", 8, 1111), True)
        self.assertEqual(action_permission(2222, "view", 9, 1111), True)
        self.assertEqual(action_permission(2222, "view", 0, 12), False)

        # Testing of ASSISTING SUPERVISOR viewing privileges
        self.assertEqual(action_permission(7777, "view", 1, 1111), True)
        self.assertEqual(action_permission(7777, "view", 2, 1111), True)
        self.assertEqual(action_permission(7777, "view", 3, 1111), True)
        self.assertEqual(action_permission(7777, "view", 4, 1111), True)
        self.assertEqual(action_permission(7777, "view", 5, 1111), True)
        self.assertEqual(action_permission(7777, "view", 6, 1111), True)
        self.assertEqual(action_permission(7777, "view", 7, 1111), False)
        self.assertEqual(action_permission(7777, "view", 8, 1111), True)
        self.assertEqual(action_permission(7777, "view", 9, 1111), True)
        self.assertEqual(action_permission(7777, "view", 0, 12), False)

        # Testing of PRIMARY SUPERVISOR editing privileges
        self.assertEqual(action_permission(2222, "edit", 1, 1111), False)
        self.assertEqual(action_permission(2222, "edit", 2, 1111), False)
        self.assertEqual(action_permission(2222, "edit", 3, 1111), True)
        self.assertEqual(action_permission(2222, "edit", 4, 1111), True)
        self.assertEqual(action_permission(2222, "edit", 5, 1111), True)
        self.assertEqual(action_permission(2222, "edit", 6, 1111), True)
        self.assertEqual(action_permission(2222, "edit", 7, 1111), False)
        self.assertEqual(action_permission(2222, "edit", 8, 1111), False)
        self.assertEqual(action_permission(2222, "edit", 9, 1111), True)
        self.assertEqual(action_permission(2222, "edit", 0, 12), False)

        # Testing of ASSISTING SUPERVISOR editing privileges
        self.assertEqual(action_permission(7777, "edit", 1, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 2, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 3, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 4, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 5, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 6, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 7, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 8, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 9, 1111), False)
        self.assertEqual(action_permission(7777, "edit", 0, 12), False)

        # Testing of PRIMARY SUPERVISOR privileges
        self.assertEqual(action_permission(2222, "print", 1, 1111), True)
        self.assertEqual(action_permission(2222, "print", 2, 1111), True)
        self.assertEqual(action_permission(2222, "print", 3, 1111), True)
        self.assertEqual(action_permission(2222, "print", 4, 1111), True)
        self.assertEqual(action_permission(2222, "print", 5, 1111), True)
        self.assertEqual(action_permission(2222, "print", 6, 1111), True)
        self.assertEqual(action_permission(2222, "print", 7, 1111), False)
        self.assertEqual(action_permission(2222, "print", 8, 1111), True)
        self.assertEqual(action_permission(2222, "print", 9, 1111), True)
        self.assertEqual(action_permission(2222, "print", 0, 12), False)

        # Testing of ASSISTING SUPERVISOR printing privileges
        self.assertEqual(action_permission(7777, "print", 1, 1111), False)
        self.assertEqual(action_permission(7777, "print", 2, 1111), False)
        self.assertEqual(action_permission(7777, "print", 3, 1111), False)
        self.assertEqual(action_permission(7777, "print", 4, 1111), False)
        self.assertEqual(action_permission(7777, "print", 5, 1111), False)
        self.assertEqual(action_permission(7777, "print", 6, 1111), False)
        self.assertEqual(action_permission(7777, "print", 7, 1111), False)
        self.assertEqual(action_permission(7777, "print", 8, 1111), False)
        self.assertEqual(action_permission(7777, "print", 9, 1111), False)
        self.assertEqual(action_permission(7777, "print", 0, 12), False)

    def testing_action_permission_other(self):
        # Create new OTHER user
        o1 = User(id=3333, name="other One", email="other_other@gmail.com", role=3)
        o1.set_password("other_one")
        db.session.add(o1)
        db.session.commit()

        # Create incidents to add to the db session
        inc1 = Incident(id=1, crash_sequence="20211110001B1", date="11/11/2021", time="19:01", county="Wake",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="Open", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc2 = Incident(id=2, crash_sequence="20211110002B1", date="11/11/2021", time="19:02", county="Hope",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc3 = Incident(id=3, crash_sequence="20211110003B1", date="11/11/2021", time="19:03", county="Brunswick",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc4 = Incident(id=4, crash_sequence="20211110004B1", date="11/11/2021", time="19:04", county="Onslow",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc5 = Incident(id=5, crash_sequence="20211110005B1", date="11/11/2021", time="19:05", county="Pender",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc6 = Incident(id=6, crash_sequence="20211110006B1", date="11/11/2021", time="19:06", county="Halfmoon",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc7 = Incident(id=7, crash_sequence="20211110007B1", date="11/11/2021", time="19:07", county="Sampson",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc8 = Incident(id=8, crash_sequence="20211110008B1", date="11/11/2021", time="19:08", county="Mars",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc9 = Incident(id=9, crash_sequence="20211110009B1", date="11/11/2021", time="19:09", county="Dutchess",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        # Add Incidents to db session
        db.session.add(inc1)
        db.session.add(inc2)
        db.session.add(inc3)
        db.session.add(inc4)
        db.session.add(inc5)
        db.session.add(inc6)
        db.session.add(inc7)
        db.session.add(inc8)
        db.session.add(inc9)
        db.session.commit()

        # Query the db to get each incident
        i1 = Incident.query.filter_by(id=1).first()
        i2 = Incident.query.filter_by(id=2).first()
        i3 = Incident.query.filter_by(id=3).first()
        i4 = Incident.query.filter_by(id=4).first()
        i5 = Incident.query.filter_by(id=5).first()
        i6 = Incident.query.filter_by(id=6).first()
        i7 = Incident.query.filter_by(id=7).first()
        i8 = Incident.query.filter_by(id=8).first()
        i9 = Incident.query.filter_by(id=9).first()

        # Test that each incident is accurately in the db
        self.assertEqual(inc1, i1)
        self.assertEqual(inc2, i2)
        self.assertEqual(inc3, i3)
        self.assertEqual(inc4, i4)
        self.assertEqual(inc5, i5)
        self.assertEqual(inc6, i6)
        self.assertEqual(inc7, i7)
        self.assertEqual(inc8, i8)
        self.assertEqual(inc9, i9)

        # Testing of OTHER viewing privileges
        for i in range(1, 11):
            self.assertEqual(action_permission(3333, "view", i, 1111), False)

        # Testing of OTHER editing privileges
        for j in range(1, 11):
            self.assertEqual(action_permission(3333, "edit", j, 1111), False)

        # Testing of OTHER printing privileges
        for k in range(1, 11):
            self.assertEqual(action_permission(3333, "print", k, 1111), False)

    def test_draw_permission_trooper(self):
        # Create new TROOPER users
        td1 = User(id=1111, name="Trooper One", email="trooper_one@gmail.com", role=1)  # noqa
        td2 = User(id=3333, name="Trooper Two", email="trooper_two@gmail.com", role=1)  # noqa

        td1.set_password("trooperOne")
        td2.set_password("trooperTwo")

        db.session.add(td1)
        db.session.add(td2)
        db.session.commit()

        # Create incidents to add to the db session
        inc1 = Incident(id=1, crash_sequence="20211110001B1", date="11/11/2021", time="19:01", county="Wake",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="Open", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc2 = Incident(id=2, crash_sequence="20211110002B1", date="11/11/2021", time="19:02", county="Hope",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc3 = Incident(id=3, crash_sequence="20211110003B1", date="11/11/2021", time="19:03", county="Brunswick",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc4 = Incident(id=4, crash_sequence="20211110004B1", date="11/11/2021", time="19:04", county="Onslow",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc5 = Incident(id=5, crash_sequence="20211110005B1", date="11/11/2021", time="19:05", county="Pender",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc6 = Incident(id=6, crash_sequence="20211110006B1", date="11/11/2021", time="19:06", county="Halfmoon",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc7 = Incident(id=7, crash_sequence="20211110007B1", date="11/11/2021", time="19:07", county="Sampson",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc8 = Incident(id=8, crash_sequence="20211110008B1", date="11/11/2021", time="19:08", county="Mars",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc9 = Incident(id=9, crash_sequence="20211110009B1", date="11/11/2021", time="19:09", county="Dutchess",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        # Add TROOPER 2 as assisting office to each incident
        td2.add_assist(inc1)
        td2.add_assist(inc2)
        td2.add_assist(inc3)
        td2.add_assist(inc4)
        td2.add_assist(inc5)
        td2.add_assist(inc6)
        td2.add_assist(inc7)
        td2.add_assist(inc8)
        td2.add_assist(inc9)
        db.session.commit()

        # Add incidents to db session
        db.session.add(inc1)
        db.session.add(inc2)
        db.session.add(inc3)
        db.session.add(inc4)
        db.session.add(inc5)
        db.session.add(inc6)
        db.session.add(inc7)
        db.session.add(inc8)
        db.session.add(inc9)
        db.session.commit()

        # Query the db to get each incident
        i1 = Incident.query.filter_by(id=1).first()
        i2 = Incident.query.filter_by(id=2).first()
        i3 = Incident.query.filter_by(id=3).first()
        i4 = Incident.query.filter_by(id=4).first()
        i5 = Incident.query.filter_by(id=5).first()
        i6 = Incident.query.filter_by(id=6).first()
        i7 = Incident.query.filter_by(id=7).first()
        i8 = Incident.query.filter_by(id=8).first()
        i9 = Incident.query.filter_by(id=9).first()

        # Test that each incident is accurately in the db
        self.assertEqual(inc1, i1)
        self.assertEqual(inc2, i2)
        self.assertEqual(inc3, i3)
        self.assertEqual(inc4, i4)
        self.assertEqual(inc5, i5)
        self.assertEqual(inc6, i6)
        self.assertEqual(inc7, i7)
        self.assertEqual(inc8, i8)
        self.assertEqual(inc9, i9)

        m = test_list()

        self.assertEqual(test_list(), [
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': -1, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (-1, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, -1), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (-1, -1), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(-1, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, -1), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(-1, -1), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (-1, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, -1)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (-1, -1)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(-1, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, -1), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(-1, -1), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (-1, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, -1)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (-1, -1)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(-1, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, -1), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(-1, -1), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (-1, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, -1), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (-1, -1), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (-1, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, -1), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (-1, -1), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (-1, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, -1)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (-1, -1)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (-1, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, -1)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (-1, -1)},
            {'rp1rp2': -1, 'body': (-1, -1), 'left_skid': [(-1, -1), (-1, -1)], 'right_skid': [(-1, -1), (-1, -1)],
             'car': [(-1, -1), (-1, -1), (-1, -1), (-1, -1)], 'aoi': (-1, -1)}]
                         )

        # Test PRIMARY TROOPER draw privileges given ALL VALID DATA
        self.assertEqual(draw_permission(1111, "draw", 1, 1111, m[0]), True)
        self.assertEqual(draw_permission(1111, "draw", 2, 1111, m[0]), True)
        self.assertEqual(draw_permission(1111, "draw", 3, 1111, m[0]), False)
        self.assertEqual(draw_permission(1111, "draw", 4, 1111, m[0]), False)
        self.assertEqual(draw_permission(1111, "draw", 5, 1111, m[0]), True)
        self.assertEqual(draw_permission(1111, "draw", 6, 1111, m[0]), False)
        self.assertEqual(draw_permission(1111, "draw", 7, 1111, m[0]), False)
        self.assertEqual(draw_permission(1111, "draw", 8, 1111, m[0]), False)
        self.assertEqual(draw_permission(1111, "draw", 9, 1111, m[0]), True)
        self.assertEqual(draw_permission(1111, "draw", 0, 12, m[0]), False)

        # Test ASSISTING TROOPER draw privileges given ALL VALID DATA
        self.assertEqual(draw_permission(3333, "draw", 1, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 2, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 3, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 4, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 5, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 6, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 7, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 8, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 9, 1111, m[0]), False)
        self.assertEqual(draw_permission(3333, "draw", 0, 12, m[0]), False)

        # Test PRIMARY TROOPER draw privileges given BAD DATA IN VARYING DEGREES
        for p in range(1, 32):
            for a in range(1, 11):
                self.assertEqual(draw_permission(1111, "draw", a, 1111, m[p]), False)

        # Test ASSISTING TROOPER draw privileges given BAD DATA IN VARYING DEGREES
        for q in range(1, 32):
            for b in range(1, 11):
                self.assertEqual(draw_permission(3333, "draw", b, 1111, m[q]), False)

    def test_draw_permission_supervisor(self):
        # Create new SUPERVISOR users
        sd1 = User(id=2222, name="Supervisor One", email="supervisor_one@gmail.com", role=2)
        sd2 = User(id=7777, name="Supervisor Two", email="supervisor_two@gmail.com", role=2)

        sd1.set_password("supervisorOne")
        sd2.set_password("supervisorTwo")

        db.session.add(sd1)
        db.session.add(sd2)
        db.session.commit()

        # Create incidents to add to the db session
        inc1 = Incident(id=1, crash_sequence="20211110001B1", date="11/11/2021", time="19:01", county="Wake",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="Open", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc2 = Incident(id=2, crash_sequence="20211110002B1", date="11/11/2021", time="19:02", county="Hope",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc3 = Incident(id=3, crash_sequence="20211110003B1", date="11/11/2021", time="19:03", county="Brunswick",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc4 = Incident(id=4, crash_sequence="20211110004B1", date="11/11/2021", time="19:04", county="Onslow",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc5 = Incident(id=5, crash_sequence="20211110005B1", date="11/11/2021", time="19:05", county="Pender",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc6 = Incident(id=6, crash_sequence="20211110006B1", date="11/11/2021", time="19:06", county="Halfmoon",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc7 = Incident(id=7, crash_sequence="20211110007B1", date="11/11/2021", time="19:07", county="Sampson",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc8 = Incident(id=8, crash_sequence="20211110008B1", date="11/11/2021", time="19:08", county="Mars",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc9 = Incident(id=9, crash_sequence="20211110009B1", date="11/11/2021", time="19:09", county="Dutchess",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        # Add SUPERVISOR 2 as assisting office to each incident
        sd2.add_assist(inc1)
        sd2.add_assist(inc2)
        sd2.add_assist(inc3)
        sd2.add_assist(inc4)
        sd2.add_assist(inc5)
        sd2.add_assist(inc6)
        sd2.add_assist(inc7)
        sd2.add_assist(inc8)
        sd2.add_assist(inc9)
        db.session.commit()

        # Add incidents to db session
        db.session.add(inc1)
        db.session.add(inc2)
        db.session.add(inc3)
        db.session.add(inc4)
        db.session.add(inc5)
        db.session.add(inc6)
        db.session.add(inc7)
        db.session.add(inc8)
        db.session.add(inc9)
        db.session.commit()

        # Query the db to get each incident
        i1 = Incident.query.filter_by(id=1).first()
        i2 = Incident.query.filter_by(id=2).first()
        i3 = Incident.query.filter_by(id=3).first()
        i4 = Incident.query.filter_by(id=4).first()
        i5 = Incident.query.filter_by(id=5).first()
        i6 = Incident.query.filter_by(id=6).first()
        i7 = Incident.query.filter_by(id=7).first()
        i8 = Incident.query.filter_by(id=8).first()
        i9 = Incident.query.filter_by(id=9).first()

        # Test that each incident is accurately in the db
        self.assertEqual(inc1, i1)
        self.assertEqual(inc2, i2)
        self.assertEqual(inc3, i3)
        self.assertEqual(inc4, i4)
        self.assertEqual(inc5, i5)
        self.assertEqual(inc6, i6)
        self.assertEqual(inc7, i7)
        self.assertEqual(inc8, i8)
        self.assertEqual(inc9, i9)

        m = test_list()

        self.assertEqual(test_list(), [
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': -1, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (-1, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, -1), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (-1, -1), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(-1, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, -1), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(-1, -1), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (-1, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, -1)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (-1, -1)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(-1, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, -1), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(-1, -1), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (-1, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, -1)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (-1, -1)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(-1, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, -1), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(-1, -1), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (-1, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, -1), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (-1, -1), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (-1, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, -1), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (-1, -1), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (-1, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, -1)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (-1, -1)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (-1, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, -1)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (-1, -1)},
            {'rp1rp2': -1, 'body': (-1, -1), 'left_skid': [(-1, -1), (-1, -1)], 'right_skid': [(-1, -1), (-1, -1)],
             'car': [(-1, -1), (-1, -1), (-1, -1), (-1, -1)], 'aoi': (-1, -1)}]
                         )

        # Test PRIMARY SUPERVISOR draw privileges given ALL VALID DATA
        self.assertEqual(draw_permission(2222, "draw", 1, 1111, m[0]), False)
        self.assertEqual(draw_permission(2222, "draw", 2, 1111, m[0]), False)
        self.assertEqual(draw_permission(2222, "draw", 3, 1111, m[0]), True)
        self.assertEqual(draw_permission(2222, "draw", 4, 1111, m[0]), False)
        self.assertEqual(draw_permission(2222, "draw", 5, 1111, m[0]), True)
        self.assertEqual(draw_permission(2222, "draw", 6, 1111, m[0]), True)
        self.assertEqual(draw_permission(2222, "draw", 7, 1111, m[0]), False)
        self.assertEqual(draw_permission(2222, "draw", 8, 1111, m[0]), False)
        self.assertEqual(draw_permission(2222, "draw", 9, 1111, m[0]), True)
        self.assertEqual(draw_permission(2222, "draw", 0, 12, m[0]), False)

        # Test ASSISTING SUPERVISOR draw privileges given ALL VALID DATA
        self.assertEqual(draw_permission(7777, "draw", 1, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 2, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 3, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 4, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 5, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 6, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 7, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 8, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 9, 1111, m[0]), False)
        self.assertEqual(draw_permission(7777, "draw", 0, 12, m[0]), False)

        # Test PRIMARY SUPERVISOR draw privileges given BAD DATA IN VARYING DEGREES
        for p in range(1, 32):
            for a in range(1, 11):
                self.assertEqual(draw_permission(2222, "draw", a, 1111, m[p]), False)

        # Test ASSISTING SUPERVISOR draw privileges given BAD DATA IN VARYING DEGREES
        for q in range(1, 32):
            for b in range(1, 11):
                self.assertEqual(draw_permission(7777, "draw", b, 1111, m[q]), False)

    def test_draw_permission_other(self):
        # Create new OTHER user
        od1 = User(id=3333, name="other One", email="other_other@gmail.com", role=3)
        od1.set_password("other_one")
        db.session.add(od1)
        db.session.commit()

        # Create incidents to add to the db session
        inc1 = Incident(id=1, crash_sequence="20211110001B1", date="11/11/2021", time="19:01", county="Wake",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="Open", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc2 = Incident(id=2, crash_sequence="20211110002B1", date="11/11/2021", time="19:02", county="Hope",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc3 = Incident(id=3, crash_sequence="20211110003B1", date="11/11/2021", time="19:03", county="Brunswick",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underSuperReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc4 = Incident(id=4, crash_sequence="20211110004B1", date="11/11/2021", time="19:04", county="Onslow",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc5 = Incident(id=5, crash_sequence="20211110005B1", date="11/11/2021", time="19:05", county="Pender",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedBySuper", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc6 = Incident(id=6, crash_sequence="20211110006B1", date="11/11/2021", time="19:06", county="Halfmoon",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="pendingDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc7 = Incident(id=7, crash_sequence="20211110007B1", date="11/11/2021", time="19:07", county="Sampson",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="underDmvReview", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc8 = Incident(id=8, crash_sequence="20211110008B1", date="11/11/2021", time="19:08", county="Mars",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="approvedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        inc9 = Incident(id=9, crash_sequence="20211110009B1", date="11/11/2021", time="19:09", county="Dutchess",
                        severity=3, num_vehicles=1, num_pedestrians=0, status="rejectedByDmv", officer=1111,
                        photos_taken=True, photographer="Sam Smith")

        # Add Incidents to db session
        db.session.add(inc1)
        db.session.add(inc2)
        db.session.add(inc3)
        db.session.add(inc4)
        db.session.add(inc5)
        db.session.add(inc6)
        db.session.add(inc7)
        db.session.add(inc8)
        db.session.add(inc9)
        db.session.commit()

        # Query the db to get each incident
        i1 = Incident.query.filter_by(id=1).first()
        i2 = Incident.query.filter_by(id=2).first()
        i3 = Incident.query.filter_by(id=3).first()
        i4 = Incident.query.filter_by(id=4).first()
        i5 = Incident.query.filter_by(id=5).first()
        i6 = Incident.query.filter_by(id=6).first()
        i7 = Incident.query.filter_by(id=7).first()
        i8 = Incident.query.filter_by(id=8).first()
        i9 = Incident.query.filter_by(id=9).first()

        # Test that each incident is accurately in the db
        self.assertEqual(inc1, i1)
        self.assertEqual(inc2, i2)
        self.assertEqual(inc3, i3)
        self.assertEqual(inc4, i4)
        self.assertEqual(inc5, i5)
        self.assertEqual(inc6, i6)
        self.assertEqual(inc7, i7)
        self.assertEqual(inc8, i8)
        self.assertEqual(inc9, i9)

        m = test_list()

        self.assertEqual(test_list(), [
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': -1, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (-1, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, -1), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (-1, -1), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(-1, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, -1), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(-1, -1), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (-1, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, -1)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (-1, -1)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(-1, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, -1), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(-1, -1), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (-1, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, -1)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (-1, -1)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(-1, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, -1), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(-1, -1), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (-1, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, -1), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (-1, -1), (70.0, 70.0), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (-1, 70.0), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, -1), (20.0, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (-1, -1), (20.0, 100.0)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (-1, 100.0)], 'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, -1)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)], 'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (-1, -1)],
             'aoi': (70.0, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (-1, 50.0)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (70.0, -1)},
            {'rp1rp2': 100.0, 'body': (60.0, 60.0), 'left_skid': [(70.0, 78.0), (70.0, 88.0)],
             'right_skid': [(42.0, 80.0), (32.0, 90.0)],
             'car': [(28.0, 102.0), (32.0, 90.0), (70.0, 70.0), (20.0, 100.0)], 'aoi': (-1, -1)},
            {'rp1rp2': -1, 'body': (-1, -1), 'left_skid': [(-1, -1), (-1, -1)], 'right_skid': [(-1, -1), (-1, -1)],
             'car': [(-1, -1), (-1, -1), (-1, -1), (-1, -1)], 'aoi': (-1, -1)}]
                         )

        # Test OTHER draw privileges given ALL VALID DATA
        for s in range(1, 11):
            self.assertEqual(draw_permission(3333, "draw", s, 1111, m[0]), False)

        # Test OTHER draw privileges given INVALID DATA
        for s in range(1, 11):
            self.assertEqual(draw_permission(3333, "draw", s, 1111, m[1]), False)


if __name__ == '__main__':
    unittest.main(verbosity=6)