from datetime import datetime


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


a = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]
if __name__ == "__main__":
    print(filter_by_state(a))
