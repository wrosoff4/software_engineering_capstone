from incident_app.models.measurements import Measurement


def test_measurement_constructor():
    m = Measurement("meters", "distance", 3)
    assert m.measurement_name == "meters"
    assert m.measurement_type == "distance"
    assert type(m.measurement) is float
    assert m.measurement == 3.0


def test_measurement_constructor_feet_inches():
    m = Measurement("feet", "distance", (11, 2))
    assert m.measurement_name == "feet"
    assert m.measurement_type == "distance"
    assert type(m.measurement) is float
    assert round(m.measurement, 2) == 11.17
