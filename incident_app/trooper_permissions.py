
# Created by Terrence Hernandez


def trooper_edit(status):
    """
    Function serves as the editing permissions for a trooper user
    :param status: <String> Status of the incident
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """
    if (
            status == "Open"
            or status == "pendingSuperReview"
            or status == "rejectedBySuper"
            or status == "rejectedByDmv"
    ):
        # Trooper is allowed to edit incident
        permission = True
    else:
        # Trooper not allowed to edit incident
        permission = False

    return permission


def trooper_view(status):
    """
    Function serves as the viewing permissions for a trooper
    :param status: <String> Status of the incident
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """

    if (
            status == "underSuperReview"
            or status == "underDmvReview"
    ):
        # Trooper is not allowed to view incident
        permission = False
    else:
        # Trooper is allowed to view the incident
        permission = True
    return permission


def trooper_print(status):
    """
    Function serves as the printing permissions for a trooper user
    :param status: <String> Status of the incident
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """

    if status == "approvedByDmv":
        # Trooper is allowed to print the incident
        permission = True
    else:
        # Trooper is not allowed to print the incident
        permission = False
    return permission


def trooper_draw(status):
    """
    Function serves as the draw permissions for a trooper user
    :param status: <String> Status of the incident
    :return: <Boolean> True if action is permitted | False is action is not permitted
    """

    if (
            status == "Open"
            or status == "pendingSuperReview"
            or status == "rejectedBySuper"
            or status == "rejectedByDmv"
    ):
        # Trooper is allowed to draw
        permission = True
    else:
        # Trooper is not allowed to draw
        permission = False
    return permission
