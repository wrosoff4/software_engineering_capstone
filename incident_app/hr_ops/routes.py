from flask import Blueprint, redirect, render_template, request  # noqa

from incident_app.hr_ops.forms import NewUserForm

hr = Blueprint('hr', __name__)


# hr home page
@hr.route('/hr/home')
@hr.route('/hr')
# @login_required
def hr_home():
    return render_template('hr_ops.html')


# page for creating a new user
@hr.route('/hr/account/new', methods=['GET', 'POST'])
# @login_required
def create_account():
    form = NewUserForm()
    return render_template('new_user.html')
    # user = User()
    # user.id = form.id_field.data
    # user.name = form.name_field.data
    # user.email = form.email_field.data
    # user.password = form.password_field.data
    # user.role = form.role_field.data
    # db.session.add(user)
    # db.session.commit()


# page for search accounts form
@hr.route('/hr/search-accounts', methods=['GET', 'POST'])
# @login_required
def find_user():
    return render_template('hr_ops.html')


# page for editing a user record
@hr.route('/hr/account/edit-account', methods=['GET', 'POST'])
# @login_required
def edit_user():
    return render_template('edit_user.html')


# confirmation page for deleting a user record
@hr.route('/hr/account/delete/confirm', methods=['GET', 'POST'])
# @login_required
def remove_user():
    return render_template('delete_user.html')
