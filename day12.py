import math


def getTestInput():
    return '''F10
N3
F7
R90
F11'''


tInput = getTestInput().splitlines()
rInput = open('day12-input.txt').read().strip().splitlines()


#  N
# W   E
#  S

def part1(input):
    return follow_instuctions(input, dirMap['E'], False)


dirMap = {'N': {'row': -1, 'col': 0}, 'S': {'row': 1, 'col': 0}, 'W': {'row': 0, 'col': -1}, 'E': {'row': 0, 'col': 1}}


def movePoint(p, dir, amount):
    p['row'] += dir['row'] * amount
    p['col'] += dir['col'] * amount


def follow_instuctions(input, startWp, moveWaypoint):
    ship = {'row': 0, 'col': 0}
    wp = startWp
    print(['_', '_', ship, wp])
    for instruct in input:
        letter = instruct[0]
        amount = int(instruct[1:])
        if letter in dirMap:
            movePoint(wp if moveWaypoint else ship, dirMap[letter], amount)
        if letter == 'L' or letter == 'R':
            wp = rotate_point(amount, letter, wp)
        if letter == 'F':
            movePoint(ship, wp, amount)

        print('[letter, amount, wRow, wCol, wDir, sRow, sCol]')
        print([instruct, ship, wp])
    return abs(ship['row']) + abs(ship['col'])


def rotate_point(amount, letter, p: {'row': int, 'col': int}):
    y = -p['row']
    x = p['col']
    # Positive degrees go counter clockwise (L) if you start at the bottom right
    signedRadians = math.radians(amount * (-1 if letter == 'R' else 1))
    cos = round(math.cos(signedRadians))
    sin = round(math.sin(signedRadians))
    newX = x * cos - y * sin
    newY = x * sin + y * cos
    newP = {'row': -newY, 'col': newX}
    # print(newP, cos, sin, cos)
    return newP


for deg in [180, -180]:
    for dir in ['L', 'R']:
        for row in [0, 1, -1]:
            for col in [0, 1, -1]:
                assert rotate_point(deg, dir, {'row': row, 'col': col}) == {'row': -row, 'col': -col}


def part2(input):
    return follow_instuctions(input, {'row': -1, 'col': 10}, True)


if __name__ == '__main__':
    part_t = part1(tInput)
    print(['part1', (part_t)])
    assert part_t == 25
    part1_r = part1(rInput)
    print(['part1', part1_r])
    assert part1_r == 1482
    part2_t = part2(tInput)
    print(['part2 t', part2_t])
    assert part2_t == 286
    part2_r = part2(rInput)
    print(['part2', part2_r])
    assert part2_r == 48739
