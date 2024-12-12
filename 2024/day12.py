import time

import numpy as np

from grid_robot import yx_key, GridRobot, DIRS, parse_state_key, DIR_LETTERS

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
    row_col_key = yx_key(row, col)
    if row_col_key in patch["tile_set"]:
        return
    patch["tile_set"].add(row_col_key)
    for dir in DIRS:
        new_robot = GridRobot(col, row, dir)
        new_robot.move_forward()
        patch_letter = patch["letter"]
        if out_of_bounds(garden, new_robot) or garden[new_robot.y][new_robot.x] != patch_letter:
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
    patches = find_patches(garden)

    result = sum([calc_price(patch) for patch in patches])
    print(result)
    return result


def find_patches(garden):
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
    return patches


# assert part1(tInput0) == 140
# assert part1(tInput) == 1930
# part1(rInput)


def find_disconnected_walls(wall_set):
    print(wall_set)
    walls = [parse_state_key(wall_key) for wall_key in wall_set]
    nb_disconnected = 0
    x_index = 1
    y_index = 0
    for dir in ['>', '<']:
        walls_for_dir = [wall for wall in walls if wall[2] == dir]
        print(walls_for_dir)
        x_values = set([wall[x_index] for wall in walls_for_dir])
        for x in x_values:
            sorted_walls_on_line = sorted([wall for wall in walls_for_dir if wall[x_index] == x],
                                          key=lambda wall: wall[y_index])
            curr_y = None
            for sorted_wall in sorted_walls_on_line:
                if curr_y != sorted_wall[y_index] - 1:
                    print('found disconnect for dir', dir, 'x', x, 'curr_y', curr_y, '->', sorted_wall[y_index])
                    nb_disconnected += 1
                curr_y = sorted_wall[y_index]
    for dir in ['^', 'v']:
        walls_for_dir = [wall for wall in walls if wall[2] == dir]
        print(walls_for_dir)
        y_values = set([wall[y_index] for wall in walls_for_dir])
        for y in y_values:
            sorted_walls_on_line = sorted([wall for wall in walls_for_dir if wall[y_index] == y],
                                          key=lambda wall: wall[x_index])
            curr_x = None
            for sorted_wall in sorted_walls_on_line:
                if curr_x != sorted_wall[x_index] - 1:
                    nb_disconnected += 1
                    print('found disconnect for dir', dir, 'y', y, 'curr_x', curr_x, '->', sorted_wall[x_index])
                curr_x = sorted_wall[x_index]
    return nb_disconnected


def calc_price2(patch):
    print('calc_price2: ' + patch['letter'])
    nb_disconnected = find_disconnected_walls(patch["wall_set"])
    print('nb_disconnected', patch['letter'], nb_disconnected)

    return nb_disconnected * len(patch['tile_set'])


def part2(input):
    # for wall in patch
    # for y in rows
    # get_disconnected_y(walls,y)

    # for x in cols
    # get_disconnected_x(wall,x)
    garden = parseInput(input)
    patches = find_patches(garden)

    result = sum([calc_price2(patch) for patch in patches])

    print(result)
    return result


assert part2(tInput0) == 80
assert part2(tInput) == 1206
part2(rInput)
