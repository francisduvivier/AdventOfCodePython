import time

import numpy as np

from grid_robot import DIRS, DIR
from util import map_to_numbers, sub_map_to_numbers

test_input = open('day15-testinput.txt').read().strip()
test_input0 = open('day15-testinput0.txt').read().strip()
real_input = open('day15-input.txt').read().strip()


def parse_input(input):
    (tile_lines, step_lines) = input.split('\n\n')
    tile_grid = np.array([[char for char in line] for line in tile_lines.splitlines()])
    step_dirs = np.array([DIR[dir_letter] for dir_letter in ''.join(step_lines.splitlines())])
    return tile_grid, step_dirs


def get_box_score(tiles):
    return sum([
        sum([x + 100 * y for x, value in enumerate(line) if value == 'O'])
        for y, line in enumerate(tiles)
    ])


def part1(input):
    tile_grid, step_dirs = parse_input(input)
    result = get_box_score(tile_grid)
    print(result)
    return result


assert part1(test_input0) == 2028
assert part1(test_input) == 10092
part1(real_input)
