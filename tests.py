import unittest
from tools import SingleEmployeeData, DataAnalyzer
from exceptions import DataStructureError, DuplicatedDayError, InvalidHourError, LimitHourError


class TestTools(unittest.TestCase):
    def setUp(self) -> None:
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
        employee_name, employee_hours = employee_data.extract_hours_and_name()
        expected_employee_hours = ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00']
        self.assertEqual(employee_name, 'RENE')
        self.assertEqual(employee_hours, expected_employee_hours)

    def test_extract_limit_hours_and_days(self):
        single_data = ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00']
        single_data_line_number = 2
        expected_result = self.employee_hours
        analyzer = DataAnalyzer(single_data_line_number)
        result = analyzer.limit_hours_and_days(single_data)
        self.assertEqual(result, expected_result)

    def test_validate_data_hour_not_rounded(self):
        single_data = 'RENE=MO10:00-12:01,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            single_employee_data = SingleEmployeeData(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data does not have the specified structure.')

    def test_validate_data_duplicated_day(self):
        single_data = ['MO10:00-12:00', 'MO10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00']
        single_data_line_number = 2

        with self.assertRaises(DuplicatedDayError) as context:
            analyzer = DataAnalyzer(single_data_line_number)
            result = analyzer.limit_hours_and_days(single_data)
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

    def test_validate_data_bad_hour(self):
        single_data = ['MO10:00-25:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00']
        single_data_line_number = 2

        with self.assertRaises(InvalidHourError) as context:
            analyzer = DataAnalyzer(single_data_line_number)
            result = analyzer.limit_hours_and_days(single_data)
        self.assertEqual(context.exception.msg, 'Data in line 2 has an invalid hour.')

    def test_validate_data_bad_limits(self):
        single_data = ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-11:00']
        single_data_line_number = 2

        with self.assertRaises(LimitHourError) as context:
            analyzer = DataAnalyzer(single_data_line_number)
            result = analyzer.limit_hours_and_days(single_data)
        self.assertEqual(
            context.exception.msg,
            'Data in line 2 has an invalid limit hour. Start hour must be less than the end hour.'
        )

    def test_convert_data_day_to_list(self):
        single_data = self.employee_hours
        single_data_line_number = 2
        expected_result = self.full_day_hours
        analyzer = DataAnalyzer(single_data_line_number)
        result = analyzer.hours_lists(single_data)
        self.assertEqual(result, expected_result)

    def test_calculate_amount(self):
        single_data = self.full_day_hours
        single_data_line_number = 2
        analyzer = DataAnalyzer(single_data_line_number)
        result = analyzer.calculate_amount(single_data)
        self.assertEqual(result, 215)


if __name__ == '__main__':
    unittest.main()
