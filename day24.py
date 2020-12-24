import time

from util import mapl

tInput = open('day24-testinput.txt').read().strip().splitlines()
rInput = open('day24-input.txt').read().strip().splitlines()

DIRS = ['ne', 'nw', 'se', 'sw', 'w', 'e']


def part1(input):
    tileFlips: [[str]] = parseInput(input)
    tileFlipIds = calcTileIds(tileFlips)
    result = len(tileFlipIds)
    print('len(tileFlipIds)', result)
    return result


def calcTileIds(tileFlips):
    tileFlipIds = set()
    for tileFlip in tileFlips:
        tileId = calcTileId(tileFlip)
        if tileId in tileFlipIds:
            tileFlipIds.remove(tileId)
        else:
            tileFlipIds.add(tileId)
    return tileFlipIds


def calcTileId(tileFlip):
    dirCounts = {}
    for dir in DIRS:
        dirCounts[dir] = tileFlip.count(dir)
    NE = dirCounts['ne'] - dirCounts['sw']
    SE = dirCounts['se'] - dirCounts['nw']
    E = dirCounts['e'] - dirCounts['w']
    N = NE - SE
    E = 2 * E + NE + SE
    tileId = ','.join(mapl(str, [N, E]))
    print('tileId', tileId)
    return tileId


def parseInput(lines):
    tileFlips = []
    for line in lines:
        dirList = calcDirList(line)
        tileFlips.append(dirList)
    return tileFlips


def calcDirList(line):
    for dir in DIRS:
        line = line.replace(dir, dir.swapcase() + ',').strip(',')
    dirList = line.lower().split(',')
    print('dirList', dirList)
    return dirList


assert calcTileId(calcDirList('esew')) == '-1,1'
assert calcTileId(calcDirList('nwwswee')) == '0,0'
if __name__ == '__main__':
    assert part1(tInput) == 10
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 411
    # assert part2(tInput) == 291
    # part2_r = part2(rInput)
    # print(['part2 real', part2_r])
    # assert part2_r == 33647
