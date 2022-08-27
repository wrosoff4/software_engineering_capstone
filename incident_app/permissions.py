from incident_app import trooper_permissions, supervisor_permissions

# Created by Terrence Hernandez


class Permission:
    """
    Creates models of type Permission with attributes title, action and status.
    Each instance of a user attempting an action given a certain status of a
    of an incident is used to create a Permission object. The values in the
    Permission object are evaluated to determine the action eligibility of the
    user of that object create.
    """

    def __init__(self, title="", action="", status=""):
        self.title = title
        self.action = action
        self.status = status

    def view(self):
        """
        Class method is called when a user wants to view an incident.
        The user attempting this action dictates which permissions
        are used to determine action eligibility.
        :return: <Boolean> True if action is permitted | False is action is not permitted
        """
        # If trooper, use trooper viewing permissions
        if self.title == "Trooper":
            return trooper_permissions.trooper_view(self.status)

        # If supervisor, use supervisor viewing permissions
        elif self.title == "Supervisor":
            return supervisor_permissions.supervisor_view(self.status)

        # Anyone other than trooper/supervisor viewing is denied
        else:
            return False

    def edit(self):
        """
        Class method is called when a user wants to edit an incident.
        The user attempting this action dictates which permissions
        are used to determine action eligibility.
        :return: <Boolean> True if action is permitted | False is action is not permitted
        """
        # If trooper, use trooper editing permissions
        if self.title == "Trooper":
            return trooper_permissions.trooper_edit(self.status)

        # If supervisor, use supervisor editing permissions
        elif self.title == "Supervisor":
            return supervisor_permissions.supervisor_edit(self.status)

        # Anyone other than trooper/supervisor editing is denied
        else:
            return False

    def print(self):
        """
        Class method is called when a user wants to print an incident.
        The user attempting this action dictates which permissions
        are used to determine action eligibility.
        :return: <Boolean> True if action is permitted | False is action is not permitted
        """
        # If trooper, use trooper printing permissions
        if self.title == "Trooper":
            return trooper_permissions.trooper_print(self.status)

        # If supervisor, use supervisor printing permissions
        elif self.title == "Supervisor":
            return supervisor_permissions.supervisor_print(self.status)

        # Anyone other than trooper/supervisor printing is denied
        else:
            return False

    def draw(self):
        """
        Class method is called when a user wants to draw an incident image
        for an incident. The user attempting this action dictates which
        permissions are used to determine action eligibility.
        :return: <Boolean> True if action is permitted | False is action is not permitted
        """
        # If trooper, use trooper drawing permissions
        if self.title == "Trooper":
            return trooper_permissions.trooper_draw(self.status)

        # If supervisor, use supervisor drawing permissions
        elif self.title == "Supervisor":
            return supervisor_permissions.supervisor_draw(self.status)

        # Anyone other than trooper/supervisor drawing is denied
        else:
            return False
