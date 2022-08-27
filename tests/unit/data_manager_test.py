# Created by Andrew Davison
# Instructions to run unittest: Run main conditional at end of file
import unittest
from datetime import datetime

from incident_app import app, db, data_manager as dm
from incident_app.models.incident import Incident
from incident_app.models.object import Object


class DataManager(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_id(self):
        assert dm.create_id('20201019', 'A1') == '20201019001A1'
        assert dm.create_id('20201019', '19') == '2020101900119'
        with self.assertRaises(TypeError):
            dm.create_id(20201019, 'A2')  # noqa
            dm.create_id('20201019', 13)  ## noqa

    def test_create_new_incident(self):
        # tests validate_new_incident method as well
        i1 = Incident(date="09/30/2021", time="15:30", county="Transylvania",
                      num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                      status="Open", officer=1)  # Good incident
        i2 = Incident(date="02/292021", time="15:30", county="Gotham",
                      num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                      status="Open", officer=1)  # Bad date
        i3 = Incident(date="02/15/2021", time="15:30", county="Hazzard", num_vehicles=1, severity=1,
                      location="SR-1234", num_pedestrians=0, status="Open", officer=1)  # Good time
        i4 = Incident(date="09/31/2021", time="1530", county="Hope County",
                      num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                      status="Open", officer=1)  # Bad time
        i5 = Incident(date="01/20/2021", time=datetime.now().strftime("%H:%M"),
                      county="Derry", num_vehicles=1, severity=1, location="",
                      num_pedestrians=0, status="Open", officer=1)  # Good location
        i6 = Incident(date="05/25/2021", time=datetime.now().strftime("%H:%M"), county="Haddonfield",
                      num_vehicles=1, severity=1, location="Rocky Horror Picture Show", num_pedestrians=0,
                      status="Open", officer=1)  # Bad location
        i7 = Incident(date="04/23/2021", time=datetime.now().strftime("%H:%M"), county="New Hanover",
                      num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                      status="Open", officer=1)  # Good number of vehicles
        i8 = Incident(date="03/20/2021", time=datetime.now().strftime("%H:%M"), county="Duplin", num_vehicles=0,
                      severity=1, location="SR-1234", num_pedestrians=0, status="Open", officer=1)  # Bad num_vehicles
        i9 = Incident(date="05/10/2021", time=datetime.now().strftime("%H:%M"), county="Onslow", num_vehicles=1,
                      severity=1, location="SR-1234", num_pedestrians=0, status="Open", officer=1)  # Good severity
        i10 = Incident(date="12/24/2020", time=datetime.now().strftime("%H:%M"), county="Transylvania",
                       num_vehicles=1, severity=0, location="SR-1234", num_pedestrians=0,
                       status="Open", officer=1)  # Bad severity
        i11 = Incident(date="11/01/2021", time=datetime.now().strftime("%H:%M"), county="", num_vehicles=1,
                       severity=1, location="SR-1234", num_pedestrians=0, status="Open", officer=1)  # Good County
        i12 = Incident(date="12/25/2020", time=datetime.now().strftime("%H:%M"), county="Miami-Dade",
                       num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0, status="Open",
                       officer=1)  # Bad County
        assert dm.create_new_incident(i1) is None
        i1.date = "01/15/2021"
        assert dm.create_new_incident(i1) is None
        i1.date = "12/15/2020"
        assert dm.create_new_incident(i1) is None
        i1.date = "02/28/2021"
        assert dm.create_new_incident(i1) is None
        i1.date = "04/30/2021"
        assert dm.create_new_incident(i1) is None
        i1.date = "08/31/2021"
        assert dm.create_new_incident(i1) is None
        i1.date = "12/31/2020"
        assert dm.create_new_incident(i1) is None
        i1.date = datetime.now().strftime("%m/%d/%Y")
        assert dm.create_new_incident(i1) is None
        assert dm.create_new_incident(i3) is None
        i3.time = "00:15"
        assert dm.create_new_incident(i3) is None
        i3.time = "23:15"
        assert dm.create_new_incident(i3) is None
        i3.time = "23:00"
        assert dm.create_new_incident(i3) is None
        i3.time = "23:59"
        assert dm.create_new_incident(i3) is None
        assert dm.create_new_incident(i5) is None
        i5.location = "SR-1234"
        assert dm.create_new_incident(i5) is None
        i5.location = "RockyHorrorPictureShow-1"
        assert dm.create_new_incident(i7) is None
        i7.num_vehicles = 999
        assert dm.create_new_incident(i7) is None
        assert dm.create_new_incident(i9) is None
        i9.severity = 3
        assert dm.create_new_incident(i9) is None
        assert dm.create_new_incident(i11) is None
        i11.county = "New Hanover"
        assert dm.create_new_incident(i11) is None
        with self.assertRaises(AttributeError):
            dm.create_new_incident(i2)
            i2.date = "02/29/20/21"
            dm.create_new_incident(i2)
            i2.date = "00/29/2021"
            dm.create_new_incident(i2)
            i2.date = "13/29/2020"
            dm.create_new_incident(i2)
            i2.date = "02/29/2021"
            dm.create_new_incident(i2)
            i2.date = "04/31/2021"
            dm.create_new_incident(i2)
            i2.date = "02/29/2020"
            dm.create_new_incident(i2)
            i2.date = "12/31/2021"
            dm.create_new_incident(i2)
            dm.create_new_incident(i4)
            i4.time = "1:5:30"
            dm.create_new_incident(i4)
            i4.time = "-1:30"
            dm.create_new_incident(i4)
            i4.time = "24:30"
            dm.create_new_incident(i4)
            i4.time = "15:-01"
            dm.create_new_incident(i4)
            i4.time = "15:60"
            dm.create_new_incident(i4)
            dm.create_new_incident(i6)
            dm.create_new_incident(i8)
            dm.create_new_incident(i10)
            i10.severity = 4
            dm.create_new_incident(i10)
            dm.create_new_incident(i12)

    def test_get_calculations(self):
        incident_id = '20211024003A2'
        measurements = {'force': 30.32,
                        'sled_weight': 230,
                        'total_weight': 3674,
                        'skid_start_distance': 30,
                        'skid_end_distance': 15,
                        'skid_total_distance': 45}
        result = {'drag_factor': 0.13,
                  'start_velocity': 19.55,
                  'skid_velocity': 15.96,
                  'impact_velocity': 11.28,
                  'time_of_skid': 4.60,
                  'kinetic_energy': 14529.87,
                  'start_speed': 13.33,
                  'skid_speed': 10.89,
                  'impact_speed': 7.70}
        assert dm.get_calculations(incident_id, measurements) == result
        with self.assertRaises(TypeError):
            measurements = {'force': '30.32',
                            'sled_weight': 230,
                            'total_weight': 3674,
                            'skid_start_distance': 30,
                            'skid_end_distance': 15,
                            'skid_total_distance': 45}
            dm.get_calculations(incident_id, measurements)

    def test_get_measurements(self):
        db.session.add(Object(id=1, incident_id=1, object_type='unit 1 begin skid', is_ref1=False, is_ref2=False,
                              north_or_rp1=53.1, south_or_rp2=12.2, east=0, west=0))
        db.session.add(Object(id=2, incident_id=1, object_type='aoi', is_ref1=False, is_ref2=False,
                              north_or_rp1=39, south_or_rp2=28.1, east=0, west=0))
        db.session.add(Object(id=3, incident_id=1, object_type='unit 1 rear right tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=26.8, south_or_rp2=41.1, east=0, west=0))
        db.session.add(Object(id=4, incident_id=1, object_type='unit 1 front right tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=27, south_or_rp2=44.7, east=0, west=0))
        db.session.add(Object(id=5, incident_id=1, object_type='unit 1 rear left tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=29.2, south_or_rp2=40.2, east=0, west=0))
        db.session.add(Object(id=6, incident_id=1, object_type='unit 1 front left tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=30.3, south_or_rp2=45.9, east=0, west=0))
        db.session.add(Object(id=7, incident_id=1, object_type='unit 2 head', is_ref1=False, is_ref2=False,
                              north_or_rp1=32.1, south_or_rp2=50.1, east=0, west=0))
        db.session.add(Object(id=8, incident_id=1, object_type='unit 2 torso', is_ref1=False, is_ref2=False,
                              north_or_rp1=33.3, south_or_rp2=49.8, east=0, west=0))
        db.session.add(Object(id=9, incident_id=1, object_type='rp2', is_ref1=False, is_ref2=True,
                              north_or_rp1=55.7, south_or_rp2=0, east=0, west=0))
        db.session.add(Object(id=10, incident_id=1, object_type='rp1', is_ref1=True, is_ref2=False,
                              north_or_rp1=0, south_or_rp2=0, east=0, west=0))
        db.session.add(Object(id=11, incident_id=1, object_type='unit 3 rear right tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=41.1, south_or_rp2=26.8, east=0, west=0))
        db.session.add(Object(id=12, incident_id=1, object_type='unit 3 front right tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=44.7, south_or_rp2=27, east=0, west=0))
        db.session.add(Object(id=13, incident_id=1, object_type='unit 3 rear left tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=40.2, south_or_rp2=29.2, east=0, west=0))
        db.session.add(Object(id=14, incident_id=1, object_type='unit 3 front left tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=45.9, south_or_rp2=30.3, east=0, west=0))
        db.session.add(Object(id=15, incident_id=2, object_type='unit 1 begin skid', is_ref1=False, is_ref2=False,
                              north_or_rp1=53.1, south_or_rp2=12.2, east=0, west=0))
        db.session.add(Object(id=16, incident_id=2, object_type='aoi', is_ref1=False, is_ref2=False,
                              north_or_rp1=39, south_or_rp2=28.1, east=0, west=0))
        db.session.add(Object(id=17, incident_id=2, object_type='unit 1 rear right tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=26.8, south_or_rp2=41.1, east=0, west=0))
        db.session.add(Object(id=18, incident_id=2, object_type='unit 1 front right tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=27, south_or_rp2=44.7, east=0, west=0))
        db.session.add(Object(id=19, incident_id=2, object_type='unit 1 rear left tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=29.2, south_or_rp2=40.2, east=0, west=0))
        db.session.add(Object(id=20, incident_id=2, object_type='unit 1 front left tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=30.3, south_or_rp2=45.9, east=0, west=0))
        db.session.add(Object(id=21, incident_id=2, object_type='unit 2 head', is_ref1=False, is_ref2=False,
                              north_or_rp1=32.1, south_or_rp2=50.1, east=0, west=0))
        db.session.add(Object(id=22, incident_id=2, object_type='unit 2 torso', is_ref1=False, is_ref2=False,
                              north_or_rp1=33.3, south_or_rp2=49.8, east=0, west=0))
        db.session.add(Object(id=23, incident_id=2, object_type='rp2', is_ref1=False, is_ref2=True,
                              north_or_rp1=55.7, south_or_rp2=0, east=0, west=0))
        db.session.add(Object(id=24, incident_id=2, object_type='unit 3 rear right tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=41.1, south_or_rp2=26.8, east=0, west=0))
        db.session.add(Object(id=25, incident_id=2, object_type='unit 3 front right tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=44.7, south_or_rp2=27, east=0, west=0))
        db.session.add(Object(id=26, incident_id=2, object_type='unit 3 rear left tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=40.2, south_or_rp2=29.2, east=0, west=0))
        db.session.add(Object(id=27, incident_id=2, object_type='unit 3 front left tire', is_ref1=False, is_ref2=False,
                              north_or_rp1=45.9, south_or_rp2=30.3, east=0, west=0))
        db.session.commit()

        result1 = {'unit 1 begin skid': (53.1, 12.2),
                   'aoi': (39.0, 28.1),
                   'unit 2 head': (32.1, 50.1),
                   'unit 2 torso': (33.3, 49.8),
                   'rp1rp2': 55.7,
                   'unit 3': [(41.1, 26.8), (44.7, 27.0), (40.2, 29.2), (45.9, 30.3)],
                   'unit 1': [(26.8, 41.1), (27.0, 44.7), (29.2, 40.2), (30.3, 45.9)]}
        assert dm.get_measurements('1') == result1
        assert dm.get_measurements('2') == result1
        assert dm.get_measurements('3') == {}

    def test_get_status(self):
        db.session.add(Incident(date="09/01/2021", time="15:30", county="Transylvania",
                                num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                                status="Open", officer=1))
        db.session.add(Incident(date="09/01/2021", time="15:30", county="Transylvania",
                                num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                                status="submittedToSuper", officer=1))
        db.session.add(Incident(date="09/03/2021", time="15:30", county="Transylvania",
                                num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                                status="pendingDmvReview", officer=1))
        db.session.add(Incident(date="09/04/2021", time="15:30", county="Transylvania",
                                num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                                status="underSuperReview", officer=1))
        db.session.add(Incident(date="09/05/2021", time="15:30", county="Transylvania",
                                num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                                status="rejectedBySuper", officer=1))
        db.session.add(Incident(date="09/06/2021", time="15:30", county="Transylvania",
                                num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                                status="rejected", officer=1))
        db.session.add(Incident(date="09/06/2021", time="15:30", county="Transylvania",
                                num_vehicles=1, severity=1, location="SR-1234", num_pedestrians=0,
                                status="approved", officer=1))
        db.session.commit()
        assert dm.get_status('1') == "Open"
        assert dm.get_status('2') == "submittedToSuper"
        assert dm.get_status('3') == "pendingDmvReview"
        assert dm.get_status('4') == "underSuperReview"
        assert dm.get_status('5') == "rejectedBySuper"
        assert dm.get_status('6') == "rejected"
        assert dm.get_status('7') == "approved"
        assert dm.get_status('8') is None


if __name__ == "__main__":
    unittest.main()
