from src.schemas import Order, Project


def get_object_by_input(input_data: int) -> tuple | None | int:
    try:
        initial_input = int(input_data)
    except ValueError:
        print("Введите число, пожалуйста!")
        return None
    if initial_input == 0:
        print('Спасибо, всего хорошего!')
        return 0
    elif initial_input > 2 or initial_input < 0:
        print('Введите корректное число!')
    return (Order, 'Договор') if initial_input == 1 else (Project, 'Проект')


def get_approve_status():
    is_approved = input('Подтвердите создание договора [Y/n]')
    status = None
    while status is None:
        if is_approved != 'Y':
            print('Введите корректное значение - Y или n!')
            continue
        status = False if is_approved == 'n' else True
    return status
