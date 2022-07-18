import re

from exceptions import DataStructureError, LimitHourError, DuplicatedDayError, InvalidHourError


class SingleData:
    """Class for manage the data of an employee"""
    def __get__(self, instance, owner=None):
        """Method which returns the data of an employee"""
        return self.value

    def __set__(self, instance, value):
        """Method which validates the data of an employee"""
        general_matched = re.fullmatch(
            '[a-zA-Z]+=((MO|TU|WE|TH|FR|SA|SU)\d{2}:00-\d{2}:00,)*(MO|TU|WE|TH|FR|SA|SU)\d{2}:00-\d{2}:00\n?',
            value
        )

        if not general_matched:
            raise DataStructureError

        self.value = value


class SingleEmployeeData:
    """Class for manage a single employee data"""
    single_data = SingleData()

    def __init__(self, single_data: str, line_number: int) -> None:
        self.single_data = single_data
        self.line_number = line_number
        self.employee_name, self.employee_hours = self._extract_hours_and_name()

    def _extract_hours_and_name(self) -> (str, list):
        employee_name_and_hours = self.single_data.split('=')
        employee_name = employee_name_and_hours[0]
        string_with_hours = employee_name_and_hours[1]
        employee_hours = string_with_hours.split(',')

        return employee_name, employee_hours

    def _limit_hours_and_days(self) -> dict:
        """Method for converting the 'XXHH:MM-HH:MM' list from a employee to a XX: [initial, end] dictionary"""
        result = {}
        for day_data in self.employee_hours:
            day = day_data[:2]
            if day in result:
                raise DuplicatedDayError(self.line_number)
            initial_hour, end_hour = int(day_data[2:4]), int(day_data[8:10])
            if 0 <= initial_hour < 23 and 0 <= end_hour < 23:
                if initial_hour < end_hour:
                    result[day] = [initial_hour, end_hour]
                else:
                    raise LimitHourError(self.line_number)
            else:
                raise InvalidHourError(self.line_number)
        return result

    def _hours_lists(self) -> dict:
        """Method for converting the [initial, end] data from a employee to full 24 hours lists"""
        result = {}
        days_limits = self._limit_hours_and_days()
        for day in days_limits:
            initial_hour = days_limits[day][0]
            end_hour = days_limits[day][1]
            result[day] = [1 if initial_hour <= i < end_hour else 0 for i in range(24)]
        return result

    def calculate_amount(self) -> int:
        """Method for calculating the amount to pay for a employee"""
        full_day_employee_hours = self._hours_lists()

        payment_per_hour = {
            'MO': [25, 25, 25, 25, 25, 25, 25, 25, 25, 15, 15, 15, 15, 15, 15, 15, 15, 15, 20, 20, 20, 20, 20, 20],
            'TU': [25, 25, 25, 25, 25, 25, 25, 25, 25, 15, 15, 15, 15, 15, 15, 15, 15, 15, 20, 20, 20, 20, 20, 20],
            'WE': [25, 25, 25, 25, 25, 25, 25, 25, 25, 15, 15, 15, 15, 15, 15, 15, 15, 15, 20, 20, 20, 20, 20, 20],
            'TH': [25, 25, 25, 25, 25, 25, 25, 25, 25, 15, 15, 15, 15, 15, 15, 15, 15, 15, 20, 20, 20, 20, 20, 20],
            'FR': [25, 25, 25, 25, 25, 25, 25, 25, 25, 15, 15, 15, 15, 15, 15, 15, 15, 15, 20, 20, 20, 20, 20, 20],
            'SA': [30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 20, 20, 20, 20, 20, 20, 20, 20, 25, 25, 25, 25, 25, 25],
            'SU': [30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 20, 20, 20, 20, 20, 20, 20, 20, 25, 25, 25, 25, 25, 25]
        }

        total_amount = 0

        for day in full_day_employee_hours:
            for i, j in zip(full_day_employee_hours[day], payment_per_hour[day]):
                total_amount += i * j

        return total_amount
