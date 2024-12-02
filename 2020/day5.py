def toSeat(line: str):
    binary = line.replace('F', '0', 8).replace('L', '0', 8).replace('B', '1', 8).replace('R', '1', 8)

    return {'row': int(binary[:7], 2), 'col': int(binary[7:], 2)}


def toId(seat):
    return seat['row'] * 8 + seat['col']


def part1():
    input: str = open('day5-input.txt', 'r').read()
    lines = list(input.split('\n'))
    seats = map(toSeat, lines)
    ids = map(toId, seats)
    print('max id: ' + str(max(ids)))


def part2():
    input: str = open('day5-input.txt', 'r').read()
    lines = list(input.split('\n'))
    seats = map(toSeat, lines)
    ids = list(sorted(map(toId, seats)))
    prevId = ids[0]
    for id in ids[1:]:
        if (prevId + 2 == id):
            print('part 2: '+str(prevId + 1))
        prevId = id
    return


if __name__ == '__main__':
    print('started\n')
    part1()
    part2()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
