# Created by Andrew Davison
# Instructions to run unittest: Run main conditional at end of file
import unittest

from incident_app import calculations as calc


class TestCalculations(unittest.TestCase):

    def test_calculate_average_force(self):
        measurements = [30.2, 30.5, 30.4, 30.2, 30.3]
        assert calc.calculate_average_force(measurements) == 30.32
        measurements = [130.2, 130.5, 130.4, 130.2, 130.3]
        assert calc.calculate_average_force(measurements) == 130.32
        measurements = [210, 202.2, 215, 205, 204.3]
        assert calc.calculate_average_force(measurements) == 207.3
        with self.assertRaises(TypeError):
            measurements = ['130.2', '130.5', '130.4', '130.2', '130.3']
            calc.calculate_average_force(measurements)

    def test_calculate_drag_factor(self):
        force, sled_weight = 30.32, 230
        assert round(calc.calculate_drag_factor(force, sled_weight), 2) == 0.13
        force, sled_weight = 130.32, 230
        assert round(calc.calculate_drag_factor(force, sled_weight), 2) == 0.57
        with self.assertRaises(TypeError):
            force, sled_weight = '130.32', 230
            round(calc.calculate_drag_factor(force, sled_weight), 2)
            force, sled_weight = 130.32, '230'
            round(calc.calculate_drag_factor(force, sled_weight), 2)
        with self.assertRaises(ZeroDivisionError):
            force, sled_weight = 130.32, 0
            round(calc.calculate_drag_factor(force, sled_weight), 2)

    def test_calculate_velocity(self):
        factor, distance = 0.13, 45
        assert round(calc.calculate_velocity(factor, distance), 2) == 19.41
        distance = 15
        assert round(calc.calculate_velocity(factor, distance), 2) == 11.21
        distance = 30
        assert round(calc.calculate_velocity(factor, distance), 2) == 15.85
        distance = 0
        assert round(calc.calculate_velocity(factor, distance), 2) == 0
        factor, distance = calc.calculate_drag_factor(30.32, 230), 45
        assert round(calc.calculate_velocity(factor, distance), 2) == 19.55
        distance = 15
        assert round(calc.calculate_velocity(factor, distance), 2) == 11.28
        distance = 30
        assert round(calc.calculate_velocity(factor, distance), 2) == 15.96
        with self.assertRaises(TypeError):
            factor, distance = 0.13, '0'
            round(calc.calculate_velocity(factor, distance), 2)
            factor, distance = '0.13', 0
            round(calc.calculate_velocity(factor, distance), 2)

    def test_calculate_time_of_skid(self):
        factor = calc.calculate_drag_factor(30.32, 230)
        velocity = calc.calculate_velocity(factor, 45)
        assert round(calc.calculate_time_of_skid(velocity, factor), 2) == 4.60
        velocity = calc.calculate_velocity(factor, 30)
        assert round(calc.calculate_time_of_skid(velocity, factor), 2) == 3.76
        velocity = calc.calculate_velocity(factor, 15)
        assert round(calc.calculate_time_of_skid(velocity, factor), 2) == 2.66
        with self.assertRaises(TypeError):
            velocity = calc.calculate_velocity(factor, 15)
            round(calc.calculate_time_of_skid(str(velocity), factor), 2)
            velocity = calc.calculate_velocity(factor, 15)
            round(calc.calculate_time_of_skid(velocity, str(factor)), 2)
        with self.assertRaises(ZeroDivisionError):
            round(calc.calculate_time_of_skid(velocity, 0), 2)

    def test_calculate_kinetic_energy(self):
        factor = calc.calculate_drag_factor(30.32, 230)
        weight, velocity = 3674, calc.calculate_velocity(factor, 30)
        assert round(calc.calculate_kinetic_energy(weight, velocity), 2) == 14529.87
        assert round(calc.calculate_kinetic_energy(0, velocity), 2) == 0
        assert round(calc.calculate_kinetic_energy(weight, 0), 2) == 0
        with self.assertRaises(TypeError):
            round(calc.calculate_kinetic_energy(str(weight), velocity), 2)
            round(calc.calculate_kinetic_energy(weight, str(velocity)), 2)

    def test_calculate_speed(self):
        factor, distance = calc.calculate_drag_factor(30.32, 230), 45
        velocity = calc.calculate_velocity(factor, distance)
        assert round(calc.calculate_speed(velocity), 2) == 13.33
        distance = 15
        velocity = calc.calculate_velocity(factor, distance)
        assert round(calc.calculate_speed(velocity), 2) == 7.70
        distance = 30
        velocity = calc.calculate_velocity(factor, distance)
        assert round(calc.calculate_speed(velocity), 2) == 10.89
        assert round(calc.calculate_speed(0), 2) == 0
        with self.assertRaises(TypeError):
            round(calc.calculate_speed(str(velocity)), 2)


if __name__ == "__main__":
    unittest.main()
