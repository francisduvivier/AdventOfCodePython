import time

from util import map_to_numbers

tInput = open('day07-testinput.txt').read().strip()
rInput = open('day07-input.txt').read().strip()

def parseInput(input):
    lines = input.splitlines()
    equations = [line.split(': ') for line in lines]
    equations = [(float(left), map_to_numbers(right.split(' '))) for (left, right) in equations]

    return equations


operators = ['+', '*']


def invert_operator(left, last, operator):
    if operator == '+':
        return left - last
    if operator == '*':
        return left / last
    return None


def apply_operator(left, right, operator):
    if operator == '+':
        return left + right
    if operator == '*':
        return left * right
    pass


def fill_operators_rec(left: float, right: list[int]) -> None or list[str]:
    global operators
    if left < 0:
        return None
    if not left.is_integer():
        return None
    if len(right) == 1:
        return [] if left == right[0] else None

    for operator in operators:
        new_left = invert_operator(left, right[-1], operator)
        solution = fill_operators_rec(new_left, right[:-1])
        if solution is not None:
            return [operator] + solution
    return None


def part1(input):
    equations = parseInput(input)
    result = int(sum([left for (left, right) in equations if fill_operators_rec(left, right) is not None]))

    print(result)
    return result


assert part1(tInput) == 3749
part1(rInput)
