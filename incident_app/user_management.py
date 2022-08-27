# Claimed by Will Rosoff
from passlib.hash import pbkdf2_sha256  # noqa

from incident_app import db
from incident_app.models.user import User


def hello():
    """
        Sends back a string saying hello to the world from a lonely, dark component.
        :return: a string saying hello
    """
    return "Hello from UserManager!"


def get_user(user_id: int) -> User:  # noqa
    """
    Retrieves User record matching user_id from db, and returns instance of user
    :param user_id: unique id to search for user with
    :return: User instance for user matching user_id, else raises ValueError
    """
    res = User.query.get(user_id)
    if res:
        return res
    raise ValueError('User not found.')


def add_user(user: User) -> bool:  # noqa
    """
    Takes a user instance (created by hr_operations) and commits it to the database.
    Will check to make sure user is unique.
    If a unique user is passed (all fields will already have been validated, can validate again here),
    it is added and committed to database.
    :param user: User object to be added to the database
    :return: True if added successfully, else raises ValueError
    """
    res = User.query.get(user.id)
    if res:
        raise ValueError('User already exists')
    if None in [user.id, user.name, user.email, user.password, user.role]:
        raise ValueError('Null Fields Not Accepted')
    else:
        db.session.add(user)
        db.session.commit()
    return True


def remove_user(user_id: int) -> bool:  # noqa
    """
    Removes a user record from database
    :param user_id: Unique identifier for user to be removed
    :return: True if user successfully removed, else raises ValueError
    """
    if isinstance(user_id, int):
        res = User.query.get(user_id)
        if res:
            db.session.delete(res)
            db.session.commit()
            return True
        raise ValueError('User does not exist')
    raise ValueError('remove_user expects int value as parameter')


# Individual user attributes can probably be accessed using the login_manager's current_user attribute
# I still placed individual queries here for now
def get_role(user_id: int) -> str:  # noqa
    """
    Searches DB for matching username and retrieves corresponding user's role
    :param user_id: Identifier representing user to search for
    :return: Token identifying user roll if found, or None if no user found
    """
    res = User.query.get(user_id)
    if res:
        return res.role
    raise ValueError('User not found.')


def get_precinct(user_id) -> str:  # noqa
    """
    Returns precinct(s) associated with User record matching user_id
    :param user_id: Unique identifier for user record
    :return: Precinct(s) associated with user, or None if no user found
    """
    pass


def get_subordinates(user_id) -> [User]:  # noqa
    """
    Returns, if any, a list of user id's that correspond to the users, if any, that are under the user matching user_id
    :param user_id: Unique identifier for a supervisor role
    :return: A list of user id's, or an empty list if no subordinates found
    """
    return []
