from incident_app.dictionary_search import float_validation, tuple_validation, tup_list_validation
from incident_app.models.incident import Incident
from incident_app.models.user import User
from incident_app.permissions import Permission


# Created by Terrence Hernandez
def routes_handler():
    """
        This function returns a string confirming that routes.py called
        workflow_manager.run(). Serves as a test for a module calling
        workflow_manager.run().

        :return: String (Confirmation)
        """
    return "Hello from workflow_manager"


def action_permission(current_user, action, incident_id, officer_id):
    """
    The function determines which set of rules to call depending on which
    user is attempting the action and what the status of the incident is at
    the time of the attempted action.

    :param current_user: Unique ID number for the user
    :param action: <String> Action to be performed on a particular incident
    :param incident_id: Unique ID number of the incident
    :param officer_id: Unique ID of the officer
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """

    # Query the DB to locate the incident the action is to be performed on
    incident = Incident.query.filter_by(id=incident_id, officer=officer_id).first()

    # Query the db to get the current user object
    user = User.query.filter_by(id=current_user).first()

    # Get the list of incidents the current user has assisted on
    user_assists = user.assists

    # Initialize the variable that indicates if the current user was the
    # assisting officer to the incident the action is to be performed on.
    assisting_officer = False

    if user_assists:
        # Iteration through the list of incidents the current user has assisted on
        for incidents in user_assists:
            if incidents.id == incident_id:
                assisting_officer = True
                break

    # Get the assigned role integer of the current user
    role = user.role

    # Use the role integer to determine role title  (Trooper | Supervisor | Other)
    # Assign role string value to current_user variable
    if role == 1:
        current_user = "Trooper"
    elif role == 2:
        current_user = "Supervisor"
    else:
        current_user = "Other"

    # If the incident does not exist, deny any action
    if incident is None:
        permission = False
    else:
        # Else, get the status of the located incident
        status = incident.status

        # If current user is the assisting officer, allow "view" action only
        if assisting_officer:
            # If action is "view", check permissions of user to view incident
            if action == "view":
                permission = Permission(current_user, action, status).view()
            else:
                # Else, any other action by an assisting officer is denied
                permission = False
        else:
            # Else, current user is not the assisting officer of the incident
            # Determine which action is being attempted and determine
            # which class method (permissions) are to be called.
            if action == "view":
                permission = Permission(current_user, action, status).view()
            elif action == "edit":
                permission = Permission(current_user, action, status).edit()
            elif action == "print":
                permission = Permission(current_user, action, status).print()
            else:
                permission = False

    # Return the determined boolean value to the calling component
    return permission


def draw_permission(current_user, action, incident_id, officer_id, measurements):
    """
    This function servers to determine two things, if the current user is
    permitted to execute the draw component given the current state/status
    of an incident, and if the draw component is permitted to execute given
    the validity of the measurement data obtained from the scene of the accident.

    :param current_user: Unique ID number for the user
    :param action: <String> Action to be performed on a particular incident
    :param incident_id: Unique ID number of the incident
    :param officer_id: Unique ID of the officer
    :param measurements: Measurement dictionary containing measurements
    obtained from the accident scene
    :return:
    """

    # Initialize draw permission variable
    permission_draw = False

    # Query the DB to locate the incident the draw component is to execute on
    incident = Incident.query.filter_by(id=incident_id, officer=officer_id).first()

    # Query the db to get the current user object
    user = User.query.filter_by(id=current_user).first()

    # Get the list of incidents the current user has assisted on
    user_assists = user.assists

    # Initialize the variable that indicates if the current user was the
    # assisting officer to the incident the action is to be performed on.
    assisting_officer = False

    if user_assists:
        # Iteration through the list of incidents the current user has assisted on
        for incidents in user_assists:
            if incidents.id == incident_id:
                assisting_officer = True
                break

    # Get the assigned role integer of the current user
    role = user.role

    # Use the role integer to determine role title  (Trooper | Supervisor | Other)
    # Assign role string value to current_user variable
    if role == 1:
        current_user = "Trooper"
    elif role == 2:
        current_user = "Supervisor"
    else:
        current_user = "Other"

    # If the incident does not exist, deny draw permission and component execution
    if incident is None:
        permission_draw = False
    else:
        # If the incident does exist, get the status of the located incident
        status = incident.status
        # If current user is the assisting officer, deny draw permission
        if assisting_officer:
            permission = False
        else:
            # Else, determine if the current user is allowed to draw given the state
            # of the report, then determine if the data received is valid for drawing
            if action == "draw":
                # Determines if the user is able to draw given the current status
                # of the located incident
                permission_draw = Permission(current_user, action, status).draw()

                # If the user is not allowed to draw given the current state of the
                # located incident, return False, prompting a draw denial.
                if not permission_draw:
                    permission_draw = False
                else:

                    # Iteration through the measurements dictionary to find invalid data
                    for key, value in measurements.items():

                        # Item is of type float
                        if type(value) == float:
                            # Validate if float data is valid
                            float_test = float_validation(value)
                            if float_test:
                                # Float data is valid, continue iteration through dictionary
                                continue
                            else:
                                # Float not valid, set permission to False
                                permission_draw = float_test

                        # Item is of type tuple
                        elif type(value) == tuple:
                            # Validate if tuple data is valid
                            tup_test = tuple_validation(value)
                            if tup_test:
                                # Tuple data is valid, continue iteration through dictionary
                                continue
                            else:
                                # Tuple data not valid, set permission to False
                                permission_draw = False

                        # Item is of type list
                        elif type(value) == list:
                            # Validate if list data is valid
                            list_test = tup_list_validation(value)
                            if list_test:
                                # List data is valid, continue iteration through dictionary
                                continue
                            else:
                                # List data not valid, set permission to False
                                permission_draw = False

                        else:
                            # If data is not of type float, tuple, list, set permission to
                            # false, execute break statement to stop iteration through the
                            # dictionary.
                            permission_draw = False
                            break
            else:
                # Any other action other than draw calling this method will
                # prompt an draw component execution denial.
                permission_draw = False

    return permission_draw