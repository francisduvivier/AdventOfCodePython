tInput = open('day18-testinput.txt').read().strip().splitlines()
rInput = open('day18-input.txt').read().strip().splitlines()


def calcMapRec(map):
    return 1


import re


def doCalcPart2(subCalc):
    print('doCalc subCalc', subCalc)
    result = subCalc[0]
    subCalcString = ''.join(list(map(str, subCalc)))
    subCalcString = re.sub(r'([0-9+]+)', r'(\1)', subCalcString)
    return eval(subCalcString)


def doCalcPart1(subCalc):
    print('doCalc subCalc', subCalc)
    result = subCalc[0]
    for i in range(1, len(subCalc) - 1, 2):
        toEval = str(result) + str(subCalc[i]) + str(subCalc[i + 1])
        print('toEval', toEval)
        result = eval(toEval)
    return result


def calcLine(line, simpleCalcFunc=doCalcPart1):
    parts = list(filter(lambda ch: ch != ' ', [char for char in line]))
    print('parts', parts)
    deepCalcList = []
    calcStack = []
    for part in parts:
        if part == '(':
            subCalc = []
            deepCalcList.append(subCalc)
            calcStack.append(deepCalcList)
            deepCalcList = subCalc
            pass
        elif part == ')':
            currCalc = deepCalcList
            deepCalcList = calcStack.pop()
            subCalc = deepCalcList.pop()
            assert subCalc == currCalc
            subCalcResult = simpleCalcFunc(subCalc)
            deepCalcList.append(subCalcResult)
            pass
        else:
            deepCalcList.append(part)
    print(deepCalcList)
    result = simpleCalcFunc(deepCalcList)
    print([line, deepCalcList, result])

    return result


def part1(input):
    sum = 0
    for line in input:
        sum += calcLine(line, doCalcPart1)
    return sum


def part2(input):
    sum = 0
    for line in input:
        sum += calcLine(line, doCalcPart2)
    return sum


if __name__ == '__main__':
    assert calcLine(tInput[0]) == 26
    assert calcLine(tInput[1]) == 437
    assert calcLine(tInput[2]) == 12240
    assert calcLine(tInput[3]) == 13632
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 14208061823964

assert calcLine('1 + (2 * 3) + (4 * (5 + 6))', doCalcPart2) == 51
assert calcLine('2 * 3 + (4 * 5)', doCalcPart2) == 46
assert calcLine('5 + (8 * 3 + 9 + 3 * 4 * 3)', doCalcPart2) == 1445
assert calcLine('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', doCalcPart2) == 669060
assert calcLine('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', doCalcPart2) == 23340

part2_r = part2(rInput)
print(['part2 real', part2_r])
