import time

tInput = open('dayxx-testinput.txt').read().strip()
rInput = open('day02-input.txt').read().strip()


def mapToNumbers(arr):
    return list(map(int, arr))


lineToNumbers = lambda line: mapToNumbers(line.split(' '))


def parseInput(input):
    reportLines = input.split('\n')
    reportMatrix = list(map(lineToNumbers, reportLines))
    return reportMatrix


def isSafe(reportLine):
    prevVal = None
    direction = reportLine[0] > reportLine[1]
    for val in reportLine:
        if prevVal == val:
            return False
        if prevVal is not None:
            newDirection = prevVal > val
            if newDirection != direction:
                return False
            if abs(prevVal - val) > 3:
                return False
        prevVal = val
    return True


def part1(input):
    parsed = parseInput(input)
    safeReports = 0
    for reportLine in parsed:
        if isSafe(reportLine):
            safeReports += 1

    print(safeReports)


part1(tInput)
part1(rInput)
