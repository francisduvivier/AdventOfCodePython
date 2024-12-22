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
    code_results = [calc_numpad_cost(code) for code in codes]

    result = sum([res[0] * res[1] for res in code_results])
    print('result part 1', result)
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

DEBUG = False


@cache
def translate_move(from_val: str, to_val: str, grid_name: str) -> (DotMap, np.array, DotMap):
    grid = numpad_grid if grid_name == 'numpad_grid' else dirpad_grid
    from_pos = find_value_pos(from_val, grid)
    to_pos = find_value_pos(to_val, grid)
    return from_pos, to_pos, grid


def unsorted_passes_none(from_val: str, to_val: str, grid_name):
    from_pos, to_pos, grid = translate_move(from_val, to_val, grid_name)
    none_pos = find_value_pos(None, grid)
    return (from_pos.x == none_pos.x and to_pos.y == none_pos.y or
            from_pos.y == none_pos.y and to_pos.x == none_pos.x)
    pass


assert unsorted_passes_none('A', 'A', 'dirpad_grid') == False
assert unsorted_passes_none('A', 'v', 'dirpad_grid') == False
assert unsorted_passes_none('A', '<', 'dirpad_grid') == True
assert unsorted_passes_none('A', 'A', 'numpad_grid') == False
assert unsorted_passes_none('A', '9', 'numpad_grid') == False
assert unsorted_passes_none('A', '5', 'numpad_grid') == False
assert unsorted_passes_none('A', '4', 'numpad_grid') == True


@cache
def get_pad_letters(from_val, to_val, grid_name: str):
    from_pos, to_pos, grid = translate_move(from_val, to_val, grid_name)
    order = 'v>^<' if grid[0][0] is None else '^>v<'
    if DEBUG: assert order == 'v>^<' if grid_name == 'dirpad_grid' else '^>v<'
    ydiff = to_pos.y - from_pos.y
    xdiff = to_pos.x - from_pos.x
    letters = []
    if xdiff != 0:
        letters += ['>' if xdiff > 0 else '<' for _ in range(abs(xdiff))]
    if ydiff != 0:
        letters += ['v' if ydiff > 0 else '^' for _ in range(abs(ydiff))]

    sort_key = lambda l: order.index(l)
    sorted_letters = sorted(letters, key=sort_key)
    path_letters = [''.join(sorted_letters) + 'A']
    if unsorted_passes_none(from_val, to_val, grid_name) or xdiff == 0 or ydiff == 0:
        return path_letters
    return path_letters + [''.join(reversed(sorted_letters)) + 'A']


assert get_pad_letters('A', 'A', 'dirpad_grid') == ['A']
assert get_pad_letters('A', '<', 'dirpad_grid') == ['v<<A']
assert get_pad_letters('<', 'A', 'dirpad_grid') == ['>>^A']
assert get_pad_letters('v', 'A', 'dirpad_grid') == ['>^A', '^>A']
assert get_pad_letters('A', '>', 'dirpad_grid') == ['vA']
assert get_pad_letters('>', 'A', 'dirpad_grid') == ['^A']

assert get_pad_letters('0', 'A', 'numpad_grid') == ['>A']
assert get_pad_letters('A', '0', 'numpad_grid') == ['<A']
assert get_pad_letters('A', '7', 'numpad_grid') == ['^^^<<A']
assert get_pad_letters('7', 'A', 'numpad_grid') == ['>>vvvA']


@cache
def calc_keys_rec(nb_subrobots: int, keys: str):
    if nb_subrobots == 0:
        return len(keys)
    curr_letter = 'A'
    all = 0
    for letter in keys:
        move_letters_options = get_pad_letters(curr_letter, letter, 'dirpad_grid')
        all += min([calc_keys_rec(nb_subrobots - 1, move_letters) for move_letters in move_letters_options])
        curr_letter = letter
    return all


start = find_value_pos('A', numpad_grid)
assert start == DotMap({'y': 3, 'x': 2})
assert calc_keys_rec(0, 'A') == len('A')
assert calc_keys_rec(0, '<') == len('<')
assert calc_keys_rec(0, '>') == len('>')
assert calc_keys_rec(0, 'v') == len('v')
assert calc_keys_rec(0, '^') == len('^')
assert calc_keys_rec(1, 'A') == len('A')
assert calc_keys_rec(2, 'A') == len('A')
assert calc_keys_rec(3, 'A') == len('A')
assert calc_keys_rec(4, 'A') == len('A')
assert calc_keys_rec(1, '>') == len('vA')
assert calc_keys_rec(1, '>>A') == len('vAA^A')
assert calc_keys_rec(1, '>>vA') == len('vAA<A>^A')


def calc_numpad_cost(code, robots=2):
    curr_letter = 'A'
    all = 0
    for letter in code:
        move_letters_options = get_pad_letters(curr_letter, letter, 'numpad_grid')
        all += min([calc_keys_rec(robots, move_letters) for move_letters in move_letters_options])
        curr_letter = letter
    multiplier = int(code[:-1])
    if DEBUG: print('full result', (len(all), multiplier), all)
    return (all, multiplier)


# 68 * 29, 60 * 980, 68 * 179, 64 * 456, 64 * 379. Adding these together produces 126384.
assert calc_numpad_cost('029A') == (68, 29)
assert calc_numpad_cost('980A') == (60, 980)
assert calc_numpad_cost('179A') == (68, 179)
assert calc_numpad_cost('456A') == (64, 456)
assert calc_numpad_cost('379A') == (64, 379)
# v<<A>>^AvA^Av<<A>>^Av<A<A>>^AAvAA^<A>Av<A<A>>^AvA^<A>Av<A>^AAv<<A>>^AvA^<A>A

# <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
assert part1(test_input) == 126384

assert part1(real_input) == 94426


def part2(input):
    codes = parse_input(input)
    code_results = []
    for robots in range(1, 26):
        print('part 2: trying i: ' + str(robots))
        code_results = [calc_numpad_cost(code, robots) for code in codes]

    result = sum([res[0] * res[1] for res in code_results])
    print('result part 2', result)
    return result


part2(real_input)
