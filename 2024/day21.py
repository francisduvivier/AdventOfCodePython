from functools import cache

import numpy as np
from dotmap import DotMap

from grid_robot import find_value, find_value_pos

test_input = open('day21-testinput.txt').read().strip()
real_input = open('day21-input.txt').read().strip()


def parse_input(input):
    lines = input.splitlines()
    return lines


def part1(input):
    codes = parse_input(input)
    code_results = [part1_(code) for code in codes]

    result = sum([res[0] * res[1] for res in code_results])
    print('result', result)
    return result


dirpad_grid = np.array([
    [None, '^', 'A'],
    ['<', 'v', '>']
])
assert dirpad_grid[0][2] == 'A'
assert dirpad_grid[0][0] is None
assert dirpad_grid[1][0] == '<'

numpad_grid = np.array([
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
])

assert numpad_grid[0][0] == '7'
assert numpad_grid[3][0] is None
assert numpad_grid[3][2] == 'A'

DEBUG = True


@cache
def get_pad_letters(from_val, to_val, grid_name: str):
    grid = numpad_grid if grid_name == 'numpad_grid' else dirpad_grid
    order = 'v>^<' if grid[0][0] is None else '^>v<'
    if DEBUG: assert order == 'v>^<' if grid_name == 'dirpad_grid' else '^>v<'
    from_pos = find_value_pos(from_val, grid)
    to_pos = find_value_pos(to_val, grid)
    ydiff = to_pos.y - from_pos.y
    xdiff = to_pos.x - from_pos.x
    letters = []
    if xdiff != 0:
        letters += ['>' if xdiff > 0 else '<' for _ in range(abs(xdiff))]
    if ydiff != 0:
        letters += ['v' if ydiff > 0 else '^' for _ in range(abs(ydiff))]

    sort_key = lambda l: order.index(l)
    sorted_letters = sorted(letters, key=sort_key)
    return ''.join(sorted_letters) + 'A'


assert get_pad_letters('A', 'A', 'dirpad_grid') == 'A'
assert get_pad_letters('A', '<', 'dirpad_grid') == 'v<<A'
assert get_pad_letters('<', 'A', 'dirpad_grid') == '>>^A'
assert get_pad_letters('A', '>', 'dirpad_grid') == 'vA'
assert get_pad_letters('>', 'A', 'dirpad_grid') == '^A'

assert get_pad_letters('0', 'A', 'numpad_grid') == '>A'
assert get_pad_letters('A', '0', 'numpad_grid') == '<A'
assert get_pad_letters('A', '7', 'numpad_grid') == '^^^<<A'
assert get_pad_letters('7', 'A', 'numpad_grid') == '>>vvvA'


@cache
def calc_keys_rec(nb_subrobots: int, keys: str):
    grid_name = 'dirpad_grid'
    if nb_subrobots == 0:
        return keys
    curr_letter = 'A'
    all = ''
    for letter in keys:
        move_letters = get_pad_letters(curr_letter, letter, grid_name)
        all += calc_keys_rec(nb_subrobots - 1, move_letters)
        curr_letter = letter
    return all


start = find_value_pos('A', numpad_grid)
assert start == DotMap({'y': 3, 'x': 2})
assert calc_keys_rec(0, 'A') == 'A'
assert calc_keys_rec(0, '<') == '<'
assert calc_keys_rec(0, '>') == '>'
assert calc_keys_rec(0, 'v') == 'v'
assert calc_keys_rec(0, '^') == '^'
assert calc_keys_rec(1, 'A') == 'A'
assert calc_keys_rec(2, 'A') == 'A'
assert calc_keys_rec(3, 'A') == 'A'
assert calc_keys_rec(4, 'A') == 'A'
assert calc_keys_rec(1, '>') == 'vA'
assert calc_keys_rec(1, '>>A') == 'vAA^A'
assert calc_keys_rec(1, '>>vA') == 'vAA<A>^A'


def part1_(code):
    curr_letter = 'A'
    all = ''
    for letter in code:
        move_letters = get_pad_letters(curr_letter, letter, 'numpad_grid')
        all += calc_keys_rec(2, move_letters)
        curr_letter = letter
    multiplier = int(code[:-1])
    print('full result', (len(all), multiplier), all)
    return (len(all), multiplier)


# 68 * 29, 60 * 980, 68 * 179, 64 * 456, 64 * 379. Adding these together produces 126384.
assert part1_('029A') == (68, 29)
assert part1_('980A') == (60, 980)
assert part1_('179A') == (68, 179)
assert part1_('456A') == (64, 456)
assert part1_('379A') == (64, 379)
assert part1(test_input) == 126384

part1(real_input)
