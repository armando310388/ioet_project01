def validate_data(single_data: str) -> bool:
    """Method for validating a given single data from a employee"""
    pass


def extract_data_day(single_data: str) -> list:
    """Method for extracting each single day data from a single data from a employee"""
    string_with_hours = single_data.split('=')[1]
    return string_with_hours.split(',')


def convert_data_day_to_list(single_data: str) -> list:
    """Method for converting a single day data from a employee to a list based on hours on a single day"""
    initial_hour = int(single_data[2:4])
    end_hour = int(single_data[8:10])
    return [1 if initial_hour <= i < end_hour else 0 for i in range(24)]


def calculate_amount(data: dict) -> int:
    """Method for calculating the amount to pay for a employee"""
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

    for day in data:
        for i, j in zip(data[day], payment_per_hour[day]):
            total_amount += i*j

    return total_amount


