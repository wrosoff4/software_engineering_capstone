import os

from incident_app import db
from incident_app.models.incident import Incident, AssociatedVehicle
from incident_app.models.user import User
from incident_app.models.vehicle import Vehicle

base_dir = os.path.abspath(os.path.dirname(__file__))


# POPULATION METHODS
# Roles: Trooper -> 1; Supervisor -> 2; HR -> 3;
def populate_user_table():
    filepath = os.path.join(base_dir, 'static/seed_data/users.txt')
    user_file = open(filepath, "r")
    for line in user_file:
        data = line.strip().split(',')
        user = User()
        user.id = data[0]
        user.name = data[1]
        user.email = data[2]
        user.password = data[3]
        user.role = data[4]
        db.session.add(user)
    user_file.close()
    db.session.commit()


# severity: property_damage -> 1; bodily_damage -> 2; fatality -> 3
def populate_incident_table():
    filepath = os.path.join(base_dir, 'static/seed_data/incidents.txt')
    incident_file = open(filepath, "r")
    for line in incident_file:
        data = line.strip().split(',')
        incident = Incident(id=data[0], crash_sequence=data[1],
                            county=data[2], severity=data[3],
                            officer=data[4], status=data[5])
        db.session.add(incident)
    incident_file.close()
    db.session.commit()


def populate_supervises():
    filepath = os.path.join(base_dir, 'static/seed_data/supervising.txt')
    supervising_file = open(filepath, 'r')
    for line in supervising_file:
        data = line.split(',')
        supervisor = User.query.get(data[0])
        underling = User.query.get(data[1])
        if supervisor and underling:
            supervisor.add_supervisee(underling)
    db.session.commit()


def populate_vehicle_table():
    filepath = os.path.join(base_dir, 'static/seed_data/vehicles.txt')
    vehicle_file = open(filepath, "r")
    for line in vehicle_file:
        data = line.strip().split(',')
        vehicle = Vehicle(state=data[1].upper(),
                          plate=data[2].upper(), make=data[3].upper(),
                          model=data[4].upper(), color=data[5].upper(),
                          num_occupants=data[6], weight=data[7])
        db.session.add(vehicle)
    vehicle_file.close()
    db.session.commit()


def populate_association():
    filepath = os.path.join(base_dir, 'static/seed_data/association.txt')
    association_file = open(filepath, "r")
    for line in association_file:
        line = line.split(',')
        inc = line[0]
        v = line[1]
        va = AssociatedVehicle(incident_id=inc, vehicle_id=v)
        db.session.add(va)
    association_file.close()
    db.session.commit()


def populate():
    populate_user_table()
    populate_supervises()
    populate_incident_table()
    populate_vehicle_table()
    populate_association()
