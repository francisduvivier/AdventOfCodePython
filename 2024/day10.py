import time

import numpy as np

from grid_robot import DIR, DIRS, GridRobot

tInput = open('day10-testinput.txt').read().strip()
tInput0 = open('day10-testinput0.txt').read().strip()
tInput1 = open('day10-testinput1.txt').read().strip()
rInput = open('day10-input.txt').read().strip()


def mapToNumbers(arr):
    return list(map(int, arr))


def parseInput(input):
    lines = input.split('\n')
    int_matrix = np.array([[-1 if char == '.' else int(char) for char in line] for line in lines])
    return int_matrix


def part1(input):
    number_matrix = parseInput(input)
    total_score = 0
    for y, row in enumerate(number_matrix):
        for x, char in enumerate(row):
            if char == 0:
                zero_location = GridRobot(y, x)
                total_score += find_nines_rec(zero_location, number_matrix, set())

    print(total_score)
    return total_score


def find_nines_rec(robot_state: GridRobot, int_matrix: np.array, visited_locations: set[int] or None = None):
    if visited_locations is not None:
        if robot_state.yx_key() in visited_locations:
            return 0
        visited_locations.add(robot_state.yx_key())
    if int_matrix[robot_state.y][robot_state.x] == 9:
        return 1
    total_score = 0
    for dir in DIRS:
        new_robot = GridRobot(robot_state.y, robot_state.x, dir)
        new_robot.move_forward()
        if not out_of_bounds(new_robot,
                             int_matrix) and int_matrix[new_robot.y][new_robot.x] == int_matrix[robot_state.y][robot_state.x] + 1:
            total_score += find_nines_rec(new_robot, int_matrix, visited_locations)
    return total_score

def out_of_bounds(robot, int_matrix):
    return robot.y < 0 or robot.y >= len(int_matrix) or robot.x < 0 or robot.x >= len(int_matrix[robot.y])


assert part1(tInput0) == 2
assert part1(tInput) == 36
part1(rInput)


def part2(input):
    number_matrix = parseInput(input)
    total_score = 0
    for y, row in enumerate(number_matrix):
        for x, char in enumerate(row):
            if char == 0:
                zero_location = GridRobot(y, x)
                total_score += find_nines_rec(zero_location, number_matrix)

    print(total_score)
    return total_score


assert part2(tInput1) == 3
assert part2(tInput) == 81
part2(rInput)
