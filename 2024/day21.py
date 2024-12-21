import time

import numpy as np

from util import map_to_numbers, sub_map_to_numbers

test_input = open('day21-testinput.txt').read().strip()
real_input = open('day21-input.txt').read().strip()

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

# 68 * 29, 60 * 980, 68 * 179, 64 * 456, 64 * 379. Adding these together produces 126384.
assert part1(test_input) == [(68 , 29), (60 , 980), (68 , 179), (64 , 456), (64 , 379)]
part1(real_input)
