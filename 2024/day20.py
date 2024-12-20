import time
from logging import DEBUG

import numpy as np

from grid_robot import find_value, GridRobot, DIRS
from util import map_to_numbers, sub_map_to_numbers

test_input = open('day20-testinput.txt').read().strip()
real_input = open('day20-input.txt').read().strip()

DEBUG = False


def parse_input(input):
    lines = input.splitlines()
    char_matrix = [[char for char in line] for line in lines]
    return np.array(char_matrix)


def get_next_dirs_4(robot: GridRobot, max_cheat_dist):
    clones = [robot.clone_forward(dir) for dir in DIRS]
    return [clone for clone in clones if
            not clone.out_of_bounds() and clone.tile_value() == '.']


def count_paths(start_robot: GridRobot, end_check, heuristic, get_next_states, max_cost):
    found_states = {}
    heur_map = {}

    sorted_states_to_try = [start_robot.yx_key()]
    found_states[start_robot.yx_key()] = start_robot
    heur_map[start_robot.yx_key()] = -heuristic(start_robot)
    def key_heuristic(el_key):
        return heur_map[el_key]

    def insert_sorted(next_states, rob):
        yx_key = rob.yx_key()
        found_states[yx_key] = next_r
        heur_map[yx_key] = -heuristic(rob)
        next_states.append(yx_key)
        pass
    ok_robots=0
    while len(sorted_states_to_try) > 0:
        sorted_states_to_try.sort(key=key_heuristic)
        try_state = found_states[sorted_states_to_try.pop()]
        next_states = get_next_states(try_state)
        for next_r in next_states:
            next_key = next_r.yx_key()
            end_found = end_check(next_r)
            if next_r.cost > max_cost:
                continue
            if not end_found:
                if next_key not in found_states:
                    insert_sorted(sorted_states_to_try, next_r)
                elif found_states[next_key].cost > next_r.cost:
                    if next_key in sorted_states_to_try:
                        sorted_states_to_try.remove(next_key)
                    insert_sorted(sorted_states_to_try, next_r)
            else:
                best_robot = next_r
                if DEBUG: print('found path', best_robot, best_robot.cost)
                ok_robots +=1
    return ok_robots


def find_all(start_robot, end_robot, grid, max_cost, max_cheat_dist):
    start_robot.grid = grid
    end_robot.grid = grid

    def end_check(test_r):
        return test_r.x == end_robot.x and test_r.y == end_robot.y

    def heuristic(robot: GridRobot):
        return robot.cost + abs(robot.x - end_robot.x) + abs(robot.y - end_robot.y)

    def get_next(r):
        return get_next_dirs_4(r, max_cheat_dist)

    result = count_paths(start_robot, end_check, heuristic, get_next, max_cost)
    return result


def get_cheat_grids(grid: np.array):
    cheat_grids = []
    for y, line in enumerate(grid):
        for x, value in enumerate(line):
            if value == '#':
                cheat_grid = grid.copy()
                cheat_grid[y][x] = '.'
                cheat_grids.append(cheat_grid)
    return cheat_grids


def part12(input, max_cost, improvement_needed, only_equal=False, max_cheat_dist=1):
    print('improvement_needed', improvement_needed)
    grid = parse_input(input)
    start = find_value('S', grid)
    # print('start', start)
    end = find_value('E', grid)
    # print('end', end)
    grid[start[0]][start[1]] = '.'
    grid[end[0]][end[1]] = '.'

    def cost_calc(amount):
        return 1

    start_robot = GridRobot(start[0], start[1], cost_calc_fn=cost_calc)
    end_robot = GridRobot(end[0], end[1])
    result = find_all(start_robot, end_robot, grid, max_cost, max_cheat_dist)
    print(result)
    return result


assert part12(test_input, 84, 64, False) == 1
part12(real_input, 9456, 100)

assert part12(test_input, 84, 50, True, 20) == 32
assert part12(test_input, 84, 52, True, 20) == 31
part12(real_input, 9456, 100, False, 20)
