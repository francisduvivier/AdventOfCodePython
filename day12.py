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
    return follow_instuctions(input)


def follow_instuctions(input, startRow=0, startCol=0, startDir={'row': 1, 'col': 0}, waypoint=False):
    wRow = startRow
    wCol = startCol
    wDir = startDir
    sCol = 0
    sRow = 0
    print(['_', '_', wRow, wCol, wDir, sCol, sRow])
    for instruct in input:
        letter = instruct[0]
        amount = int(instruct[1:])
        if letter == 'N':
            # means to move north by the given value.
            wRow -= amount
        if letter == 'S':
            # means to move south by the given value.
            wRow += amount
        if letter == 'E':
            # means to move east by the given value.
            wCol += amount
        if letter == 'W':
            # means to move west by the given value.
            wCol -= amount
        if letter == 'L' or letter == 'R':
            # L means to turn left the given number of degrees.
            # R means to turn right the given number of degrees.
            if amount == 180:
                wDir['row'] = -wDir['row']
                wDir['col'] = -wDir['col']
            else:  # 90
                if amount == 270:
                    letter = 'L' if letter == 'R' else 'R'
                amount = 90
                assert amount == 90
                if wDir['row'] == 1:
                    wDir['col'] = -1 if letter == 'L' else 1
                    wDir['row'] = 0
                elif wDir['row'] == -1:
                    wDir['col'] = 1 if letter == 'L' else -1
                    wDir['row'] = 0
                elif wDir['col'] == 1:
                    wDir['row'] = 1 if letter == 'L' else -1
                    wDir['col'] = 0
                elif wDir['col'] == -1:
                    wDir['row'] = -1 if letter == 'L' else 1
                    wDir['col'] = 0
        if letter == 'F':
            # means to move forward by the given value in the direction
            if waypoint:
                sCol += (wCol - sCol) * amount
                sRow += (wRow - sRow) * amount
            else:
                wCol += wDir['col'] * amount
                wRow += wDir['row'] * amount
        print([letter, amount, wRow, wCol, wDir, sRow, sCol])
    return abs(wRow) + abs(wCol) if not waypoint else abs(sRow) + abs(sCol)


def part2(input):
    return follow_instuctions(input, -1, 10, {'col': 0, 'row': -1}, True)


if __name__ == '__main__':
    # print(['part1', (part1(tInput))])
    # part_ = part1(rInput)
    # print(['part1', part_])
    # assert part_ == 1482
    print(['part2 t', part2(tInput)])
    # print(['part2', part2(rInput)])
