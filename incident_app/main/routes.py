from flask import \
    Blueprint, render_template, request, flash, redirect, url_for, session  # noqa
from sqlalchemy import desc

from incident_app.models.incident import Incident
from incident_app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)


# home page
@main.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    session['logged_in'] = False
    session['user_name'] = None

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.", 'error')
            return redirect(url_for('main.login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(email=username).first()

        if user and user.verify_password(password):
            session['logged_in'] = True
            session['user_name'] = username
            login_user(user)
            return redirect(url_for("main.home_page", username=username))
        else:
            flash("Invalid credentials.", 'error')

    return render_template('login.html', title='Login')


@main.route("/home")
@login_required
def home_page():
    incidents = current_user.incidents.order_by(desc(Incident.severity))
    return render_template('home.html', title='Home', incidents=incidents)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
