import time

import numpy as np
from dotmap import DotMap

from grid_robot import print_grid, GridRobot, DIRS, SKEWED_DIRS
from util import map_to_numbers, sub_map_to_numbers

test_input = open('day18-testinput.txt').read().strip()
real_input = open('day18-input.txt').read().strip()


def parse_input(input):
    lines = input.splitlines()
    line_split_lambda = lambda line: line.split(',')
    char_matrix = [line_split_lambda(line) for line in lines]
    numbers_matrix = sub_map_to_numbers(char_matrix)

    return [DotMap({"y": n[1], "x": n[0]}) for n in numbers_matrix]


DEBUG = False


def get_next_dirs_4(robot: GridRobot):
    clones = [robot.clone_forward(dir) for dir in DIRS]
    return [clone for clone in clones if not clone.out_of_bounds() and clone.tile_value() == '.']


def get_next_dirs_8(robot: GridRobot):
    clones = [robot.clone_forward(dir) for dir in DIRS + SKEWED_DIRS]
    return [clone for clone in clones if not clone.out_of_bounds() and clone.tile_value() == '#']


def shortest_path(start_robot: GridRobot, end_check, heuristic, get_next_states):
    found_states = {}
    best_robot = None
    heur_map = {}

    heur_map[start_robot.yx_key()] = heuristic(start_robot)
    sorted_states_to_try = [start_robot.yx_key()]
    found_states[start_robot.yx_key()] = start_robot

    def key_heuristic(el_key):
        return heur_map[el_key]

    def insert_sorted(next_states, rob):
        yx_key = rob.yx_key()
        found_states[yx_key] = next_r
        heur_map[yx_key] = -heuristic(rob)
        next_states.append(yx_key)
        pass

    while len(sorted_states_to_try) > 0:
        sorted_states_to_try.sort(key=key_heuristic)
        next_states = get_next_states(found_states[sorted_states_to_try.pop()])
        for next_r in next_states:
            if best_robot is not None and best_robot.cost <= heuristic(next_r):
                continue
            next_key = next_r.yx_key()
            if next_key not in found_states:
                insert_sorted(sorted_states_to_try, next_r)
            elif found_states[next_key].cost > next_r.cost:
                if next_key in sorted_states_to_try:
                    sorted_states_to_try.remove(next_key)
                insert_sorted(sorted_states_to_try, next_r)
            end_found = end_check(next_r)
            if end_found:
                best_robot = next_r
                if DEBUG: print('found path', best_robot, best_robot.cost)
    return best_robot


def part1(input, slice, grid_size):
    blocks = parse_input(input)[0:slice]
    grid = np.array([['.' for x in range(grid_size)] for y in range(grid_size)])
    for block in blocks:
        grid[block.y][block.x] = '#'
    if DEBUG: print_grid(grid)
    start_robot = GridRobot(0, 0, grid=grid, cost_calc_fn=lambda amount: amount)
    end_robot = GridRobot(grid_size - 1, grid_size - 1)

    def end_check(test_r):
        return test_r.x == end_robot.x and test_r.y == end_robot.y

    def heuristic(robot: GridRobot):
        return robot.cost + abs(robot.x - end_robot.x) + abs(robot.y - end_robot.y)

    best_robot = shortest_path(start_robot, end_check, heuristic, get_next_dirs_4)
    return best_robot.cost


assert part1(test_input, 12, 6 + 1) == 22
part1(real_input, 1024, 70 + 1)


def part2(input, grid_size):
    blocks = parse_input(input)
    grid = np.array([['.' for x in range(grid_size)] for y in range(grid_size)])
    if DEBUG: print_grid(grid)
    end_robot = GridRobot(grid_size - 1, grid_size - 1)

    def end_check_r(test_r):
        return test_r.x == end_robot.x or test_r.y == 0

    def end_check_l(test_r):
        return test_r.x == 0 or test_r.y == end_robot.y

    def heuristic_r(robot: GridRobot):
        return robot.cost + abs(robot.x - end_robot.x) + robot.y

    def heuristic_l(robot: GridRobot):
        return robot.cost + abs(robot.y - end_robot.y) + robot.x

    for index, block in enumerate(blocks):
        grid[block.y][block.x] = '#'
        start_robot = GridRobot(block.y, block.x, grid=grid, cost_calc_fn=lambda amount: amount)
        best_robot_r = shortest_path(start_robot, end_check_r, heuristic_r, get_next_dirs_8)
        if best_robot_r is None:
            continue
        best_robot_l = shortest_path(start_robot, end_check_l, heuristic_l, get_next_dirs_8)
        if best_robot_l is None:
            continue
        print_grid(grid)
        solution = str(block.x) + ',' + str(block.y)
        print('blocker found', solution, 'block_index', index)
        return solution
    print('NO RESULT!')
    return None


assert part2(test_input, 6 + 1) == '6,1'
part2(real_input, 70 + 1)
