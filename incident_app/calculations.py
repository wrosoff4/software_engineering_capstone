# Created by Andrew Davison
# All calculations are using the full floating point calculated value, rounding occurs for storage

def hello():
    """
    Returns string saying hello from component.
    :return: string saying hello.
    """
    return "Hello from calculations!"


def calculate_average_force(measurements: list) -> float:
    """
    Calculates and returns average force.

    :param measurements: list of force measurements.
    :return: float of calculated average of measurements list.
    """
    return sum(measurements) / len(measurements)


def calculate_drag_factor(force: float, weight: float) -> float:
    """
    Calculates drag factor coefficient f from the mean of sled pulls / weight of sled,
    f = F/W.

    :param force: F = mean of drag sled measurements.
    :param weight: W = weight of the drag sled (lbs.).
    :return: float of calculated drag factor coefficient.
    """
    return force / weight


def calculate_velocity(drag_factor: float, distance: float) -> float:
    """
    Calculates velocity V = sqrt(64.4*f*D) ft/s. Used for calculating velocity at start of skid mark,
    velocity at time of impact, and velocity after impact.

    :param drag_factor: f = drag factor coefficient.
    :param distance: D = total distance of skid mark (ft).
    :return: float calculated velocity.
    """
    return (64.4 * drag_factor * distance) ** 0.5


def calculate_time_of_skid(velocity: float, drag_factor: float) -> float:
    """
    Calculate time t = V/(f*32.2) seconds, from start of skid to end of the skid mark.

    :param velocity: V = velocity at start of skid mark (ft/s).
    :param drag_factor: f = drag factor coefficient.
    :return: float calculated time.
    """
    return velocity / (drag_factor * 32.2)


def calculate_kinetic_energy(weight: float, velocity: float) -> float:
    """
    Calculates kinetic energy Ke = (W*V**2)/64.4 ft-lbs, exerted on impact.

    :param weight: W = total weight of vehicle and occupants (lbs).
    :param velocity: V = velocity on impact (ft/s).
    :return: float calculated kinetic energy
    """
    return (weight * velocity ** 2) / 64.4


def calculate_speed(velocity: float) -> float:
    """
    Calculates speed S = V/1.466, converting ft/s to mph. Used for calculating speed at start of skid mark,
    speed at point of impact, and speed after impact.

    :param velocity: V = velocity (ft/s).
    :return: float calculated speed.
    """
    return velocity / 1.466
