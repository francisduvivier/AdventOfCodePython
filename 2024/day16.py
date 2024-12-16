import time
from curses import start_color

import numpy as np
from dotmap import DotMap

from grid_robot import find_value, GridRobot, DIR

test_input = open('day16-testinput.txt').read().strip()
test_input2 = open('day16-testinput2.txt').read().strip()
real_input = open('day16-input.txt').read().strip()
import sys

sys.setrecursionlimit(1500000)
DEBUG = False


def parse_input(input):
    lines = input.splitlines()
    line_split_lambda = lambda line: [char for char in line]
    char_matrix = np.array([line_split_lambda(line) for line in lines])
    return char_matrix


# def find_best_rec(robot: GridRobot, end, calc_state):
#     min_turn_cost = 1000 if robot.x != end.x and robot.y != end.y else 0
#     if calc_state.min < robot.cost + abs(robot.x - end.x) + abs(
#             robot.y - end.y) + min_turn_cost:
#         return
#     end_found = robot.y == end.y and robot.x == end.x
#     min_cost_here = calc_state.min_map[robot.state_key()] if robot.state_key() in calc_state.min_map else None
#     if min_cost_here is not None and min_cost_here < robot.cost:
#         return
#     if min_cost_here is not None and min_cost_here == robot.cost:
#         if robot.yx_key() in calc_state.all_tiles:
#             for tile in robot.path_tiles:
#                 calc_state.all_tiles.add(tile)
#         return
#     if DEBUG: print('find_best_rec', robot, robot.cost)
#     calc_state.min_map[robot.state_key()] = robot.cost
#     if end_found:
#         if robot.cost < calc_state.min:
#             calc_state.all_tiles = set()
#         for tile in robot.path_tiles:
#             calc_state.all_tiles.add(tile)
#         calc_state.min = robot.cost
#         return
#     left_robot = robot.clone()
#     left_robot.turn_right(-1)
#     if left_robot.state_key() not in calc_state.min_map  or calc_state.min_map[
#         left_robot.state_key()] > left_robot.cost + 1:
#         calc_state.min_map[left_robot.state_key()] = left_robot.cost + 1
#     clean_robot = robot.clone()
#     for _turn in [1, 1]:
#         clean_robot.turn_right()
#         if clean_robot.state_key() not in calc_state.min_map  or calc_state.min_map[
#             clean_robot.state_key()] > clean_robot.cost + 1:
#             calc_state.min_map[clean_robot.state_key()] = clean_robot.cost + 1
#     for turn in [3, 1]:
#         turn_robot = robot.clone()
#         turn_robot.turn_right(turn)
#         find_best_rec(turn_robot, end, calc_state)
#     move_robot = robot.clone()
#     move_robot.move_forward()
#     if not move_robot.out_of_bounds() and move_robot.tile_value() != '#':
#         find_best_rec(move_robot, end, calc_state)
#     return


def get_next_states(robot: GridRobot)-> list[GridRobot]:
    next_states = []
    for turn in [3, 1]:
        turn_robot = robot.clone()
        turn_robot.turn_right(turn)
        next_states.append(turn_robot)
    move_robot = robot.clone()
    move_robot.move_forward()
    if not move_robot.out_of_bounds() and move_robot.tile_value() != '#':
        next_states.append(move_robot)

    return next_states


def insert_sorted(next_states, param, key):
    next_states.append(param)
    next_states.sort(key= key)
    pass


def part12(input):
    grid = parse_input(input)
    start = find_value('S', grid)
    end = DotMap({"y": find_value('E', grid)[0],
                      "x": find_value('E', grid)[1]})
    calc_state = DotMap({"min": 2 ** 30})
    calc_state.min_map = {}
    calc_state.all_tiles = set()
    start_robot = GridRobot(start[0], start[1], DIR['>'], grid, cost_calc_fn=lambda x: 1, turn_cost_fn=lambda x: 1000)
    sorted_states_to_try = [start_robot.state_key()]
    found_states = {}
    found_states[start_robot.state_key()] = start_robot
    def heuristic(robot: GridRobot):
        min_turn_cost = 1000 if robot.x != end.x and robot.y != end.y else 0
        return abs(robot.x - end.x) + abs(robot.y - end.y) + min_turn_cost

    min_result = None
    def key_heuristic(robot_key: str):
        robot = found_states[robot_key]
        min_turn_cost = 1000 if robot.x != end.x and robot.y != end.y else 0
        return abs(robot.x - end.x) + abs(robot.y - end.y) + min_turn_cost
    while len(sorted_states_to_try) > 0:
        next_states = get_next_states(found_states[sorted_states_to_try.pop()])
        for next_r in next_states:
            if min_result is not None and heuristic(next_r) >= min_result:
                continue
            end_found = next_r.y == end.y and next_r.x == end.x
            if end_found:
                min_result = next_r.cost
                print('found path', min_result)
                continue
            if next_r.state_key() not in found_states:
                found_states[next_r.state_key()] = next_r
                insert_sorted(sorted_states_to_try, next_r.state_key(), key=key_heuristic)
            elif found_states[next_r.state_key()].cost > next_r.cost:
                found_states[next_r.state_key()] = next_r
                if next_r.state_key() in sorted_states_to_try:
                    sorted_states_to_try.remove(next_r.state_key())
                insert_sorted(sorted_states_to_try, next_r.state_key(), key=key_heuristic)

    result = len(calc_state.all_tiles)
    print('result', result)
    print('min_result', min_result)
    return result, min_result


assert part12(test_input) == (0, 7036)
assert part12(test_input2) == (0, 11048)
part12(real_input)
