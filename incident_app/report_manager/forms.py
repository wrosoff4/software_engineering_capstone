import re
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import \
    StringField, SubmitField, IntegerField, BooleanField, FloatField, SelectField, TextAreaField, HiddenField
from wtforms.validators import \
    DataRequired, Optional, NumberRange, ValidationError, Length  # noqa

from incident_app.models.incident import Incident
from incident_app.models.user import User


class NewIncidentForm(FlaskForm):
    badge_num = IntegerField('Primary Investigator (Badge Number)*',
                             validators=[DataRequired(
                                 message='Check that you entered a badge number for primary'),
                                 NumberRange(min=0,
                                             message='Check that you entered a badge number for primary')])
    severity_select = SelectField('Severity*', choices=[(0, '--select severity--'),
                                                        (1, 'Property Damage'),
                                                        (2, 'Bodily Harm'),
                                                        (3, 'Fatality')],
                                  validators=[DataRequired()])
    date = StringField('Collision Date', default=datetime.now().strftime('%m/%d/%Y'))
    time = StringField('Collision Time', default=datetime.now().strftime('%H:%M'))
    county = StringField('County',
                         validators=[DataRequired(), Length(min=3, max=25)])
    location = StringField('Location',
                           validators=[DataRequired(), Length(min=3, max=25)])
    # use badge numbers for now
    assisted_by = IntegerField('Assisted by (Badge Number)',
                               validators=[Optional(),
                                           NumberRange(min=0,
                                                       message='check you entered a'
                                                               ' badge number for assisting.')])
    photos_taken = BooleanField('Photographs Taken', default=False)
    photographer = StringField('Photographer',
                               validators=[Optional()])
    vehicles = IntegerField('Vehicle(s) Involved', default=1,
                            validators=[NumberRange(min=1,
                                                    message='Every incident requires at least 1 vehicle.')])
    pedestrians = IntegerField('Pedestrians', default=0,
                               validators=[NumberRange(min=0,
                                                       message='Cannot have negative quantity of pedestrians.')])
    notes = TextAreaField('Notes', validators=[Optional()])
    close = SubmitField('Save and Close')
    to_vehicles = SubmitField('Save and Continue')

    def validate_badge_num(self, test_id):  # noqa
        res = User.query.get(test_id.data)
        if res is None or res.role == 3:
            raise ValidationError('Please enter a valid user')

    def validate_severity_select(self, choice):  # noqa
        if choice.data == '0':
            raise ValidationError('Please select a severity')

    # def validate_assisted_by(self, assisted_by):
    #     res = User.query.get(self.assisted_by.data)
    #     if res is None or res.role == 3:
    #         raise ValidationError('Please enter a valid user')

    # def validate_pedestrians(self, pedestrians):
    #     if self.severity.data > 1 > pedestrians.data:
    #         raise ValidationError('At least one person must be involved for an incident of this severity')


class FindIncidentById(FlaskForm):
    search_id = IntegerField('Incident ID',
                             validators=[DataRequired(),
                                         NumberRange(min=1)])
    submit_search = SubmitField('Find Incident')

    @staticmethod
    def validate_search_id(self, search_id):  # noqa
        if Incident.query.get(search_id.data) is None:
            raise ValidationError('Entered incident could not be found')


class NewVehicleForm(FlaskForm):
    state = StringField('State*', validators=[DataRequired(),
                                              Length(min=2, max=2)])
    plate = StringField('License Plate*',
                        validators=[DataRequired()])
    incident_id = IntegerField('Incident ID*',
                               validators=[DataRequired()])
    num_occupants = IntegerField('# of Occupants*', default=1,
                                 validators=[DataRequired(),
                                             NumberRange(min=0)])
    weight = FloatField('Vehicle Weight*',
                        validators=[DataRequired(),
                                    NumberRange(min=0)])
    make = StringField('Make*', validators=[DataRequired(),
                                            Length(min=2, max=25)])
    model = StringField('Model*', validators=[DataRequired(),
                                              Length(min=2, max=25)])
    color = StringField('Color*')
    damage = HiddenField('damage', validators=[Optional()])
    skid_before = FloatField('Before Impact', default=0,
                             validators=[Optional(),
                                         NumberRange(min=0)])
    skid_after = FloatField('After Impact', default=0,
                            validators=[Optional(),
                                        NumberRange(min=0)])
    airbag_front = BooleanField('Front Airbags', default=False,
                                validators=[])
    airbag_side = BooleanField('Side Airbags', default=False,
                               validators=[])
    submit = SubmitField('Save and Return')
    submit_and_continue = SubmitField('Save and Add Another')

    def validate_color(self, color):  # noqa
        if re.match(r'^[0-9]*$', color.data):
            raise ValidationError('Numeric values not accepted here.')

    def validate_incident_id(self, incident_id):  # noqa
        res = Incident.query.get(self.incident_id.data)
        if res is None:
            raise ValidationError('Entered incident id is not valid')


class NewObjectForm(FlaskForm):
    incident_id = IntegerField(validators=[DataRequired()])
    type_desc = StringField('RP1 to RP2?', id='desc', validators=[DataRequired('Required'),
                                                Length(min=1, max=25)])
    is_rp1 = BooleanField('RP1', id='check',
                          validators=[Optional()])
    # is_rp2 = BooleanField('RP2',
    #                       validators=[Optional()])
    north_or_rp1 = FloatField('RP1', id='rp1', validators=[Optional()])
    south_or_rp2 = FloatField('RP2', id='rp2', validators=[Optional()])
    # east = FloatField('East', validators=[Optional()])
    # west = FloatField('West', validators=[Optional()])
    submit = SubmitField('Save and Return')
    submit_and_continue = SubmitField('Save and Add Another')

    def validate_incident_id(self, incident_id):  # noqa
        res = Incident.query.get(self.incident_id.data)
        if res is None:
            raise ValidationError('Invalid incident associated with object')

    def validate_is_rp1(self, is_rp1):
        # if is_rp1.data and self.is_rp2.data:
        #     raise ValidationError('Can only be assigned as one RP')
        res = Incident.query.get(self.incident_id.data)
        if res is None:
            raise ValidationError('No incident associated. Find Incident and try again.')
        objects = res.objects.all()
        for o in objects:
            if o.is_ref1:
                raise ValidationError('Incident already has a RP1')

    # def validate_is_rp2(self, is_rp2):
    #     if self.is_rp1.data and is_rp2.data:
    #         raise ValidationError('Can only be assigned as one RP')
    #     res = Incident.query.get(self.incident_id.data)
    #     if res is None:
    #         raise ValidationError('No incident associated. Find Incident and try again.')
    #     objects = res.objects.all()
    #     for o in objects:
    #         if o.is_ref2:
    #             raise ValidationError('Incident already has a RP2')
