import time

import numpy as np

from util import map_to_numbers, sub_map_to_numbers

test_input = open('day14-testinput.txt').read().strip()
real_input = open('day14-input.txt').read().strip()

def parse_input(input):
    lines = input.splitlines()
    line_split_lambda = lambda line: line.split(' ')
    char_matrix = [line_split_lambda(line) for line in lines]
    numbers_matrix = sub_map_to_numbers(char_matrix)
    return numbers_matrix


def part1(input):
    parsed = parse_input(input)
    result = sum(parsed[0])
    print(result)
    return result

assert part1(test_input) == 20
part1(real_input)
