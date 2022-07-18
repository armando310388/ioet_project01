import unittest
import os
import io
import sys
from unittest.mock import patch
from tools import SingleEmployeeData
from exceptions import DataStructureError, DuplicatedDayError, InvalidHourError, LimitHourError
from main import full_calculate_payment


class TestTools(unittest.TestCase):
    def setUp(self):
        self.employee_hours = {
            'MO': [10, 12],
            'TU': [10, 12],
            'TH': [1, 3],
            'SA': [14, 18],
            'SU': [20, 21]
        }
        self.full_day_hours = {
            'MO': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'TU': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'TH': [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'SA': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            'SU': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        }

    def test_extract_hours_and_name(self):
        single_data = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2
        employee_data = SingleEmployeeData(single_data, single_data_line_number)
        employee_name, employee_hours = employee_data._extract_hours_and_name()
        expected_employee_hours = ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00']
        self.assertEqual(employee_name, 'RENE')
        self.assertEqual(employee_hours, expected_employee_hours)

    @patch('tools.SingleEmployeeData.__init__')
    def test_extract_limit_hours_and_days(self, mock_single_employee_data):
        expected_result = self.employee_hours

        mock_single_employee_data.return_value = None
        employee_data = 'some_data'
        single_employee_data = SingleEmployeeData(employee_data)
        single_employee_data.employee_hours = [
            'MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00'
        ]
        single_employee_data.line_number = 2

        result = single_employee_data._limit_hours_and_days()
        self.assertEqual(result, expected_result)

    def test_validate_data_hour_not_rounded(self):
        single_data = 'RENE=MO10:00-12:01,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            single_employee_data = SingleEmployeeData(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data does not have the specified structure.')

    @patch('tools.SingleEmployeeData.__init__')
    def test_validate_data_duplicated_day(self, mock_single_employee_data):
        mock_single_employee_data.return_value = None
        employee_data = 'some_data'
        single_employee_data = SingleEmployeeData(employee_data)
        single_employee_data.employee_hours = [
            'MO10:00-12:00', 'MO10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00'
        ]
        single_employee_data.line_number = 2

        with self.assertRaises(DuplicatedDayError) as context:
            result = single_employee_data._limit_hours_and_days()
        self.assertEqual(context.exception.msg, 'Data in line 2 has a duplicated day.')

    def test_validate_data_bad_day(self):
        single_data = 'RENE=OM10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            single_employee_data = SingleEmployeeData(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data does not have the specified structure.')

    def test_validate_data_empty_with_name(self):
        single_data = 'RENE='
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            single_employee_data = SingleEmployeeData(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data does not have the specified structure.')

    def test_validate_data_without_name(self):
        single_data = 'MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            single_employee_data = SingleEmployeeData(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data does not have the specified structure.')

    def test_validate_data_without_name_with_equal(self):
        single_data = '=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            single_employee_data = SingleEmployeeData(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data does not have the specified structure.')

    def test_validate_data_ends_with_comma(self):
        single_data = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00,'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            single_employee_data = SingleEmployeeData(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data does not have the specified structure.')

    def test_validate_data_single_hour_ends_with_comma(self):
        single_data = 'RENE=MO10:00-12:00,'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            single_employee_data = SingleEmployeeData(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data does not have the specified structure.')

    @patch('tools.SingleEmployeeData.__init__')
    def test_validate_data_bad_hour(self, mock_single_employee_data):
        mock_single_employee_data.return_value = None
        employee_data = 'some_data'
        single_employee_data = SingleEmployeeData(employee_data)
        single_employee_data.employee_hours = [
            'MO10:00-25:00', 'MO10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00'
        ]
        single_employee_data.line_number = 2

        with self.assertRaises(InvalidHourError) as context:
            result = single_employee_data._limit_hours_and_days()
        self.assertEqual(context.exception.msg, 'Data in line 2 has an invalid hour.')

    @patch('tools.SingleEmployeeData.__init__')
    def test_validate_data_bad_limits(self, mock_single_employee_data):
        mock_single_employee_data.return_value = None
        employee_data = 'some_data'
        single_employee_data = SingleEmployeeData(employee_data)
        single_employee_data.employee_hours = [
            'MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-11:00'
        ]
        single_employee_data.line_number = 2

        with self.assertRaises(LimitHourError) as context:
            result = single_employee_data._limit_hours_and_days()
        self.assertEqual(
            context.exception.msg,
            'Data in line 2 has an invalid limit hour. Start hour must be less than the end hour.'
        )

    @patch('tools.SingleEmployeeData.__init__')
    @patch('tools.SingleEmployeeData._limit_hours_and_days')
    def test_convert_data_day_to_list(self, mock_limit_hours_and_days, mock_single_employee_data):
        expected_result = self.full_day_hours

        mock_single_employee_data.return_value = None
        employee_data = 'some_data'
        single_employee_data = SingleEmployeeData(employee_data)

        mock_limit_hours_and_days.return_value = self.employee_hours

        result = single_employee_data._hours_lists()
        self.assertEqual(result, expected_result)

    @patch('tools.SingleEmployeeData.__init__')
    @patch('tools.SingleEmployeeData._hours_lists')
    def test_calculate_amount(self, mock_hours_lists, mock_single_employee_data):
        mock_single_employee_data.return_value = None
        employee_data = 'some_data'
        single_employee_data = SingleEmployeeData(employee_data)

        mock_hours_lists.return_value = self.full_day_hours

        result = single_employee_data.calculate_amount()
        self.assertEqual(result, 215)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.main_folder = os.path.dirname(os.path.abspath(__file__))
        self.data_without_error = self.main_folder + '/fixtures/full_correct_data.txt'
        self.data_with_error = self.main_folder + '/fixtures/full_not_correct_data.txt'

    def test_calculate_payment(self):
        expected_result = 'The amount to pay RENE is: 215 USD\n' \
                          'The amount to pay CARL is: 170 USD\n' \
                          'The amount to pay JULIO is: 110 USD\n' \
                          'The amount to pay ARMANDO is: 415 USD\n' \
                          'The amount to pay JOSE is: 165 USD\n' \
                          'The amount to pay IVAN is: 105 USD\n' \
                          'The amount to pay JORGE is: 185 USD\n'
        captured_output = io.StringIO()
        sys.stdout = captured_output
        full_calculate_payment(self.data_without_error)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), expected_result)

    def test_calculate_payment_error(self):
        expected_result = 'The amount to pay RENE is: 215 USD\n' \
                          'The amount to pay CARL is: 170 USD\n' \
                          'The amount to pay JULIO is: 110 USD\n'

        captured_output = io.StringIO()
        sys.stdout = captured_output
        with self.assertRaises(InvalidHourError) as context:
            full_calculate_payment(self.data_with_error)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), expected_result)


if __name__ == '__main__':
    unittest.main()
