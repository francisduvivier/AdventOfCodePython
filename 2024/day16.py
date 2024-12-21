import sys
sys.path.append("..")

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


def get_next_states(robot: GridRobot) -> list[GridRobot]:
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
    eq_map = {}

    def heuristic(robot: GridRobot):
        min_turn_cost = 1000 if robot.x != end.x and robot.y != end.y else 0
        return robot.cost + abs(robot.x - end.x) + abs(robot.y - end.y) + min_turn_cost

    best_robot = None
    heur_map = {}
    heur_map[start_robot.state_key()]= heuristic(start_robot)
    def key_heuristic(el: GridRobot):
        return heur_map[el]

    def insert_sorted(next_states, rob):
        state_key = rob.state_key()
        eq_map[state_key] = []
        found_states[state_key] = next_r
        heur_map[state_key] = -heuristic(rob)
        next_states.append(state_key)
        pass

    while len(sorted_states_to_try) > 0:
        sorted_states_to_try.sort(key=key_heuristic)
        next_states = get_next_states(found_states[sorted_states_to_try.pop()])
        for next_r in next_states:
            if best_robot is not None and best_robot.cost < heuristic(next_r):
                continue
            next_key = next_r.state_key()
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

    def get_eq_path_tiles_rec(r_state):
        result_set = set()
        for eq in eq_map[r_state]:
            result_set = result_set.union(eq.path_tiles[:-1])
            for sub_path in eq.path[:-1]:
                result_set = result_set.union(get_eq_path_tiles_rec(sub_path))
        return result_set

    all_tiles = set(best_robot.path_tiles)
    for path_item in best_robot.path:
        all_tiles = all_tiles.union(get_eq_path_tiles_rec(path_item))
    result = len(all_tiles)
    print('result', result)
    print('best_robot', best_robot.cost)
    return result, best_robot.cost


assert part12(test_input) == (45, 7036)
assert part12(test_input2) == (64, 11048)
part12(real_input)
