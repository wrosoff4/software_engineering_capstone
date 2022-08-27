from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, IntegerField, TextField, DateField


class NewUserForm(FlaskForm):
    name_field: str = TextField(label='User Name')
    id_field: int = IntegerField(label='User ID')
    role_field: str = TextField('User Role')
    email_field: str = TextField(label='User Name')
    date_field: str = DateField(label='Date Added')
    precinct_field: str = TextField(label='Precinct')
    password_field: str = PasswordField(label='Confirm Password')
    confirm_password_field: str = PasswordField()
    submit = SubmitField(label='Create User')


class FindUserForm(FlaskForm):
    name_field: str = TextField(label='User Name')
    id_field: int = IntegerField(label='User ID')
    submit = SubmitField('Find User')


class EditUserForm(FlaskForm):
    name_field: str = TextField(label='User Name')
    id_field: int = IntegerField(label='User ID')
    role_field: str = TextField('User Role')
    email_field: str = TextField(label='User Name')
    precinct_field: str = TextField(label='Precinct')
    date_edited_field: str = DateField(label='Date Edited')
    submit = SubmitField('Edit')
