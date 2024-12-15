import time

import numpy as np

from grid_robot import DIRS, DIR, GridRobot
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

DEBUG = False
def find_first_free(try_robot):
    if DEBUG: print('search open spot', try_robot)
    while True:
        try_robot.move_forward()
        if try_robot.tile_value() == '.':
            if DEBUG: print('open spot found', try_robot)
            return try_robot
        if try_robot.tile_value() == '#':
            if DEBUG: print('wall found', try_robot)
            return None


def print_grid(tile_grid):
    print('\n'.join([''.join(line) for line in tile_grid]))


def part1(input):
    tile_grid, step_dirs = parse_input(input)
    robot_pos = ([
        [(y, x) for x, value in enumerate(line) if value == '@'][0]
        for y, line in enumerate(tile_grid) if '@' in line
    ])[0]
    print('robot_pos', robot_pos[0], robot_pos[1])
    robot = GridRobot(robot_pos[0], robot_pos[1], step_dirs[0], tile_grid)
    print("step dirs", len(step_dirs))
    for dir in step_dirs:
        find_free_robot = robot.clone(dir)
        first_free = find_first_free(find_free_robot)
        if first_free is not None:
            robot.set_tile_value('.')
            robot.set_dir(dir)
            robot.move_forward()
            tile_value = robot.tile_value()
            find_free_robot.set_tile_value(tile_value)
            robot.set_tile_value('@')

    result = get_box_score(tile_grid)
    print_grid(tile_grid)
    print(result)
    return result


assert part1(test_input0) == 2028
assert part1(test_input) == 10092
part1(real_input)
