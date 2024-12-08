import time

import numpy as np

from util import map_to_numbers

tInput = open('day08-testinput.txt').read().strip()
rInput = open('day08-input.txt').read().strip()


def parseInput(input):
    lines = input.splitlines()
    char_matrix = np.array([[char for char in line] for line in lines])
    return char_matrix


# condition for anitnode is that -given dx=x2-x1, dy=y2-y1: dx1/dy1 == dx2/dy2 and also dx1 == dx2 and dy1 == dy2 wit right polarity
# but can be more than 2, so for each pair ...
#  so I will need a map from char to list of locations with that char, so let's make a function that takes a charmatrix and converts it to a dict of
# char to list of [row, col] (or [y, x])
# then with this list, I can do O(N2) loop for so I get a the combination of pairs
# then for each pair I can calculate the dx and dy and then with that calculate an antinode location and check if it is out of bounds
# so that will be a function that takes a pair and updates a set of antinodes, it actually does not need to do both dirs, I can use the O(N2) loop for that since I will always get the pair double.

# Q before we start: are anitinodes unique for the freq or is that then the same antinode? No, In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency.
def get_location_list_for_char_map(char_matrix: np.array(np.array(str))) -> dict[str, list[tuple[int, int]]]:
    char_map = {}
    for row in range(len(char_matrix)):
        for col in range(len(char_matrix[row])):
            char = char_matrix[row][col]
            if char not in char_map:
                char_map[char] = []
            char_map[char].append((row, col))
    return char_map


def part1(input):
    char_matrix = parseInput(input)
    location_list_for_char_map = get_location_list_for_char_map(char_matrix)
    antinodes = set()
    # Now we need to loop over all pairs of locations for each char
    for (char, locations) in location_list_for_char_map.items():
        if char == '.':
            continue
        for location in locations:
            for location2 in locations:
                if location == location2:
                    continue
                # print(location, location2)
                # Now we need to calculate the dx and dy
                dx = location2[1] - location[1]
                dy = location2[0] - location[0]
                antinode_row_col = (location2[0] + dy, location2[1] + dx)
                if not is_out_of_bounds(antinode_row_col, char_matrix):
                    antinodes.add(tuple_to_key(antinode_row_col))
                    print(char, antinode_row_col)
    result = len(antinodes)
    print(result)
    return result


def is_out_of_bounds(antinode_row_col, char_matrix):
    rows = len(char_matrix)
    cols = char_matrix[0]
    row = antinode_row_col[0]
    col = antinode_row_col[1]
    return row < 0 or row >= rows or col < 0 or col >= len(cols)


def tuple_to_key(antinode):
    return str(antinode[0]) + ',' + str(antinode[1])


assert part1(tInput) == 14
part1(rInput)
