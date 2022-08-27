"""
Travis Fryar
Unit testing draw functions
Test by running this file
"""

import math
import unittest
from incident_app.models.app_enums import Severity
from incident_app.models.incident import Incident
from incident_app.models.object import Object
from incident_app.models.user import User
from incident_app.models.vehicle import Vehicle
from incident_app import db


# dictionary template:
#     {'rp1rp2': 100, 'body': (60, 60), 'left_skid': [(35, 78), (25, 88)], 'right_skid': [(42, 80), (32, 90)],
#      'car': [(28, 102), (32, 90), (25, 88), (20, 100)], 'aoi': (70, 50)})

def angle(a, b, c):
    return math.degrees(math.acos((b ** 2 + c ** 2 - a ** 2) / (2.0 * b * c)))


def check_triangle(a, b, c):
    if a + b > c and a + c > b and b + c > a:
        return True
    else:
        return False


def check_all_measurements(data):
    if data == {}:
        return False

    if 'rp1rp2' in data:
        rp1rp2 = data['rp1rp2'][0]
    else:
        return False

    for KEY in data:
        if 'rp1rp2' not in KEY and not ('unit' in KEY and KEY[-1].isnumeric()) and not check_triangle(rp1rp2,
                                                                                                      data[KEY][0],
                                                                                                      data[KEY][1]):
            return False
        elif 'unit' in KEY and KEY[-1].isnumeric() and not (
                check_triangle(rp1rp2, data[KEY][0][0], data[KEY][0][1]) and
                check_triangle(rp1rp2, data[KEY][1][0], data[KEY][1][1]) and
                check_triangle(rp1rp2, data[KEY][2][0], data[KEY][2][1]) and
                check_triangle(rp1rp2, data[KEY][3][0], data[KEY][3][1])):
            return False
    return True


def get_data(incident_id):
    incident_data = {}
    record = Incident.query.filter_by(id=incident_id).all()
    incident_data['incident_id'] = incident_id
    incident_data['date'] = record[0].date
    incident_data['time'] = record[0].time
    incident_data['officer_id'] = record[0].officer
    incident_data['officer_name'] = User.query.filter_by(id=record[0].officer).all()[0].name
    incident_data['location'] = record[0].location
    incident_data['county'] = record[0].county
    incident_data['severity'] = record[0].severity
    incident_data['num_vehicles'] = record[0].num_vehicles
    incident_data['num_pedestrians'] = record[0].num_pedestrians
    incident_data['status'] = record[0].status
    incident_data['crash_seq'] = record[0].crash_sequence
    incident_data['assisting'] = record[0].secondary_officers[0].name
    incident_data['photos_taken'] = record[0].photos_taken
    incident_data['photographer'] = record[0].photographer

    return incident_data


class DrawTest(unittest.TestCase):

    def test_angle_function_1(self):
        self.assertEqual(60, round(angle(10, 10, 10)))

    def test_triangle_check_1(self):
        self.assertTrue(check_triangle(10, 10, 10))

    def test_triangle_check_2(self):
        self.assertFalse(check_triangle(10, 0, 10))

    def test_check_all_measurements_1(self):
        measurements = {'rp1rp2': (55.7, 0.0), 'skid start': (53.1, 12.2), 'aoi': (39.0, 28.1),
                        'unit 2 body': (32.1, 50.1), 'unit 1': [(26.8, 41.1), (28.0, 46.5), (29.2, 40.2), (30.3, 45.9)]}
        self.assertTrue(check_all_measurements(measurements))

    def test_check_all_measurements_2(self):
        measurements = {}
        self.assertFalse(check_all_measurements(measurements))

    # def test_get_data_1(self):
    #     data = get_data(1)
    #     self.assertIsNotNone(data)
    #
    # def test_get_data_2(self):
    #     data = get_data(1)
    #     self.assertEqual(len(data), 15)


if __name__ == '__main__':
    unittest.main()
