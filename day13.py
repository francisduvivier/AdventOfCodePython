import math

tInput = open('day13-testinput.txt').read().strip().splitlines()
rInput = open('day13-input.txt').read().strip().splitlines()


def part1(input):
    time = int(input[0])
    print(time)
    busNumber = input[1].split(',')
    waitTimes = []
    waitTimesMap = dict()
    for busNumber in busNumber:
        if busNumber == 'x': continue
        busNumber = int(busNumber)
        waitTime = busNumber - (time % busNumber)
        waitTimes.append(waitTime)
        waitTimesMap[waitTime] = busNumber
        print(busNumber, waitTime)
    minWaitTime = min(waitTimes)
    return minWaitTime * waitTimesMap[minWaitTime]

def calcZ(busNumber, y):
    m = 1
    while (True):
        if (y * m) % busNumber == 1:
            return m
        m += 1


def calcTuples(input):
    busNumbers = input.split(',')
    print(busNumbers)
    tuples = []
    for eq, divisor in enumerate(busNumbers):
        if divisor == 'x': continue
        divisor = int(divisor)
        tuple = [divisor - (eq % divisor), divisor]
        tuples.append(tuple)
    return tuples


def part2(input):
    tuples = calcTuples(input)
    return calc_x(tuples)


def calc_x(tuples):
    bigN = 1
    for eq, divisor in tuples:
        bigN *= divisor
    yArray = []
    zArray = []
    aArray = []
    for eq, divisor in tuples:
        y = round(bigN / divisor)
        yArray.append(y)
        zArray.append(calcZ(divisor, y))
        aArray.append(eq)
    print('big', bigN, 'y', yArray, 'z', zArray)
    nbTuples = len(tuples)
    x = 0
    for i in range(nbTuples):
        x += aArray[i] * yArray[i] * zArray[i]
    print(x)
    return x % bigN


if __name__ == '__main__':
    part1_t = part1(tInput)
    print(['part1', (part1_t)])
    assert part1_t == 295
    part1_r = part1(rInput)
    print(['part1', part1_r])
    assert calc_x([[2, 3], [5, 4], [-3, 7]]) == 53
    assert calc_x([[15, 27], [16, 20]]) == 96
    assert part2('17,x,13,19') == 3417
    assert part2('67,7,59,61') == 754018
    assert part2('67,x,7,59,61') == 779210
    assert part2('7,13,x,x,59,x,31,19') == 1068781
    assert part2('67,7,x,59,61') == 1261476
    assert part2('1789,37,47,1889') == 1202161486
    part2_r = part2(rInput[1])
    print(['part2', part2_r])
