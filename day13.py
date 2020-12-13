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


if __name__ == '__main__':
    part_t = part1(tInput)
    print(['part1', (part_t)])
    assert part_t == 295
    part1_r = part1(rInput)
    print(['part1', part1_r])
