import math

from bleach import clean
from flask import \
    Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from incident_app import db
from incident_app.data_manager import create_new_incident, get_measurements
from incident_app.models.app_enums import Severity
from incident_app.models.incident import Incident
from incident_app.models.object import Object
from incident_app.models.user import User
from incident_app.models.vehicle import Vehicle
from incident_app.report_manager.forms import \
    FindIncidentById, NewIncidentForm, NewObjectForm, NewVehicleForm

report_manager = Blueprint('report_manager', __name__)


@report_manager.route('/ops/new-incident', methods=['GET', 'POST'])
@login_required
def new_incident():
    form = NewIncidentForm()
    if form.validate_on_submit():
        incident = Incident()
        incident.officer = form.badge_num.data
        incident.severity = int(form.severity_select.data)
        incident.date = form.date.data
        incident.time = form.time.data
        incident.location = form.location.data
        incident.county = form.county.data
        incident.num_vehicles = form.vehicles.data
        incident.num_pedestrians = form.pedestrians.data
        assisting = form.assisted_by.data
        incident.photos_taken = form.photos_taken.data
        incident.photographer = form.photographer.data
        try:
            create_new_incident(incident)
            flash('Your incident has been created', 'success')
            if assisting:
                u = User.query.get(assisting)
                if u:
                    u.add_assist(incident)
                else:
                    flash('Issue finding assisting officer in system. No secondary added.')
            if form.to_vehicles.data:
                return redirect(url_for('report_manager.view_incident',
                                        incident_id=incident.id))
            return redirect(url_for('main.home_page'))
        except AttributeError:
            flash('Issue validating incident. Review inputs, try again.')
            return render_template('new_incident.html', title='New Incident',
                                   form=form)

    else:
        return render_template('new_incident.html', title='New Incident',
                               form=form)


@report_manager.route('/ops/find-incident', methods=['GET', 'POST'])
@report_manager.route('/ops/inc', methods=['GET', 'POST'])
@login_required
def find_incident():
    form = FindIncidentById()
    if form.validate_on_submit():
        flash('Incident Found')
        return redirect(url_for('report_manager.view_incident',
                                incident_id=form.search_id.data))
    else:
        return render_template('find_incident.html', form=form)


@report_manager.route('/ops/inc/<int:incident_id>')
@login_required
def view_incident(incident_id):
    inc = Incident.query.get_or_404(incident_id)
    sev = Severity(inc.severity)
    return render_template('view_incident.html',
                           title='View Incident', inc=inc, sev=sev)


@report_manager.route('/ops/add-object', methods=['GET', 'POST'])
@login_required
def add_object():
    form = NewObjectForm()
    incident_id = request.args.get('incident_id')
    # inc = None
    if incident_id:
        inc = Incident.query.get(incident_id)
        if inc is None:
            flash('Passed incident reference does not match any existing incident, please try to reenter.')
            return redirect(url_for('report_manager.find_incident'))
        form.incident_id.data = inc.id
        if form.validate_on_submit():
            obj = Object()
            obj.incident_id = inc.id
            obj.object_type = clean(form.type_desc.data).lower()
            if form.is_rp1.data:
                obj.is_ref1 = True
                obj.north_or_rp1 = form.north_or_rp1.data
            # elif form.is_rp2.data:
            #     # obj.is_ref2 = True
            #     obj.south_or_rp2 = form.south_or_rp2.data
            else:
                obj.north_or_rp1 = form.north_or_rp1.data
                obj.south_or_rp2 = form.south_or_rp2.data
                # obj.east = form.east.data
                # obj.west = form.west.data
            db.session.add(obj)
            db.session.commit()
            flash('Object registered successfully')
            if form.submit_and_continue.data:
                return redirect(url_for('report_manager.add_object', incident_id=inc.id))
            else:
                return redirect(url_for('report_manager.view_incident', incident_id=inc.id))
    else:
        flash('Objects must be associated through an incident.')
        return redirect(url_for('report_manager.find_incident'))
    return render_template('add_object.html', title='Measurements',
                           form=form)


@report_manager.route('/ops/add-vehicle', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    form = NewVehicleForm()
    incident_id = request.args.get('incident_id')
    inc = None
    if incident_id:
        inc = Incident.query.get(incident_id)
        if inc is None:
            flash('Passed incident reference does not match any existing incident, please try to reenter.')
            return redirect(url_for('report_manager.find_incident'))
        form.incident_id.data = incident_id
    if form.validate_on_submit():
        plate = clean(form.plate.data.upper())
        res = Vehicle.query.filter_by(state=form.state.data.upper(),
                                      plate=plate).first()
        data = [clean(form.damage.data),
                form.skid_before.data,
                form.skid_after.data,
                form.airbag_front.data,
                form.airbag_side.data]
        if inc is None:
            inc = Incident.query.get_or_404(form.incident_id.data)
        if not res:
            vehicle = Vehicle()
            vehicle.state = clean(form.state.data).upper()
            vehicle.plate = clean(form.plate.data).upper()
            vehicle.num_occupants = form.num_occupants.data
            vehicle.weight = form.weight.data
            vehicle.make = clean(form.make.data).upper()
            vehicle.model = clean(form.model.data).upper()
            vehicle.color = clean(form.color.data).upper()
            db.session.add(vehicle)
            db.session.commit()
            vehicle.associate_incident(inc, data)
        else:
            flash('Vehicle already registered with system. Cannot adjust weight of vehicle.')
            inc.associate_vehicle(res, data)
        flash('System Updated')
        if form.submit_and_continue.data:
            return redirect(url_for('report_manager.add_vehicle', incident_id=form.incident_id.data))
        else:
            return redirect(url_for('report_manager.view_incident', incident_id=form.incident_id.data))
    return render_template('add_vehicle.html',
                           title='Add Vehicle(s)', form=form)


@report_manager.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    incident_id = request.args.get('incident_id')
    measurements = get_measurements(incident_id)

    # for key, value in measurements.items():
    #     if 'unit' in key and key[-1].isnumeric():
    #         print("value:", value)

    if measurements is None:
        measurements = {}

    # check that measurements form a triangle
    def check_triangle(a, b, c):
        if a + b > c and a + c > b and b + c > a:
            return True
        else:
            return False

    # check that all measurements comply with triangle rule
    def check_all_measurements(data):
        if data == {}:
            return False

        if 'rp1rp2' in data:
            rp1rp2 = data['rp1rp2'][0]
        else:
            return False

        for key, value in data.items():
            if key != 'rp1rp2':
                if 'unit' in key and key[-1].isdigit():
                    if isinstance(value,list):
                        for i in value:
                            if not (check_triangle(rp1rp2, i[0], i[1])):
                                return False
                    elif not (check_triangle(rp1rp2, value[0], value[1])):
                        return False
                elif not (check_triangle(rp1rp2, value[0], value[1])):
                    return False
        return True

    # determine one angle from 3 sides, needed for calc coords
    def angle(a, b, c):
        return math.degrees(math.acos((b ** 2 + c ** 2 - a ** 2) / (2.0 * b * c)))

    # calculate coordinates of object based off measurements from reference points
    def calc_coords(rp1rp2, rp1obj, rp2obj, bottom_location: bool = False):
        a = rp2obj
        b = rp1rp2
        c = rp1obj
        A = angle(a, b, c)
        Ax = 150  # hard coded rp locations
        Ay = 330  # hard coded rp locations
        Cx = 430  # hard coded rp locations
        Cy = 330  # hard coded rp locations
        uACx = (Cx - Ax) / b
        uACy = (Cy - Ay) / b

        if bottom_location:
            uABx = uACx * math.cos(math.radians(A)) + uACy * math.sin(math.radians(A))
            uABy = uACx * math.sin(math.radians(A)) + uACy * math.cos(math.radians(A))
            Bx = Ax + c * uABx
            By = Ay + c * uABy
        else:
            uABx = uACx * math.cos(math.radians(A)) + uACy * math.sin(math.radians(A))
            uABy = - uACx * math.sin(math.radians(A)) + uACy * math.cos(math.radians(A))
            Bx = Ax + c * uABx
            By = Ay + c * uABy
        return Bx, By

    def get_data(incident_id: None):
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
        try:
            incident_data['assisting'] = record[0].secondary_officers[0].name
        except IndexError:
            pass
        incident_data['photos_taken'] = record[0].photos_taken
        incident_data['photographer'] = record[0].photographer

        return incident_data

    incident_data = get_data(incident_id)

    if check_all_measurements(measurements):
        trans_measurements = {}
        for key, value in measurements.items():
            if key == 'rp1rp2':
                trans_measurements[key] = value[0]
            elif 'unit' in key and key[-1].isdigit():
                if isinstance(value, list) and len(value) == 4:
                    trans_measurements[key] = [calc_coords(measurements['rp1rp2'][0], value[0][0], value[0][1]),
                                               calc_coords(measurements['rp1rp2'][0], value[1][0], value[1][1]),
                                               calc_coords(measurements['rp1rp2'][0], value[2][0], value[2][1]),
                                               calc_coords(measurements['rp1rp2'][0], value[3][0], value[3][1])]
                else:
                    trans_measurements[key] = calc_coords(measurements['rp1rp2'][0], value[0][0], value[0][1])
            else:
                trans_measurements[key] = calc_coords(measurements['rp1rp2'][0], value[0], value[1])

        return render_template('report.html', data=trans_measurements, incident_id=incident_id,
                               incident_data=incident_data, for_report=measurements)
    else:
        inv_measure = {'Invalid': 'Invalid'}
        return render_template('report.html', data=inv_measure, incident_id=incident_id, incident_data=incident_data,
                               for_report=measurements)


class TriangleException(Exception):
    pass
