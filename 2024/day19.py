import re
import time
from functools import cache

import numpy as np

from util import map_to_numbers, sub_map_to_numbers

test_input = open('day19-testinput.txt').read().strip()
real_input = open('day19-input.txt').read().strip()


def parse_input(input):
    # r, wr, b, g, bwu, rb, gb, br
    #
    # brwrr
    # bggr
    (towels_line, design_lines) = input.split('\n\n')
    towels = [towel for towel in towels_line.split(', ')]
    designs = design_lines.splitlines()
    return towels, designs

@cache
def find_nb_solutions_rec(remaining, towels_joined):
    options = towels_joined.split(',')
    if remaining == '':
        return 1
    return sum(
        [find_nb_solutions_rec(remaining[:-len(option)], towels_joined) for option in options if
         remaining.endswith(option)]
    )


def possible(design, towels):
    towels_joined = ','.join(towels)
    return find_nb_solutions_rec(design, towels_joined)


def part1(input):
    towels, designs = parse_input(input)
    nb_possible = sum([1 for design in designs if possible(design, towels)])
    print(nb_possible)
    return nb_possible


assert part1(test_input) == 6
part1(real_input)


def part2(input):
    towels, designs = parse_input(input)
    nb_possible = sum([possible(design, towels) for design in designs])
    print(nb_possible)
    return nb_possible


assert part2(test_input) == 16
part2(real_input)
