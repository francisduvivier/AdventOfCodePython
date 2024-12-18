import time

import numpy as np
from dotmap import DotMap

from grid_robot import print_grid
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
def part1(input, slice, grid_size):
    blocks = parse_input(input)[0:slice]
    grid = np.array([['.' for x in range(grid_size)] for y in range(grid_size)])
    for block in blocks:
        grid[block.y][block.x] = '#'
    if DEBUG: print_grid(grid)

    return 0


assert part1(test_input, 12, 6+1) == 20
part1(real_input, 1024, 70+1)
