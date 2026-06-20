def log(filename=None):
    """Декоратор log, автоматически логирует начало и конец выполнения функции, ее результаты и возникшие ошибки."""

    def decarator(func):
        def wrapper(*args, **kwargs):
            mes = ""
            try:
                result = func(*args, **kwargs)
                mes = f"{func.__name__} ok\n"
                return result
            except Exception as err:
                mes = f"{func.__name__}: {err}. Inputs: {args}, {kwargs}\n"
            finally:
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(mes)
                else:
                    print(mes)

        return wrapper

    return decarator
