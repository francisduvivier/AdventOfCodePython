tInput = open('day17-testinput.txt').read().strip().splitlines()
rInput = open('day17-input.txt').read().strip().splitlines()


def neighbors(active):
    result = []
    for row in [-1, 0, 1]:
        for col in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                if any([row, col, z]):
                    result.append({'row': active['row'] + row, 'col': active['col'] + col, 'z': active['z'] + z})
    return result


toKey = str


def doCycle(actives):
    countMap = dict()
    for active in actives:
        for nb in neighbors(active):
            key = toKey(nb)
            if key in countMap:
                countMap[key]['count'] += 1
            else:
                countMap[key] = nb
                nb['count'] = 1
    newInactives = []
    for active in actives:
        key = toKey(active)
        count = 0
        if key in countMap:
            count = countMap[key]['count']
            del countMap[key]
        if not (count == 3 or count == 2):
            newInactives.append(active)
    for nia in newInactives: actives.remove(nia)
    for inactive in countMap.values():
        if inactive['count'] == 3:
            del inactive['count']
            actives.append(inactive)


def playGame(actives, cycles):
    for i in range(cycles):
        doCycle(actives)
    pass


def part1(input):
    actives: [{'row': int, 'col': int, 'z': int, 'nb': (int or None)}] = []
    for row, line in enumerate(input):
        for col, letter in enumerate(line):
            if letter == '#':
                actives.append({'row': row, 'col': col, 'z': 0})
    playGame(actives, 6)
    return len(actives)


if __name__ == '__main__':
    part1_t = part1(tInput)
    print(['part1 test', (part1_t)])
    assert part1_t == 112
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    # assert part2(tInput2)
    # part2_r = part2(rInput)
    # # print(['part2 real', part2_r])
