import unittest
from tools import validate_data, extract_data_day, convert_data_day_to_list, calculate_amount


class TestTools(unittest.TestCase):
    def test_validate_data(self):
        single_data = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        result = validate_data(single_data)
        self.assertTrue(result)

    def test_validate_data_duplicated_day(self):
        single_data = 'RENE=MO10:00-12:00,MO10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        result = validate_data(single_data)
        self.assertFalse(result)

    def test_validate_data_bad_day(self):
        single_data = 'RENE=MA10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        result = validate_data(single_data)
        self.assertFalse(result)

    def test_validate_data_empty_with_name(self):
        single_data = 'RENE='
        result = validate_data(single_data)
        self.assertFalse(result)

    def test_validate_data_without_name(self):
        single_data = 'MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        result = validate_data(single_data)
        self.assertFalse(result)

    def test_validate_data_without_name_with_equal(self):
        single_data = '=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        result = validate_data(single_data)
        self.assertFalse(result)

    def test_validate_data_bad_hour(self):
        single_data = 'RENE=MO10:00-25:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        result = validate_data(single_data)
        self.assertFalse(result)

    def test_validate_data_bad_limits(self):
        single_data = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-11:00,SU20:00-21:00'
        result = validate_data(single_data)
        self.assertFalse(result)

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
        data_matrix = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        ]
        result = calculate_amount(data_matrix)
        self.assertEqual(result, 215)


if __name__ == '__main__':
    unittest.main()