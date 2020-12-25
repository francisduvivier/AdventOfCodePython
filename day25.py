import time

from util import mapl

tInput = open('day25-testinput.txt').read().strip().splitlines()
rInput = open('day25-input.txt').read().strip().splitlines()


def doLoop(subjectNb, loopSize):
    val = 1
    for i in range(loopSize):
        val = (val * subjectNb) % 20201227
    return val


def findLoopSize(subjectNb, publicKey):
    val = 1
    loopSize = 0
    while val != publicKey:
        val = (val * subjectNb) % 20201227
        loopSize += 1
    return loopSize


def part1(input):
    [cardPk, doorPk] = mapl(int, input)
    cardLoopSize = findLoopSize(7, cardPk)
    cardPrivKey = doLoop(doorPk, cardLoopSize)
    doorLoopSize = findLoopSize(7, doorPk)
    doorPrivKey = doLoop(cardPk, doorLoopSize)
    assert cardPrivKey == doorPrivKey
    return cardPrivKey


if __name__ == '__main__':
    assert part1(tInput) == 14897079
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 6421487
    # assert part2(tInput) == 2208
    # part2_r = part2(rInput)
    # print(['part2 real', part2_r])
    # assert part2_r == 4092
