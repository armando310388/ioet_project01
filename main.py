import re
import sys
from exceptions import FileTypeError
from tools import SingleEmployeeData


def check_file(data_path: str) -> bool:
    """Method for checking if the file is a txt file"""
    matched = re.findall(
        '\.txt\Z',
        data_path
    )
    return bool(matched)


def full_calculate_payment(data_path: str) -> None:
    """Method for calculating all the payment values for the employees in a file"""
    result = ''
    line_number = 0
    employees_names = set()
    show_employees_payment = True
    try:
        with open(data_path, mode='r') as file:
            for line in file:
                line_number += 1
                single_data = line
                single_employee_data = SingleEmployeeData(single_data, line_number)
                if single_employee_data.employee_name in employees_names:
                    print(f'Error: The employee {single_employee_data.employee_name} appears more than once.')
                    show_employees_payment = False
                    break
                else:
                    employees_names.add(single_employee_data.employee_name)
                    payment = single_employee_data.calculate_amount()
                    result += f'The amount to pay {single_employee_data.employee_name} is: {payment} USD\n'
        if show_employees_payment:
            if line_number >= 5:
                print(result)
            else:
                print('The file must have at least five sets of data.')
    except FileNotFoundError:
        print("Error: The file wasn't found.")


if __name__ == '__main__':
    sys.tracebacklimit = 0

    file_path = input('Enter data file path: ')
    file_path_clean = file_path.strip()
    if check_file(file_path_clean):
        full_calculate_payment(file_path_clean)
    else:
        raise FileTypeError
