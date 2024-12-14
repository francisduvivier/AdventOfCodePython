import time

import numpy as np

from grid_robot import DIR, GridRobot

tInput = open('day06-testinput.txt').read().strip()
rInput = open('day06-input.txt').read().strip()


def mapToNumbers(arr):
    return list(map(int, arr))


def parseInput(input):
    lines = input.split('\n')
    char_matrix = np.array([[char for char in line] for line in lines])
    return char_matrix


def find_robot(char_matrix):
    ROBOT_START_CHAR = '^'
    for y, row in enumerate(char_matrix):
        for x, char in enumerate(row):
            if char == ROBOT_START_CHAR:
                return GridRobot(y, x, DIR[ROBOT_START_CHAR])


def part1(input):
    char_matrix = parseInput(input)
    robot = find_robot(char_matrix)
    visited_locations = set()
    visited_locations.add(robot.yx_key())
    while True:
        robot.move_forward()
        while not out_of_bounds(char_matrix, robot) and char_matrix[robot.y][robot.x] == '#':
            robot.move_backward()
            robot.turn_right()
            robot.move_forward()
        if out_of_bounds(char_matrix, robot):
            break
        # print(str(robot))
        char_matrix[robot.y][robot.x] = 'X'
        visited_locations.add(robot.yx_key())

    print(len(visited_locations))
    return len(visited_locations)


def robot_x_y(robot):
    return str(robot.x) + ',' + str(robot.y)


def out_of_bounds(char_matrix, robot):
    return robot.y < 0 or robot.y >= len(char_matrix) or robot.x < 0 or robot.x >= len(char_matrix[robot.y])


assert part1(tInput) == 41
part1(rInput)


def check_loop(char_matrix, extra_y, extra_x):
    robot = find_robot(char_matrix)
    char_matrix = np.array(char_matrix)
    char_matrix[extra_y][extra_x] = '#'
    visited_states = set()
    visited_states.add(robot.state_key())
    while True:
        robot.move_forward()
        while not out_of_bounds(char_matrix, robot) and char_matrix[robot.y][robot.x] == '#':
            robot.move_backward()
            robot.turn_right()
            robot.move_forward()
        if out_of_bounds(char_matrix, robot):
            return 0
        # print(str(robot))
        char_matrix[robot.y][robot.x] = 'X'
        len_before = len(visited_states)
        visited_states.add(robot.state_key())
        if len_before == len(visited_states):
            # print('found a loop')
            return 1


def part2(input):
    char_matrix = parseInput(input)
    loops = 0
    for y in range(len(char_matrix)):
        for x in range(len(char_matrix[y])):
            char = char_matrix[y][x]
            if char != '#' and char != '^':
                loops += check_loop(char_matrix, y, x)

    print(loops)
    return loops


assert part2(tInput) == 6
part2(rInput)
