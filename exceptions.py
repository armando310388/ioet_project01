class DataStructureError(Exception):
    """
    Exception raised for errors when single data does not have the specified structure

    Attributes:
        line_number -- Line number of the file where the error was found
    """

    def __init__(self):
        self.msg = f'Data does not have the specified structure.'

    def __str__(self):
        return self.msg


class DuplicatedDayError(Exception):
    """
    Exception raised for errors when single data contains a duplicated day

    Attributes:
        line_number -- Line number of the file where the error was found
    """

    def __init__(self, line_number):
        self.msg = f'Data in line {line_number} has a duplicated day.'

    def __str__(self):
        return self.msg


class InvalidHourError(Exception):
    """
    Exception raised for errors when single data contains an invalid hour

    Attributes:
        line_number -- Line number of the file where the error was found
    """

    def __init__(self, line_number):
        self.msg = f'Data in line {line_number} has an invalid hour.'

    def __str__(self):
        return self.msg


class LimitHourError(Exception):
    """
    Exception raised for errors when single data contains an invalid limit hour

    Attributes:
        line_number -- Line number of the file where the error was found
    """

    def __init__(self, line_number):
        self.msg = f'Data in line {line_number} has an invalid limit hour. Start hour must be less than the end hour.'

    def __str__(self):
        return self.msg
