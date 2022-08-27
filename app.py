from incident_app import app
from incident_app import app_factory  # noqa

# app = app_factory()
# app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True)
