import re

import numpy as np
from dotmap import DotMap

from grid_robot import GridRobot

test_input = open('day14-testinput.txt').read().strip()
real_input = open('day14-input.txt').read().strip()


def parse_robot(line: str, grid):
    # p=87,24 v=-83,92
    pattern = r'p=(?P<x>\d+),(?P<y>\d+) v=(?P<dx>-?\d+),(?P<dy>-?\d+)'
    match = re.match(pattern, line)
    parsed = DotMap(match.groupdict())
    dir = {'dy': int(parsed.dy), 'dx': int(parsed.dx)}
    return GridRobot(int(parsed.y), int(parsed.x), dir, grid, wrap=True)


def parse_input(input, grid):
    lines = input.splitlines()
    robots = [parse_robot(line, grid) for line in lines]
    return robots


def get_quadrant(robot):
    grid_width = len(robot.grid[0])
    grid_height = len(robot.grid)
    if robot.x == int(grid_width / 2) or robot.y == int(grid_height / 2):
        return None
    x = int(robot.x / (int(grid_width / 2) + 1))
    y = int(robot.y / (int(grid_height / 2) + 1))
    return str(y) + ',' + str(x)
    pass


def part1(input, grid_height, grid_width):
    grid = np.array([['.' for x in range(grid_width)] for y in range(grid_height)])
    robots = parse_input(input, grid)
    for second in range(100):
        for robot in robots:
            robot.move_forward()
    quadrantscore = {
        '0,0': 0,
        '0,1': 0,
        '1,0': 0,
        '1,1': 0,
    }
    for robot in robots:
        quadrant = get_quadrant(robot)
        if quadrant:
            quadrantscore[quadrant] += 1
    result = 1
    for score in quadrantscore.values():
        result *= score
    print(result)
    return result


assert part1(test_input, 7, 11) == 12
print('Check success!')
part1(real_input, 103, 101)


def get_grid(robots):
    grid = robots[0].grid.copy()
    for robot in robots:
        grid[robot.y][robot.x] = '#'
    return grid


def part2(input, grid_height, grid_width):
    grid = np.array([['.' for x in range(grid_width)] for y in range(grid_height)])
    robots = parse_input(input, grid)
    state_map = dict()
    min_score = 2 ** 32
    min_score_time = 0
    min_score_grid = None
    for second in range(1, 10_000_000_000):
        state = ''
        for robot in robots:
            robot.move_forward()
            state += str(robot)

        score = cluster_score(robots)
        if not min_score or min_score > score:
            min_score = score
            min_score_time = second
            min_score_grid = get_grid(robots)
        if state in state_map:
            result = state_map[state]
            print('found repeat at' + str(second) + ' for second' + str(result))
            print('\n'.join([''.join(line) for line in min_score_grid]))
            print('min_score_time', min_score_time)
            return min_score_time
        state_map[state] = second
    raise Exception('no solution')


def cluster_score(robots):
    rxs = [robot.x for robot in robots]
    median_x = np.median(rxs)
    msx = np.sum(np.square([median_x - other for other in rxs]))
    rys = [robot.y for robot in robots]
    median_y = np.median(rys)
    msy = np.sum(np.square([median_y - other for other in rys]))
    return msx + msy

# part2(test_input, 7, 11)
print('test_input success')
part2(real_input, 103, 101)
