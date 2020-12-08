def isOk(lines: [str], row, col):
    return lines[row][col % len(lines[row])] == '#'


def part1():
    input: str = open('day3-input.txt', 'r').read()
    lines = list(input.split('\n'))
    colSlope = 3
    rowSlope = 1
    treesHit = checkTreesHit(colSlope, rowSlope, lines)

    print('treesHit: ' + str(treesHit))


def checkTreesHit(colSlope, rowSlope, lines):
    treesHit = 0
    row = 0
    col = 0
    while row + rowSlope < len(lines):
        row += rowSlope
        col += colSlope
        if isOk(lines, row, col):
            treesHit += 1
    return treesHit


def part2():
    input: str = open('day3-input.txt', 'r').read()
    lines = list(input.split('\n'))
    slopes = [[1, 1],
              [3, 1],
              [5, 1],
              [7, 1],
              [1, 2]]
    treesHit = 1
    for slope in slopes:
        treesHit *= checkTreesHit(slope[0], slope[1], lines)

    print('treesHit: ' + str(treesHit))


if __name__ == '__main__':
    print('started\n')
    part1()
    part2()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
