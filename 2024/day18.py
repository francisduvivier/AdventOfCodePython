import time

import numpy as np
from dotmap import DotMap

from grid_robot import print_grid, GridRobot, DIRS
from util import map_to_numbers, sub_map_to_numbers

test_input = open('day18-testinput.txt').read().strip()
real_input = open('day18-input.txt').read().strip()


def parse_input(input):
    lines = input.splitlines()
    line_split_lambda = lambda line: line.split(',')
    char_matrix = [line_split_lambda(line) for line in lines]
    numbers_matrix = sub_map_to_numbers(char_matrix)

    return [DotMap({"y": n[1], "x": n[0]}) for n in numbers_matrix]

DEBUG = True

def get_next_states(robot: GridRobot):
    clones =  [robot.clone_forward(dir) for dir in DIRS]
    return [clone for clone in clones if not clone.out_of_bounds() and clone.tile_value() == '.']

def shortest_path(start_robot:  GridRobot, end: GridRobot):
    found_states = {}
    eq_map = {}
    best_robot = None
    heur_map = {}

    def heuristic(robot: GridRobot):
        return robot.cost + abs(robot.x - end.x) + abs(robot.y - end.y)

    heur_map[start_robot.yx_key()]= heuristic(start_robot)
    sorted_states_to_try = [start_robot.yx_key()]
    found_states[start_robot.yx_key()] = start_robot


    def key_heuristic(el_key):
        return heur_map[el_key]

    def insert_sorted(next_states, rob):
        yx_key = rob.yx_key()
        eq_map[yx_key] = []
        found_states[yx_key] = next_r
        heur_map[yx_key] = -heuristic(rob)
        next_states.append(yx_key)
        pass

    while len(sorted_states_to_try) > 0:
        sorted_states_to_try.sort(key=key_heuristic)
        next_states = get_next_states(found_states[sorted_states_to_try.pop()])
        for next_r in next_states:
            if best_robot is not None and best_robot.cost < heuristic(next_r):
                continue
            next_key = next_r.yx_key()
            if next_key not in found_states:
                insert_sorted(sorted_states_to_try, next_r)
            elif found_states[next_key].cost > next_r.cost:
                if next_key in sorted_states_to_try:
                    sorted_states_to_try.remove(next_key)
                insert_sorted(sorted_states_to_try, next_r)
            elif found_states[next_key].cost == next_r.cost:
                eq_map[next_key].append(next_r)
            end_found = next_r.y == end.y and next_r.x == end.x
            if end_found:
                best_robot = next_r
                print('found path', best_robot, best_robot.cost)
    return best_robot


def part1(input, slice, grid_size):
    blocks = parse_input(input)[0:slice]
    grid = np.array([['.' for x in range(grid_size)] for y in range(grid_size)])
    for block in blocks:
        grid[block.y][block.x] = '#'
    if DEBUG: print_grid(grid)
    start_robot = GridRobot(0,0, grid=grid, cost_calc_fn=lambda amount:amount)
    end_robot = GridRobot(grid_size -1,grid_size -1)
    best_robot = shortest_path(start_robot, end_robot)
    return best_robot.cost


assert part1(test_input, 12, 6+1) == 22
part1(real_input, 1024, 70+1)
