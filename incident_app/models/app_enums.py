from enum import Enum


class Severity(Enum):
    PROPERTY_DAMAGE = 1
    BODILY_HARM = 2
    FATALITY = 3
    choices = [PROPERTY_DAMAGE, BODILY_HARM, FATALITY]

    def __repr__(self):
        if self.value == 1:
            return 'Property Damage'
        if self.value == 2:
            return 'Bodily Harm'
        if self.value == 3:
            return 'Fatality'

    def __str__(self):
        if self.value == 1:
            return 'Property Damage'
        if self.value == 2:
            return 'Bodily Harm'
        if self.value == 3:
            return 'Fatality'


class Role(Enum):
    TROOPER = 1
    SUPERVISOR = 2
    HR = 3
    roles = [TROOPER, SUPERVISOR, HR]


class PassengerPosition(Enum):
    DRIVER = 'Driver'
    FRONT_PASSENGER = 'Front Passenger'
    MIDDLE_LEFT = 'Second Row Driver'
    MIDDLE_MIDDLE = 'Second Row Middle'
    MIDDLE_RIGHT = 'Second Row Passenger'
    BACK_LEFT = 'Third Row Driver'
    BACK_MIDDLE = 'Third Row Middle'
    BACK_RIGHT = 'Third Row Passenger'
    OTHER = 'Other'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.value
