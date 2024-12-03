def mapl(func, iterable):
    return list(map(func, iterable))


def map_to_numbers(iterable: list[str]) -> list[int]:
    return list(_map_to_numbers(iterable))


def _map_to_numbers(iterable: list[str]) -> list[int]:
    return map(int, iterable)


def sub_map_to_numbers(iterable: list[list[str]]) -> list[list[int]]:
    return mapl(map_to_numbers, iterable)
