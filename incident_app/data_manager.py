# Created by Andrew Davison
import re
from datetime import datetime, timedelta

import bleach

from incident_app import calculations, db
from incident_app.models.incident import Incident
from incident_app.models.object import Object


def hello():
    """
    Returns string saying hello from component.

    :return: string saying hello.
    """
    return "Hello from data_manager!"


def create_id(date: str, troop_id: str) -> str:
    """
    Queries database for number of incidents created on incident date from the troop identifier
    to calculate next sequence number to insert in incident_id.

    :param date: string of the date of the incident, i.e. 20211003
    :param troop_id: string of the creators troop identifier, i.e., BA
    :return: string of the incident_id, i.e. 20211003001BA.
    """
    # query database, filtered by date and troop_id
    num_reports = len(Incident.query.filter(Incident.crash_sequence.startswith(date),
                                            Incident.crash_sequence.endswith(troop_id)).all())
    if num_reports == 0:
        sequence_num = '001'
    else:
        sequence_num = str(num_reports + 1).zfill(3)
    incident_id = date + sequence_num + troop_id
    return incident_id


def create_new_incident(incident: Incident):
    """
    Validates and creates new incident record in database.
    :param incident: incident to validate and create.
    :return: None or throws AttributeError.
    """
    # date, time, county, location, and status are strings that need cleaning
    try:
        validate_new_incident(incident)

        # placeholder troop_id until we can query the county table using the incident county
        troop_id = 'A9'  # database query to find the troop id, i.e. 'A9' for the county of incident
        # troop_id = County.query.filter_by(county == incident.county).first()

        regex = '[/\\-.,*()]'
        date_list = re.split(regex, incident.date)
        date = date_list[2] + date_list[0] + date_list[1]

        # create incident id
        incident_id = create_id(date, troop_id)

        # clean string inputs
        incident.crash_sequence = bleach.clean(incident_id)
        incident.date = bleach.clean(incident.date)
        incident.time = bleach.clean(incident.time)
        incident.county = bleach.clean(incident.county)
        incident.location = bleach.clean(incident.location)

        db.session.add(incident)
        db.session.commit()
    except ValueError as err:
        raise AttributeError(f'Oops...something went wrong :(\n\t{err}')


def get_open_incidents(username: str, status: list) -> list:
    """
    Queries database for all incidents that require user action.

    :param username: name of user that is logged in.
    :param status: list of status search filters.
    :return: list of incident records.
    """
    pass


def text_search(username: str, incident_id=None or str, status=None or str) -> list:
    """
    Queries database for incident(s) that match search criteria.

    :param username: name of user that is logged in.
    :param incident_id: incident sequence number to search.
    :param status: list of status to search. Default is None
    :return: list of incident record(s).
    """
    pass


def filter_search(username: str, filters: list) -> list:
    """
    Queries database for incident(s) that match filtered search criteria.

    :param username: name of user that is logged in.
    :param filters: list of filters to apply to database query.
    :return: list of incident record(s).
    """
    pass


def get_incident(username: str, incident_id: str) -> list:
    """
    Retrieves incident data from database for editing or viewing incident.

    :param username: name of user that is logged in.
    :param incident_id: incident sequence number to access.
    :return: list of incident data.
    """
    pass


def save_data(incident_id: str, data: dict) -> None:
    """
    Saves raw data to specified incident_id record in database.

    :param incident_id: sequence number to update
    :param data: dictionary of data to be stored in database.
    :return: None
    """
    pass


def get_calculations(incident_id: str, data: dict) -> dict:  # remove dictionary parameter, will compile on query
    """
    Retrieves incident calculations for user verification.

    :param incident_id: sequence number of incident to get calculations for.
    :return: dictionary of calculations.
    """
    # print(f'Querying database for IncidentID: {incident_id}...')
    # this is where the function will query the database for the measurements and store as a dictionary

    measurements = data  # delete after tests
    # calculate average of force measurements
    force = measurements['force']  # might need to keep this depending on how what data we store and retrieve
    # force = calculations.calculate_average_force(measurements['force'])  # uncomment??

    # calculate drag factor coefficient
    drag_factor = calculations.calculate_drag_factor(force, measurements['sled_weight'])

    # calculate velocities at start of skid, skid to impact, and after impact
    start_velocity = calculations.calculate_velocity(drag_factor, measurements['skid_total_distance'])
    skid_velocity = calculations.calculate_velocity(drag_factor, measurements['skid_start_distance'])
    impact_velocity = calculations.calculate_velocity(drag_factor, measurements['skid_end_distance'])

    # calculate time of skid
    time_of_skid = calculations.calculate_time_of_skid(start_velocity, drag_factor)

    # calculate kinetic energy at impact
    kinetic_energy = calculations.calculate_kinetic_energy(measurements['total_weight'], skid_velocity)
    # kinetic_energy = calculations.calculate_kinetic_energy(measurements['vehicle_weight'], skid_velocity)

    # convert three velocities to speed
    start_speed = calculations.calculate_speed(start_velocity)
    skid_speed = calculations.calculate_speed(skid_velocity)
    impact_speed = calculations.calculate_speed(impact_velocity)

    # compile dictionary
    calc_dict = dict([('drag_factor', round(drag_factor, 2)), ('start_velocity', round(start_velocity, 2)),
                      ('skid_velocity', round(skid_velocity, 2)), ('impact_velocity', round(impact_velocity, 2)),
                      ('time_of_skid', round(time_of_skid, 2)), ('kinetic_energy', round(kinetic_energy, 2)),
                      ('start_speed', round(start_speed, 2)), ('skid_speed', round(skid_speed, 2)),
                      ('impact_speed', round(impact_speed, 2))])
    return calc_dict


def get_measurements(incident_id: str) -> dict:
    """
    Retrieves all measurements for incident for drawing of incident scene.

    :param incident_id: string of incident id to get measurements for.
    :return: dictionary of object key and measurement values.
    """
    # query database Object table for measurements
    objects = db.session.query(Object.object_type, Object.north_or_rp1, Object.south_or_rp2) \
        .where(Object.incident_id == int(incident_id)).all()

    # convert result to a dictionary
    meas_dict = dict([(k[0], k[1:]) for k in objects])

    # set rp1 to rp2 measurement
    try:
        meas_dict['rp1rp2'] = meas_dict.pop('rp2')[0]
    except KeyError:
        pass

    count = 0
    unit_num = ""
    remove_set = ""
    vehicle_set = ""
    # check for four tires
    for key, value in meas_dict.items():

        if 'unit' in key and 'tire' in key:
            unit_num = key[5]
        if 'unit' in key and 'tire' in key and key[5] == unit_num:
            count += 1
        if count == 4:
            # find all vehicles and keys that correspond to each vehicle measurements
            vehicle_set = set(k[:6] for k in meas_dict if k.endswith('tire'))
            remove_set = set(k for k in meas_dict if k.endswith('tire'))
            # combine measurements to vehicles

            # dictionary cleanup

            count = 0
    if len(vehicle_set) > 0:
        for i in vehicle_set:
            meas_dict[i] = [meas_dict[k] for k in meas_dict if k.startswith(i) and k.endswith('tire')]

    if len(remove_set) > 0:
        for i in remove_set:
            meas_dict.pop(i)

    if 'rp1' in meas_dict:
        meas_dict.pop('rp1')

    # return dictionary
    return meas_dict


def get_status(incident_id: str) -> str or None:
    """
    Gets current routing/completion status of incident.

    :param incident_id: sequence number of incident to retrieve status for.
    :return: status string or None if no incident record in database.
    """
    inc_status = db.session.query(Incident.status).where(Incident.id == int(incident_id)).first()
    if inc_status is not None:
        return inc_status[0]
    else:
        return


def validate_new_incident(incident: Incident):
    """
    Validates new incident inputs for date, time, location, county and status.
    :param incident: new incident instance to be validated.
    :return: None
    """
    # regex for date and time splits
    regex = '[/\\-.,*():]'
    date = re.split(regex, incident.date)
    time = re.split(regex, incident.time)
    delta = (datetime.now().date() - timedelta(days=365)).strftime('%Y%m%d')

    # moths with 31 days in them for validation checks
    big_months = ['01', '03', '05', '07', '08', '10', '12']

    # placeholder counties until we can query the county table
    counties = ['Transylvania', 'Gotham', 'Hazzard', 'Hope County', 'Derry', 'Haddonfield',
                'New Hanover', 'Duplin', 'Onslow']
    # counties = County.query.filter(county).all()

    # validate date
    if (len(date) != 3) or (1 > int(date[0]) > 12) or \
            (int(date[0]) == 2 and (1 > int(date[1]) or int(date[1]) > 29) and int(date[2]) % 4 != 0) or \
            (int(date[0]) == 2 and (1 > int(date[1]) or int(date[1]) > 28) and int(date[2]) % 4 != 0) or \
            (int(date[0]) != 2 and date[0] not in big_months and (1 > int(date[1]) or int(date[1]) > 30)) or \
            (int(date[0]) != 2 and date[0] in big_months and (1 > int(date[1]) or int(date[1]) > 31)) or \
            (int(date[2] + date[0] + date[1]) <= int(delta) or
             int(datetime.now().date().strftime('%Y%m%d')) < int(date[2] + date[0] + date[1])):
        raise ValueError('Invalid date input.')

    # validate time
    if (len(time) != 2) or (0 > int(time[0]) or int(time[0]) > 23) or (0 > int(time[1]) or int(time[1]) > 59):
        raise ValueError('Invalid time input.')

    # validate location
    if len(incident.location) > 25:
        raise ValueError('Invalid location input length, must be less than 25 characters.')

    # validate county
    if incident.county not in counties and incident.county != '' or len(incident.county) > 25:
        raise ValueError('Invalid county input, check if county exists or county length is less than 25 characters.')

    # validate number of vehicles
    if incident.num_vehicles < 1:
        raise ValueError('There must be at least 1 vehicle in incident.')

    # validate severity
    if incident.severity not in [1, 2, 3]:
        raise ValueError('Incident severity should be an integer 1, 2, or 3.')
