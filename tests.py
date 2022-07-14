import unittest
from tools import validate_data, extract_data_day, convert_data_day_to_list, calculate_amount
from exceptions import DataStructureError, DuplicatedDayError, InvalidHourError, LimitHourError


class TestTools(unittest.TestCase):
    def test_validate_data(self):
        single_data = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2
        validate_data(single_data, single_data_line_number)

    def test_validate_data_duplicated_day(self):
        single_data = 'RENE=MO10:00-12:00,MO10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DuplicatedDayError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data in line 2 has a duplicated day.')

    def test_validate_data_bad_day(self):
        single_data = 'RENE=MA10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data in line 2 does not have the specified structure.')

    def test_validate_data_empty_with_name(self):
        single_data = 'RENE='
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data in line 2 does not have the specified structure.')

    def test_validate_data_without_name(self):
        single_data = 'MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data in line 2 does not have the specified structure.')

    def test_validate_data_without_name_with_equal(self):
        single_data = '=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data in line 2 does not have the specified structure.')

    def test_validate_data_ends_with_comma(self):
        single_data = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00,'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data in line 2 does not have the specified structure.')

    def test_validate_data_single_hour_ends_with_comma(self):
        single_data = 'RENE=MO10:00-12:00,'
        single_data_line_number = 2

        with self.assertRaises(DataStructureError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data in line 2 does not have the specified structure.')

    def test_validate_data_bad_hour(self):
        single_data = 'RENE=MO10:00-25:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(InvalidHourError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(context.exception.msg, 'Data in line 2 has an invalid hour.')

    def test_validate_data_bad_limits(self):
        single_data = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-11:00,SU20:00-21:00'
        single_data_line_number = 2

        with self.assertRaises(LimitHourError) as context:
            validate_data(single_data, single_data_line_number)
        self.assertEqual(
            context.exception.msg,
            'Data in line 2 has an invalid limit hour. Start hour must be less than the end hour.'
        )

    def test_extract_data_day_single_hour(self):
        single_data = 'RENE=MO10:00-12:00'
        result = extract_data_day(single_data)
        expected_result = ['MO10:00-12:00']
        self.assertEqual(result, expected_result)

    def test_extract_data_day(self):
        single_data = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        result = extract_data_day(single_data)
        expected_result = ['MO10:00-12:00', 'TU10:00-12:00', 'TH01:00-03:00', 'SA14:00-18:00', 'SU20:00-21:00']
        self.assertEqual(result, expected_result)

    def test_convert_data_day_to_list(self):
        data_day = 'MO10:00-12:00'
        expected_result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = convert_data_day_to_list(data_day)
        self.assertEqual(result, expected_result)

    def test_calculate_amount(self):
        data = {
            'MO': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'TU': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'TH': [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'SA': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            'SU': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        }
        result = calculate_amount(data)
        self.assertEqual(result, 215)


if __name__ == '__main__':
    unittest.main()