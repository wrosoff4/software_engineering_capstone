from flask import Flask
# from flask_moment import Moment
from flask_login import LoginManager  # noqa
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy  # noqa

from incident_app.config import Config

# USE THIS BLOCK FOR SINGLE INSTANCE
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message = "Please log in before proceeding"
login_manager.login_message_category = "warning"

# USE THIS BLOCK FOR APP_FACTORY AND MULTIPLE INSTANCES
# db = SQLAlchemy()
# migrate = Migrate()


# import the models, blueprints
from incident_app.models import user, vehicle, incident, person, object  # noqa
from incident_app.main.routes import main  # noqa
from incident_app.report_manager.routes import report_manager  # noqa
from incident_app.hr_ops.routes import hr  # noqa


# ONLY USE THESE FOR SINGLE INSTANCE OPTION
app.register_blueprint(main)
app.register_blueprint(report_manager)
app.register_blueprint(hr)


def app_factory(config_file=Config):
    this_app = Flask(__name__)
    this_app.config.from_object(config_file)

    db.init_app(this_app)
    migrate.init_app(this_app, db, render_as_batch=True)
    login_manager.init_app(app)

    this_app.register_blueprint(main)
    this_app.register_blueprint(report_manager)
    this_app.register_blueprint(hr)

    return this_app
