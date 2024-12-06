import time

import numpy as np

from grid_robot import DIR, GridRobot
from util import mapl

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
                return GridRobot(x, y, DIR[ROBOT_START_CHAR])


def part1(input):
    char_matrix = parseInput(input)
    robot = find_robot(char_matrix)
    visited_locations = set()
    visited_locations.add(str(robot))
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
        visited_locations.add(str(robot))

    print(len(visited_locations))


def out_of_bounds(char_matrix, robot):
    return robot.y < 0 or robot.y >= len(char_matrix) or robot.x < 0 or robot.x >= len(char_matrix[robot.y])


part1(tInput)
part1(rInput)
