import time

import numpy as np

from util import map_to_numbers

tInput = open('day12-testinput.txt').read().strip()
rInput = open('day12-input.txt').read().strip()


def parseInput(input):
    lines = input.splitlines()
    char_matrix = np.array([[char for char in line] for line in lines])
    return char_matrix


def part1(input):
    # A wall can be modelled as a full robot state, so a location+direction
    # We can gather all the walls by letting the robot explore the space until it can no longer continue, then we have found a wall, like in day06 I think
    # so then wel will have a list of tiles and walls, then we just need to loop over all tiles, do this search and additionally keep a map so that we know which tile are already in a patch
    # tiles that are already in a patch can be skipped.
    # so patch has {tiles: stateKeys, wallSet: wall keys}
    # we have global map: tilekey->patch
    # we also keep a list of patches
    # then we can calc for each patch the cost: nbTiles x nbWalls
    parsed = parseInput(input)
    result = parsed
    print(result)
    return result

assert part1(tInput) == 1930
part1(rInput)
