import time

import numpy as np

from grid_robot import find_value, GridRobot, DIRS
from util import map_to_numbers, sub_map_to_numbers

test_input = open('day20-testinput.txt').read().strip()
real_input = open('day20-input.txt').read().strip()


def parse_input(input):
    lines = input.splitlines()
    char_matrix = [[char for char in line] for line in lines]
    return np.array(char_matrix)


max = None


def get_next_dirs_4(robot: GridRobot):
    global max
    clones = [robot.clone_forward(dir) for dir in DIRS]
    return [clone for clone in clones if
            not clone.out_of_bounds() and clone.tile_value() == '.' and (max is None or clone.cost <= max)]


DEBUG = True


def shortest_path(start_robot: GridRobot, end_check, heuristic, get_next_states, global_found_states):
    best_robot = None
    heur_map = {}
    found_states = {}
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

    while len(sorted_states_to_try) > 0 and best_robot is None:
        sorted_states_to_try.sort(key=key_heuristic)
        next_states = get_next_states(found_states[sorted_states_to_try.pop()])
        for next_r in next_states:
            if (best_robot is not None and best_robot.cost <= heuristic(next_r) or
                    max is not None and max < heuristic(next_r)):
                continue
            next_key = next_r.yx_key()
            if next_key not in global_found_states or global_found_states[next_key].cost >= next_r.cost :
                if next_key not in found_states:
                    insert_sorted(sorted_states_to_try, next_r)
                elif found_states[next_key].cost > next_r.cost :
                    if next_key in sorted_states_to_try:
                        sorted_states_to_try.remove(next_key)
                    insert_sorted(sorted_states_to_try, next_r)
            end_found = end_check(next_r)
            if end_found:
                best_robot = next_r
                if DEBUG: print('found path', best_robot, best_robot.cost)
    return best_robot, found_states


def find_shortest(start_robot, end_robot, grid, found_states):
    start_robot.grid = grid
    end_robot.grid = grid

    def end_check(test_r):
        return test_r.x == end_robot.x and test_r.y == end_robot.y

    def heuristic(robot: GridRobot):
        return robot.cost + abs(robot.x - end_robot.x) + abs(robot.y - end_robot.y)

    best_robot, found_states = shortest_path(start_robot, end_check, heuristic, get_next_dirs_4, found_states)
    return best_robot.cost if best_robot is not None else max + 1, found_states


def get_cheat_grids(grid: np.array):
    cheat_grids = []
    for y, line in enumerate(grid):
        for x, value in enumerate(line):
            if value == '#':
                cheat_grid = grid.copy()
                cheat_grid[y][x] = '.'
                cheat_grids.append(cheat_grid)
    return cheat_grids


def part1(input, improvement_needed, only_equal=False):
    grid = parse_input(input)
    start = find_value('S', grid)
    # print('start', start)
    end = find_value('E', grid)
    # print('end', end)
    grid[start[0]][start[1]] = '.'
    grid[end[0]][end[1]] = '.'
    result = 0

    def cost_calc(amount):
        return 1

    start_robot = GridRobot(start[0], start[1], cost_calc_fn=cost_calc)
    end_robot = GridRobot(end[0], end[1])
    global max
    max = None

    shortest, found_states_start = find_shortest(start_robot, end_robot, grid, {})
    print('shortest path cost', shortest)
    max = shortest - improvement_needed
    for i, cheat_grid in enumerate(get_cheat_grids(grid)):
        if DEBUG: print('cheat grid nb', i)
        cheat_path, new_found_states = find_shortest(start_robot, end_robot, cheat_grid, found_states_start)
        if only_equal:
            if shortest - cheat_path == improvement_needed:  # todo check off by one
                result += 1
        else:
            if shortest - cheat_path >= improvement_needed:  # todo check off by one
                result += 1
    print(result)
    return result


assert part1(test_input, 2, True) == 14
assert part1(test_input, 4, True) == 14
assert part1(test_input, 6, True) == 2
assert part1(test_input, 12, True) == 3
assert part1(test_input, 64, True) == 1
part1(real_input, 100)
