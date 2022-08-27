
# Created by Terrence Hernandez


def supervisor_edit(status):
    """
    Function serves as editing permissions for a supervisor user
    :param status: <String> Status of the incident
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """
    if (
            status == "underSuperReview"
            or status == "approvedBySuper"
            or status == "rejectedBySuper"
            or status == "pendingDmvReview"
            or status == "rejectedByDmv"
    ):
        # Supervisor is allowed to edit incident
        permission = True
    else:
        # Supervisor not allowed to edit incident
        permission = False

    return permission


def supervisor_view(status):
    """
    Function serves as the viewing permissions for a supervisor user
    :param status: <String> Status of the incident
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """
    if status == "underDmvReview":
        # Supervisor is not allowed to view incident
        permission = False
    else:
        # Supervisor is allowed to view the incident
        permission = True
    return permission


def supervisor_print(status):
    """
    Function serves as the printing permissions for a supervisor user
    :param <String> Status of the incident
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """
    # Supervisor is allowed to print incident
    if status == "underDmvReview":
        permission = False
    else:
        # Supervisor is not allowed to print
        permission = True
    return permission


def supervisor_draw(status):
    """
    Function serves as the drawing permissions for a supervisor user
    :param  <String> Status of the incident
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """
    if (
            status == "underSuperReview"
            or status == "rejectedBySuper"
            or status == "pendingDmvReview"
            or status == "rejectedByDmv"
    ):
        # Supervisor is allowed to draw
        permission = True
    else:
        # Supervisor is not allowed to draw
        permission = False
    return permission
