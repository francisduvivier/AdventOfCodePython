import time

import numpy as np

from grid_robot import DIRS, DIR, GridRobot, find_value

test_input = open('day15-testinput.txt').read().strip()
test_input0 = open('day15-testinput0.txt').read().strip()
test_input2 = open('day15-testinput2.txt').read().strip()
real_input = open('day15-input.txt').read().strip()


def parse_input(input):
    (tile_lines, step_lines) = input.split('\n\n')
    tile_grid = np.array([[char for char in line] for line in tile_lines.splitlines()])
    step_dirs = [DIR[dir_letter] for dir_letter in ''.join(step_lines.splitlines())]
    return tile_grid, step_dirs


def get_box_score(tiles):
    return sum([
        sum([x + 100 * y for x, value in enumerate(line) if value == 'O' or value == '['])
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
    robot_pos = find_value('@', tile_grid)
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
    if DEBUG: print_grid(tile_grid)
    print(result)
    return result


assert part1(test_input0) == 2028
assert part1(test_input) == 10092
part1(real_input)


def find_pair(try_robot) -> GridRobot:
    pair = try_robot.clone(DIR['>'] if try_robot.tile_value() == '[' else DIR['<'])
    pair.move_forward()
    pair.set_dir(try_robot.dyx)
    return pair


def find_connected_tiles_rec(try_robot: GridRobot, done_map: dict[str, GridRobot]):
    if try_robot.yx_key() in done_map:
        return True
    if DEBUG: print('find_connected_tiles_rec', try_robot, try_robot.tile_value())
    tile_value = try_robot.tile_value()
    if tile_value == '#':
        return False
    if tile_value == '.':
        return True

    done_map[try_robot.yx_key()] = try_robot
    rec_robot = try_robot.clone()
    rec_robot.move_forward()
    result = find_connected_tiles_rec(rec_robot, done_map)
    if not result:
        return False
    if (try_robot.dyx == DIR['v'] or try_robot.dyx == DIR['^']) and (tile_value == ']' or tile_value == '['):
        replaced_pair = find_pair(try_robot)
        result = find_connected_tiles_rec(replaced_pair, done_map)
    return result


def flatten(nested_list):
    return [char for sub_list in nested_list for char in sub_list]


def double_horizontal(tile_grid):
    double = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.',
    }
    return [flatten([double[char] for char in line]) for line in tile_grid]


def part2(input):
    tile_grid, step_dirs = parse_input(input)
    tile_grid = np.array(double_horizontal(tile_grid))
    if DEBUG: print_grid(tile_grid)
    robot_pos = find_value('@', tile_grid)
    print('robot_pos', robot_pos[0], robot_pos[1])
    robot = GridRobot(robot_pos[0], robot_pos[1], step_dirs[0], tile_grid)
    print("step dirs", len(step_dirs))
    # print_grid(tile_grid)
    for step, dir in enumerate(step_dirs):
        if DEBUG: sprint('-------------step', step, dir)
        find_free_robot = robot.clone(dyx=dir)
        done_map: dict[str, GridRobot] = dict()
        move_success = find_connected_tiles_rec(find_free_robot, done_map=done_map)
        if move_success:
            robot.set_dir(dir)
            robot.move_forward()
            touched = set()
            original_grid = robot.grid.copy()
            for to_change in done_map.values():
                value_to_move = original_grid[to_change.y][to_change.x]
                if to_change.yx_key() not in touched:
                    to_change.set_tile_value('.')
                to_change.move_forward()
                to_change.set_tile_value(value_to_move)
                touched.add(to_change.yx_key())
        if DEBUG: print_grid(find_free_robot.grid)

    result = get_box_score(robot.grid)
    if DEBUG: print_grid(robot.grid)
    print(result)
    return result


assert part2(test_input2)
assert part2(test_input) == 9021
part2(real_input)
