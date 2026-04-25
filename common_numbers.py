def common_numbers(list_1: list , list_2: list) -> list:

    """
     Написать функцию, которая получает на вход два списка чисел и
     возвращает новый список, содержащий только те числа, которые
     встречаются в обоих списках.

        Пример ввода:
        [1, 2, 3, 4], [3, 4, 5, 6]

        Пример вывода:
        [3, 4]

    """

    result = []
    for num1 in list_1:
        if num1 not in result and num in list_2:
            result.append(num)

        return result


