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


def part2(input, startNb=1):
    busNumbers = input.split(',')
    print(busNumbers)
    multiplier = math.floor(startNb / int(busNumbers[0])) + 1
    tuples = []
    for index, busNumber in enumerate(busNumbers[1:]):
        if busNumber == 'x': continue
        tuples.append([index, int(busNumber)])
    while True:
        startTime = int(busNumbers[0]) * multiplier
        # print(busNumbers[0], startTime, multiplier)
        ok = True
        for index, busNumber in tuples:
            if ((startTime + index + 1) % busNumber) != 0:
                ok = False
                break
        if ok:
            print(startTime)
            return startTime
        multiplier += 1
    return


if __name__ == '__main__':
    # part1_t = part1(tInput)
    # print(['part1', (part1_t)])
    # assert part1_t == 295
    # part1_r = part1(rInput)
    # print(['part1', part1_r])
    assert part2('7,13,x,x,59,x,31,19') == 1068781
    assert part2('17,x,13,19') == 3417
    assert part2('67,7,59,61') == 754018
    assert part2('67,x,7,59,61') == 779210
    assert part2('67,7,x,59,61', 1061476) == 1261476
    assert part2('1789,37,47,1889', 1002161486) == 1202161486
    part2_r = part2(rInput[1], 100000000000000)
    print(['part2', part2_r])
