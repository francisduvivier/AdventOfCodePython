tInput = open('day18-testinput.txt').read().strip().splitlines()
rInput = open('day18-input.txt').read().strip().splitlines()


def calcLine(line):
    parts = line.split(' ')
    currString = ''
    suffix = ''
    for part in parts:
        currString += part
        if part == '*':
            currString += '('
            suffix += ')'
    print(currString, suffix, eval(currString + suffix))

    return eval(currString + suffix)


def part1(input):
    sum = 0
    for line in input:
        sum += calcLine(line)
    return sum


if __name__ == '__main__':
    assert calcLine(tInput[0]) == 26
    assert calcLine(tInput[1]) == 437
    assert calcLine(tInput[2]) == 12240
    assert calcLine(tInput[3]) == 13632
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    # assert part1_r == 265
    # assert part2(tInput) == 848
    # part2_r = part2(rInput)
    # print(['part2 real', part2_r])
