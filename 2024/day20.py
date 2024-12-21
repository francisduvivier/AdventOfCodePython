from functools import cache
from logging import DEBUG

import numpy as np

from grid_robot import find_value, GridRobot, DIRS, DIR, yx_key
import sys

sys.setrecursionlimit(15000000)

test_input = open('day20-testinput.txt').read().strip()
real_input = open('day20-input.txt').read().strip()

DEBUG = False


def parse_input(input):
    lines = input.splitlines()
    char_matrix = [[char for char in line] for line in lines]
    return np.array(char_matrix)


def get_next_dirs_4(robot: GridRobot, max_cheat_dist):
    clones = [robot.clone_forward(dir) for dir in DIRS]
    clones_in_bounds = [clone for clone in clones if not clone.out_of_bounds()]
    options = [clone for clone in clones_in_bounds if clone.tile_value() == '.']

    if max_cheat_dist > 1 and robot.cheated is None:
        for x in range(-max_cheat_dist, max_cheat_dist + 1):
            remaining = max_cheat_dist - abs(x)
            for y in range(-remaining, remaining + 1):
                if abs(y) + abs(x) < 2: continue  # not a cheat yet
                clone = robot.clone()
                clone.jump(y, x)
                if not clone.out_of_bounds() and clone.tile_value() == '.':
                    assert (clone.yx_key() != robot.yx_key())
                    options.append(clone)
    return options


def count_cheats(start_robot: GridRobot, end_check, minimal_possible_cost_for_position, get_next_states, max_cost):
    found_states = {}

    sorted_states_to_try = [start_robot]

    found_states[True] = {}
    found_states[False] = {}
    found_states[False][start_robot.yx_key()] = start_robot
    eq_map = {}  # yx_key to map of cheat_key to robot
    eq_map[start_robot.yx_key()] = []
    remaining_cost_map = {}  # yx_key to min_remaining_cost

    def insert_sorted(rob):
        assert next_key not in found_states[rob.cheated is not None]
        assert rob.yx_key() not in rob.path_tiles[:-1]
        cheated = rob.cheated is not None
        found_states[cheated][next_key] = next_r
        if cheated:
            eq_map[next_key] = []
        sorted_states_to_try.insert(0, rob)

    def get_robot_cost_neg(r):
        return -r.cost

    def min_possible_cost(r):
        key = r.yx_key()
        if key in remaining_cost_map:
            return r.cost + remaining_cost_map[key]
        return minimal_possible_cost_for_position(r)

    solutions = []
    while len(sorted_states_to_try) > 0:
        sorted_states_to_try.sort(key=get_robot_cost_neg)
        try_state = sorted_states_to_try.pop()
        next_states = get_next_states(try_state)
        for next_r in next_states:
            next_key = next_r.yx_key()
            if min_possible_cost(next_r) > max_cost:
                continue
            end_found = end_check(next_r)
            if end_found:
                if DEBUG: print('found path', next_r, next_r.cost)
                solutions.append(next_r)
                continue
            if next_key in found_states[False]:
                assert found_states[False][next_key].cost <= next_r.cost
                continue
            if next_r.cheated is None:
                insert_sorted(next_r)
                continue
            if next_key in found_states[True]:
                eq_map[next_key].append(next_r)
                continue
            insert_sorted(next_r)

    cheats = gather_eq_tiles(solutions, eq_map, found_states[True], max_cost)
    # for key in eq_map:
    #     for eq in eq_map[key] :
    #         cheats.add(eq.cheated)
    # print('cheats2',len(cheats), cheats)
    return cheats


def gather_eq_tiles(solutions, eq_map, found_states, max_cost):
    print('gathering results')
    cheats = set(sol.cheated for sol in solutions)
    options = [(0, solution) for solution in solutions if solution.cheated]
    tiles_checked = {}
    while len(options):
        (nb_tiles_backtracked, robot) = options.pop()
        yx_key = robot.yx_key()
        if nb_tiles_backtracked > 0: assert yx_key in eq_map
        if nb_tiles_backtracked > 0: assert yx_key in found_states
        assert robot.cost <= max_cost - nb_tiles_backtracked
        assert not robot.path_tiles[-1].startswith('CHEAT')
        for index, tile_key in enumerate(reversed(robot.path_tiles[:-1])):
            if tile_key.startswith('CHEAT'): break
            if tile_key in tiles_checked and tiles_checked[tile_key] <= robot.cost:
                continue
            tiles_checked[tile_key] = robot.cost
            for eq in eq_map[tile_key]:
                # if eq.cheated in cheats:
                #     continue
                # assert not eq.path_tiles[-1].startswith('CHEAT')
                eq_backtracked = nb_tiles_backtracked + index + 1
                if eq.cost <= max_cost - eq_backtracked:
                    cheats.add(eq.cheated)
                    options.append((eq_backtracked, eq))

    # print('cheats1', len(cheats), cheats)
    return cheats


def find_all(start_robot, end_robot, grid, max_cost, max_cheat_dist):
    start_robot.grid = grid
    end_robot.grid = grid

    def end_check(test_r):
        return test_r.x == end_robot.x and test_r.y == end_robot.y

    def heuristic(robot: GridRobot):
        return robot.cost + abs(robot.x - end_robot.x) + abs(robot.y - end_robot.y)

    def get_next(r):
        return get_next_dirs_4(r, max_cheat_dist)

    result = count_cheats(start_robot, end_check, heuristic, get_next, max_cost)
    return result


def part12(input, best_non_cheat, improvement_needed, max_cheat_dist=1):
    # plan is: we search with a star, but when we find an already done tile then.
    # if the tile is done by non-cheater, then stop because it will have added all the chat paths
    # else(so if the tile is done by a cheater) then:
    #  if we have not cheated yet then this is still a viable option, add it to the non-cheaters etc...
    #  else (=we also cheated already):
    #    then
    #    if the remaining_cost_map[tile] is not None: add if total cost is lower, else break
    #    else add us to the map of cheat_key to costccc
    # if we find the end, then we are the best shortest path,we will verify this with a log
    # so what we can then do is: go through path_tiles and
    # set remaining_cost_map[tile] +=1 until cheat is found (abs(xdiff)+abs(ydiff))!=1
    # for every cheat_key in cheat_key_to_min_cost
    # if cheater_cost + remaining_cost <=max_cost:
    # => Add cheater_key to list of great_cheats
    print('best_non_cheat', best_non_cheat, 'improvement_needed', improvement_needed, 'max_cheat_dist', max_cheat_dist)
    grid = parse_input(input)
    start = find_value('S', grid)
    # print('start', start)
    end = find_value('E', grid)
    # print('end', end)
    grid[start[0]][start[1]] = '.'
    grid[end[0]][end[1]] = '.'

    def cost_calc(amount):
        return amount

    start_robot = GridRobot(start[0], start[1], cost_calc_fn=cost_calc)
    end_robot = GridRobot(end[0], end[1])
    result = find_all(start_robot, end_robot, grid, best_non_cheat - improvement_needed, max_cheat_dist)
    print('FINAL result', len(result))
    return len(result)


#
assert part12(test_input, 84, 0, 1) == 1
# assert part12(test_input, 84, 2, 2) >= 14 + 14 + 16
# assert part12(test_input, 84, 4, 2) >= 14 + 16
# assert part12(test_input, 84, 6, 2) >= 16
# assert part12(test_input, 84, 8, 2) >= 14
# assert part12(test_input, 84, 10, 2) >= 10
# assert part12(test_input, 84, 12, 2) >= 8
# assert part12(test_input, 84, 20, 2) >= 5
# assert part12(test_input, 84, 36, 2) >= 4
assert part12(test_input, 84, 38, 2) >= 3
assert part12(test_input, 84, 40, 2) >= 2
assert part12(test_input, 84, 64, 2) == 1
assert part12(real_input, 9456, 0, 1) == 1
assert part12(real_input, 9456, 1, 2) >= 1441
assert part12(real_input, 9456, 100, 2) == 1441

assert part12(test_input, 84, 50, 20) >= 32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 52, 20) >= 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 54, 20) >= 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 56, 20) >= 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 58, 20) >= 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 60, 20) >= 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 62, 20) >= 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 64, 20) >= 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 66, 20) >= 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 68, 20) >= 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 70, 20) >= 12 + 22 + 4 + 3
assert part12(test_input, 84, 72, 20) >= 22 + 4 + 3
assert part12(test_input, 84, 74, 20) >= 4 + 3
assert part12(test_input, 84, 76, 20) >= 3
part12(real_input, 9456, 100, 20)
