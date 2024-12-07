import time

from util import map_to_numbers

tInput = open('day07-testinput.txt').read().strip()
rInput = open('day07-input.txt').read().strip()


def parseInput(input):
    lines = input.splitlines()
    equations = [line.split(': ') for line in lines]
    equations = [(float(left), map_to_numbers(right.split(' '))) for (left, right) in equations]

    return equations


def invert_operator(left, last, operator):
    if operator == '+':
        return left - last
    if operator == '*':
        return left / last
    if operator == '||':
        cut_off = str(int(left))[: -len(str(last))]
        cut_off = '0' if cut_off == '' else cut_off
        return float(cut_off if str(int(left)).endswith(str(last)) else -1)
    return None


def fill_operators_rec(left: float, right: list[int], operators) -> None or list[str]:
    if left < 0:
        return None
    if not left.is_integer():
        return None
    if len(right) == 1:
        return [] if left == right[0] else None

    for operator in operators:
        new_right = right[:-1]
        new_left = invert_operator(left, right[-1], operator)
        solution = fill_operators_rec(new_left, new_right, operators)
        if solution is not None:
            return [operator] + solution
    return None


def part1(input):
    equations = parseInput(input)
    operators_part1 = ['+', '*']
    result = int(
        sum([left for (left, right) in equations if fill_operators_rec(left, right, operators_part1) is not None]))
    print(result)
    return result


# assert part1(tInput) == 3749
# part1(rInput)


def part2(input):
    equations = parseInput(input)
    operators_part2 = ['+', '*', '||']
    result = int(
        sum([left for (left, right) in equations if fill_operators_rec(left, right, operators_part2) is not None]))

    print(result)
    return result


assert part2(tInput) == 11387
part2(rInput)
