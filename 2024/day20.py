from functools import cache

import numpy as np
from numpy.f2py.f90mod_rules import options

from grid_robot import find_value, GridRobot, DIRS, DIR, yx_key
import sys

sys.setrecursionlimit(15000000)

test_input = open('day20-testinput.txt').read().strip()
real_input = open('day20-input.txt').read().strip()

DEBUG = False


def parse_input(input):
    lines = input.splitlines()
    char_matrix = [[char for char in line] for line in lines]
    return np.array(char_matrix)[1:-1, 1:-1]


def get_next_dirs_4(robot: GridRobot, max_cheat_dist):
    clones = [robot.clone_forward(dir) for dir in DIRS]
    clones_in_bounds = [clone for clone in clones if not clone.out_of_bounds()]
    options = [clone for clone in clones_in_bounds if clone.tile_value() == '.']

    if max_cheat_dist > 1 and robot.cheat is None:
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
    cheater_eq_map = {}  # yx_key to map of cheat_key to robot
    remaining_cost_map = {}  # yx_key to min_remaining_cost

    def update_remaining_costs(rem, r):
        if DEBUG: assert not r.path_tiles[-1].startswith('CHEAT')
        # if DEBUG: assert not r.cost + rem <= max_cost
        done_robots_min_remaining = set()
        min_options = [(rem, r)]
        sortkey = lambda el: el[0]
        while len(min_options):
            min_options.sort(key=sortkey, reverse=True)
            remaining, curr = min_options.pop()
            curr_key = curr.yx_key()
            if curr_key in remaining_cost_map and remaining_cost_map[curr_key] < remaining:
                remaining = remaining_cost_map[curr_key]
            else:
                remaining_cost_map[curr_key] = remaining
            assert not curr.path_tiles[-1].startswith('CHEAT')
            for index, key in enumerate(reversed(curr.path_tiles[:-1])):
                if key.startswith('CHEAT'):
                    break
                new_min_remaining = remaining + 1 + index
                if key not in remaining_cost_map or remaining_cost_map[key] > new_min_remaining:
                    remaining_cost_map[key] = new_min_remaining
                if key not in cheater_eq_map:
                    continue
                subs = cheater_eq_map[key]
                for sub in subs.copy():
                    if sub in done_robots_min_remaining:
                        continue
                    if (sub.cost + new_min_remaining) > max_cost:
                        subs.remove(sub)
                        done_robots_min_remaining.add(sub)
                    else:
                        great_cheats.add(sub.cheat)
                    done_robots_min_remaining.add(sub)
                    min_options.append((new_min_remaining, sub))

    def add_r(r):
        r_key = r.yx_key()
        cheated = r.cheat is not None
        if DEBUG: assert r.yx_key() not in r.path_tiles[:-1]
        if DEBUG: assert r_key not in found_states[cheated]
        found_states[cheated][r_key] = r
        if cheated:
            cheater_eq_map[r_key] = []
        sub_states = get_next_states(r)
        for sub_r in sub_states:
            min_cost = min_possible_cost(sub_r)
            if min_cost > max_cost:
                continue
            insert_sorted(sub_r)

    def insert_sorted(rob):
        sorted_states_to_try.insert(0, rob)

    def get_robot_cost_neg(r):
        return -r.cost

    def min_possible_cost(r):
        key = r.yx_key()
        if key in remaining_cost_map and r.cheat:
            min_remaining_cost = remaining_cost_map[key]
            if DEBUG: assert r.cost + min_remaining_cost >= minimal_possible_cost_for_position(r)
            return r.cost + min_remaining_cost
        return minimal_possible_cost_for_position(r)

    great_cheats = set()
    solutions = []
    while len(sorted_states_to_try) > 0:
        sorted_states_to_try.sort(key=get_robot_cost_neg)
        popped_rob = sorted_states_to_try.pop()
        popped_key = popped_rob.yx_key()
        end_found = end_check(popped_rob)
        remaining = 0
        # if popped_rob.cheat and popped_key in remaining_cost_map:
        #     remaining = remaining_cost_map[popped_key]
        #     if remaining + popped_rob.cost <= max_cost:
        #         end_found = True
        #     else:
        #         continue
        #         # assert remaining + popped_rob.cost <= max_cost
        if end_found:
            if remaining == 0: print('found path', popped_rob, popped_rob.cost)
            if popped_rob.cheat not in great_cheats:
                great_cheats.add(popped_rob.cheat)
                solutions.append((remaining, popped_rob))  # WHY IS THIS NEEDED
            update_remaining_costs(remaining, popped_rob)
            continue
        if popped_key in found_states[False]:
            if DEBUG: assert found_states[False][popped_key].cost <= popped_rob.cost
            continue
        if popped_rob.cheat is None:
            add_r(popped_rob)
            continue
        if popped_key in cheater_eq_map:
            if DEBUG: assert found_states[True][popped_key].cost <= popped_rob.cost
            # if DEBUG: assert len([c for c in cheater_eq_map[next_key] if c.cheat == next_r.cheat]) == 0
            cheater_eq_map[popped_key].append(popped_rob)
            continue
        add_r(popped_rob)

    for rem, r in solutions:
        update_remaining_costs(rem, r)
    cheats = gather_eq_tiles(solutions, cheater_eq_map, max_cost, remaining_cost_map)
    if DEBUG: print('cheats', len(cheats), cheats)
    cheats = cheats.union(great_cheats)
    if DEBUG: print('cheats.union(great_cheats)', len(cheats), cheats)
    return cheats


def gather_eq_tiles(solutions, cheater_eq_map, max_cost, min_cost_map):
    cheats = set([r.cheat for rem, r in solutions])
    for option in min_cost_map:
        if option in cheater_eq_map:
            for cheater in cheater_eq_map[option]:
                if cheater.cost + min_cost_map[option] <= max_cost:
                    cheats.add(cheater.cheat)

    # print('cheats1', len(cheats), cheats)
    return cheats


def print_path(sol):
    return ((sol.cheat or '') + ':' + str(sol.cost)).ljust(30) + str(sol.path_tiles)


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
assert part12(test_input, 84, 2, 2) == 14 + 14 + 16
assert part12(test_input, 84, 4, 2) == 14 + 16
assert part12(test_input, 84, 6, 2) == 16
assert part12(test_input, 84, 8, 2) == 14
assert part12(test_input, 84, 10, 2) == 10
assert part12(test_input, 84, 12, 2) == 8
assert part12(test_input, 84, 20, 2) == 5
assert part12(test_input, 84, 30, 2) == 4
assert part12(test_input, 84, 38, 2) == 3
assert part12(test_input, 84, 40, 2) == 2
assert part12(test_input, 84, 64, 2) == 1
assert part12(real_input, 9456, 0, 1) == 1
assert part12(real_input, 9456, 1, 2) >= 1441
assert part12(real_input, 9456, 100, 2) == 1441

assert part12(test_input, 84, 50, 20) == 32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 52, 20) == 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 54, 20) == 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 56, 20) == 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 58, 20) == 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 60, 20) == 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 62, 20) == 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 64, 20) == 19 + 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 66, 20) == 12 + 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 68, 20) == 14 + 12 + 22 + 4 + 3
assert part12(test_input, 84, 70, 20) == 12 + 22 + 4 + 3
assert part12(test_input, 84, 72, 20) == 22 + 4 + 3
assert part12(test_input, 84, 74, 20) == 4 + 3
assert part12(test_input, 84, 76, 20) == 3
part12(real_input, 9456, 100, 20)
