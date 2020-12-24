import time

from util import mapl

tInput = open('day24-testinput.txt').read().strip().splitlines()
rInput = open('day24-input.txt').read().strip().splitlines()

DIRS = ['ne', 'nw', 'se', 'sw', 'w', 'e']


def part1(input):
    lines = input
    tileFlips = []
    for line in lines:
        for dir in DIRS:
            line = line.replace(dir, dir.capitalize() + ',').strip(',')
        dirList = line.lower().split(',')
        print('dirList', dirList)
        tileFlips.append(dirList)


if __name__ == '__main__':
    assert part1(tInput) == 306
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    # assert part1_r == 31308
    # assert part2('Player 1:\n43\n19\n\nPlayer 2:\n2\n29\n14') != None
    # assert part2(tInput) == 291
    # part2_r = part2(rInput)
    # print(['part2 real', part2_r])
    # assert part2_r == 33647
