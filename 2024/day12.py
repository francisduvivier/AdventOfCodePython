import time

import numpy as np

from grid_robot import yx_key, GridRobot, DIRS
from util import map_to_numbers

tInput0 = open('day12-testinput0.txt').read().strip()
tInput = open('day12-testinput.txt').read().strip()
rInput = open('day12-input.txt').read().strip()


def parseInput(input):
    lines = input.splitlines()
    char_matrix = np.array([[char for char in line] for line in lines])
    return char_matrix

def out_of_bounds(char_matrix, robot):
    return robot.y < 0 or robot.y >= len(char_matrix) or robot.x < 0 or robot.x >= len(char_matrix[robot.y])


def find_patch_rec(row, col, garden, patch):
    robot = GridRobot(row, col)
    if robot.yx_key() in patch["tile_set"]:
        return
    patch["tile_set"].add(robot.yx_key())
    for dir in DIRS:
        new_robot = GridRobot(row, col, dir)
        new_robot.move_forward()
        if out_of_bounds(garden, new_robot) or garden[new_robot.y][new_robot.x] != patch["letter"]:
            new_robot.move_backward()
            patch["wall_set"].add(new_robot.state_key())
        else:
            find_patch_rec(new_robot.y, new_robot.x, garden, patch)



def find_patch(row, col, garden):
    patch = {
        "tile_set": set(),
        "wall_set": set(),
        "letter": garden[row][col]
    }
    find_patch_rec(row, col, garden, patch)
    return patch


def calc_price(patch):
    return len(patch["tile_set"]) * len(patch["wall_set"])


def part1(input):
    # A wall can be modelled as a full robot state, so a location+direction
    # We can gather all the walls by letting the robot explore the space until it can no longer continue, then we have found a wall, like in day06 I think
    # so then wel will have a list of tiles and walls, then we just need to loop over all tiles, do this search and additionally keep a map so that we know which tile are already in a patch
    # tiles that are already in a patch can be skipped.
    # so patch has {tiles: stateKeys, wallSet: wall keys}
    # we have global map: tilekey->patch
    # we also keep a list of patches
    # then we can calc for each patch the cost: nbTiles x nbWalls
    garden = parseInput(input)
    done_tile_set = set()
    patches = []

    def add_patch(new_patch):
        for tile_key in new_patch["tile_set"]:
            done_tile_set.add(tile_key)
        patches.append(new_patch)

    for row in range(len(garden)):
        for col, letter in enumerate(garden[row]):
            if yx_key(row, col) in done_tile_set:
                print('skipping ', row, col, letter)
                continue
            print('doing ', row, col, letter)
            patch = find_patch(row, col, garden)
            add_patch(patch)

    result = sum([calc_price(patch) for patch in patches])
    print(result)
    return result


assert part1(tInput0) == 140
assert part1(tInput) == 1930
part1(rInput)
