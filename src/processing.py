def filter_by_state(my_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей и возвращает новый список словарей"""
    new_list = []
    for my in my_list:
        if "state" in my and my["state"] == state:
            new_list.append(my)
    return new_list


def sort_by_date(my_list: list[dict], type_sort: bool = True) -> list[dict]:
    """Функция принимает список словарей и возвращает новый список словарей отсортированный по умолчанию — убывание"""
    new_list = sorted(my_list, key=lambda a: a["date"], reverse=type_sort)

    return new_list
