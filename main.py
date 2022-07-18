from tools import SingleEmployeeData


def full_calculate_payment(data_path: str) -> None:
    line_number = 0
    employees_names = set()
    try:
        with open(data_path, mode='r') as file:
            for line in file:
                line_number += 1
                single_data = line
                single_employee_data = SingleEmployeeData(single_data, line_number)
                if single_employee_data.employee_name in employees_names:
                    print(f'Error: The employee {single_employee_data.employee_name} appears more than once.')
                    break
                else:
                    employees_names.add(single_employee_data.employee_name)
                    payment = single_employee_data.calculate_amount()
                    print(f'The amount to pay {single_employee_data.employee_name} is: {payment} USD')
    except FileNotFoundError:
        print("Error: The file wasn't found.")


if __name__ == '__main__':
    file_path = input('Enter data file path: ')
    full_calculate_payment(file_path)
