rInput = [11, 18, 0, 20, 1, 7, 16]
tInput = [0, 3, 6]


def part1(input):
    return calc_number(input, 2020 - 1)


def part2(input):
    return calc_number(input, 30000000 - 1)


def calc_number(input, index):
    input = input.copy()
    startLen = len(input)
    lastIndexMap = dict()
    prevNumber = input.pop()
    for i, n in enumerate(input):
        lastIndexMap[n] = i
    for i in range(startLen - 1, index):
        newNumber = 0
        if prevNumber in lastIndexMap:
            newNumber = i - lastIndexMap[prevNumber]
        lastIndexMap[prevNumber] = i
        prevNumber = newNumber
    print(prevNumber)
    return prevNumber


if __name__ == '__main__':
    part1_t = part1(tInput)
    print(['part1 test', (part1_t)])
    assert part1_t == 436
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    part2_r = part2(rInput)
    print(['part2 real', part2_r])
    assert part2([0, 3, 6]) == 175594
    assert part2([3, 2, 1]) == 18
    assert part2([3, 1, 2]) == 362
    assert part2([1, 3, 2]) == 2578
    assert part2([1, 2, 3]) == 261214
    assert part2([2, 1, 3]) == 3544142
    assert part2([2, 3, 1]) == 6895259

