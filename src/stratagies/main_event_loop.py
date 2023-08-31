from src.schemas import Order
from src.service import get_object_by_input, get_approve_status

from .object_stratagies import run_order_strategy, run_project_stategy


def run_loop():
    print('Вы хотите создать договор (1) или проект (2)? Выберите 1 или 2 напишите в терминале. Чтобы выйти нажмите 0')
    while True:
        initial_input = input('Введите цифру: ')
        data = get_object_by_input(initial_input)
        if isinstance(data, tuple):
            object_type, object_type_name = data
            print(f"Вы выбрали создать {object_type_name}")
            object_name = input('Введите название договора (не более 100 символов): ')
            if object_type is Order:
                order = Order(name=object_name)
                is_approved: bool = get_approve_status()
                if not is_approved:
                    continue
                # TODO
            else:
                run_project_stategy()
        else:
            if isinstance(data, int):
                break
            continue
