tInput = open('day17-testinput.txt').read().strip().splitlines()
rInput = open('day17-input.txt').read().strip().splitlines()


def getAdjacents(active):
    result = []
    z2Options = [0, -1, 1] if 'z2' in active else [0]
    for row in [-1, 0, 1]:
        for col in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                for z2 in z2Options:
                    if any([row, col, z, z2]):
                        nb = {'row': active['row'] + row, 'col': active['col'] + col, 'z': active['z'] + z}
                        if 'z2' in active:
                            nb['z2'] = active['z2'] + z2
                        result.append(nb)
    assert len(result) == (80 if 'z2' in active else 26)
    return result


toKey = str


def doCycle(actives):
    countMap = dict()
    for active in actives:
        adjacents = getAdjacents(active)
        for nb in adjacents:
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


def part2(input):
    actives: [{'row': int, 'col': int, 'z': int, 'nb': (int or None), 'z2': int}] = []
    for row, line in enumerate(input):
        for col, letter in enumerate(line):
            if letter == '#':
                actives.append({'row': row, 'col': col, 'z': 0, 'z2': 0})
    playGame(actives, 6)
    return len(actives)


if __name__ == '__main__':
    part1_t = part1(tInput)
    print(['part1 test', (part1_t)])
    assert part1_t == 112
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 265
    assert part2(tInput) == 848
    part2_r = part2(rInput)
    print(['part2 real', part2_r])
