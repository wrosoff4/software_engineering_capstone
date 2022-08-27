# Created by Andrew Davison
class Measurement:
    measurement_name: str = None
    measurement_type: str = None
    measurement: float or tuple = None

    def __init__(self, measurement_name, measurement_type, measurement):
        self.measurement_name = measurement_name
        self.measurement_type = measurement_type
        if measurement_type == 'distance' and (type(measurement) == float or type(measurement) == int):
            self.measurement = float(measurement)
        elif measurement_type == 'distance' and type(measurement) == tuple:
            self.measurement = self.__convert_measurement(measurement)
        elif measurement_type == 'weight':
            self.measurement = float(measurement)

    def __str__(self):
        if self.measurement_type == 'distance':
            return f'Name: {self.measurement_name} - Type: {self.measurement_type} -> {self.measurement} ft.'
        elif self.measurement_type == 'weight':
            return f'Name: {self.measurement_name} - Type: {self.measurement_type} -> {self.measurement} lbs.'
        else:
            raise TypeError("Measurement is of incorrect type")

    @staticmethod
    def __convert_measurement(measurement):
        """
        Converts tuple of feet and inches to a float in terms of feet.

        :return: float in terms of feet
        """
        return measurement[0] + measurement[1] / 12

    def __set_measurement_name(self, measurement_name):
        """
        Setter for measurement name.
        """
        self.measurement_name = measurement_name

    def __set_measurement_type(self, measurement_type):
        """
        Setter for measurement type. Raises TypeError if not of type distance or weight.
        """
        if measurement_type == 'distance' or measurement_type == 'weight':
            self.measurement_type = measurement_type
        else:
            raise TypeError("Measurement is of incorrect type")

    def __set_measurement(self, measurement):
        """
        Setter for measurement.
        """
        if self.measurement_type == 'distance' and (type(measurement) == float or type(measurement) == int):
            self.measurement = float(measurement)
        elif self.measurement_type == 'distance' and type(measurement) == tuple:
            self.measurement = self.__convert_measurement(measurement)
        elif self.measurement_type == 'weight':
            self.measurement = float(measurement)

    def get_measurement_name(self):
        """
        Getter for measurement name.

        :return: measurement name.
        """
        return self.measurement_name

    def get_measurement_type(self):
        """
        Getter for measurement type.

        :return: measurement type, distance or weight.
        """
        return self.measurement_type

    def get_measurement(self):
        """
        Getter for measurement.

        :return: measurement.
        """
        return self.measurement
