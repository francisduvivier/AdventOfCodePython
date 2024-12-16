import time

import numpy as np

from util import map_to_numbers, sub_map_to_numbers

test_input = open('day16-testinput.txt').read().strip()
test_input = open('day16-testinput2.txt').read().strip()
real_input = open('day16-input.txt').read().strip()

def parse_input(input):
    lines = input.splitlines()
    line_split_lambda = lambda line: line.split(' ')
    char_matrix = np.array([line_split_lambda(line) for line in lines])
    return char_matrix


def part1(input):
    parsed = parse_input(input)

    print(result)
    return result

assert part1(test_input) == 7036
assert part1(test_input2) == 11048
part1(real_input)
