import re
import time

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

def possible(design, towels):
    towelMatcher = '('+'|'.join(towels)+')+'
    return re.fullmatch(towelMatcher, design) is not None


def part1(input):
    towels, designs = parse_input(input)
    nb_possible = sum([1 for design in designs if possible(design, towels)])
    print(nb_possible)
    return nb_possible

assert part1(test_input) == 6
part1(real_input)
