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
    row = 0
    col = 0
    dir = {'row': 1, 'col': 0}
    for instruct in input:
        letter = instruct[0]
        amount = int(instruct[1:])
        if letter == 'N':
            # means to move north by the given value.
            row -= amount
        if letter == 'S':
            # means to move south by the given value.
            row += amount
        if letter == 'E':
            # means to move east by the given value.
            col += amount
        if letter == 'W':
            # means to move west by the given value.
            col -= amount
        if letter == 'L' or letter == 'R':
            print(dir)
            # L means to turn left the given number of degrees.
            # R means to turn right the given number of degrees.
            if amount == 180:
                dir['row'] = -dir['row']
                dir['col'] = -dir['col']
            else:  # 90
                if amount == 270:
                    letter = 'L' if letter == 'R' else 'R'
                amount = 90
                assert amount == 90
                if dir['row'] == 1:
                    dir['col'] = -1 if letter == 'L' else 1
                    dir['row'] = 0
                elif dir['row'] == -1:
                    dir['col'] = 1 if letter == 'L' else -1
                    dir['row'] = 0
                elif dir['col'] == 1:
                    dir['row'] = 1 if letter == 'L' else -1
                    dir['col'] = 0
                elif dir['col'] == -1:
                    dir['row'] = -1 if letter == 'L' else 1
                    dir['col'] = 0
            print([letter, amount, dir])
        if letter == 'F':
            # means to move forward by the given value in the direction
            col += dir['col'] * amount
            row += dir['row'] * amount
    return row + col


if __name__ == '__main__':
    # print(['part1', (part1(tInput))])
    print(['part1', part1(rInput)])
    # print(['part2', (part2(tInput))])
    # print(['part2', (part2(rInput))])
