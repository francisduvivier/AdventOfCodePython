tInput = open('day18-testinput.txt').read().strip().splitlines()
rInput = open('day18-input.txt').read().strip().splitlines()


def calcMapRec(map):
    return 1


import re


def doCalc(subCalc):
    print('doCalc subCalc', subCalc)
    result = subCalc[0]
    for i in range(1, len(subCalc) - 1, 2):
        toEval = str(result) + str(subCalc[i]) + str(subCalc[i + 1])
        print('toEval', toEval)
        result = eval(toEval)
    return result


def calcLine(line):
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
            subCalcResult = doCalc(subCalc)
            deepCalcList.append(subCalcResult)
            pass
        else:
            deepCalcList.append(part)
    print(deepCalcList)
    result = doCalc(deepCalcList)
    print([line, deepCalcList, result])

    return result


def part1(input):
    sum = 0
    for line in input:
        sum += calcLine(line)
    return sum


if __name__ == '__main__':
    # assert calcLine(tInput[0]) == 26
    # assert calcLine(tInput[1]) == 437
    # assert calcLine(tInput[2]) == 12240
    assert calcLine(tInput[3]) == 13632
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    # assert part1_r == 265
    # assert part2(tInput) == 848
    # part2_r = part2(rInput)
    # print(['part2 real', part2_r])
