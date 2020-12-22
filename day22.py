from util import mapl

tInput = open('day22-testinput.txt').read().strip()
rInput = open('day22-input.txt').read().strip()
import numpy as np


def parseCards(input):
    [_, p1CardStr, p2CardStr] = input.split(':')
    p1Cards: list[int] = mapl(int, p1CardStr.split('\n\n')[0].strip().splitlines())
    p2Cards: list[int] = mapl(int, p2CardStr.strip().splitlines())
    p1Cards.reverse()
    p2Cards.reverse()
    return p1Cards, p2Cards


def part1(input):
    p1Cards, p2Cards = parseCards(input)
    mostCards = playTillFinishedPart1(p1Cards, p2Cards)
    result = sum([val * (i + 1) for (i, val) in enumerate(mostCards)])
    print('p1res', result)
    return result


def playTillFinishedPart1(p1Cards, p2Cards):
    while len(p1Cards) and len(p2Cards):
        p1Card = p1Cards.pop()
        p2Card = p2Cards.pop()
        if p1Card > p2Card:
            p1Cards.insert(0, p1Card)
            p1Cards.insert(0, p2Card)
        elif p1Card < p2Card:
            p2Cards.insert(0, p2Card)
            p2Cards.insert(0, p1Card)
        else:
            raise Exception('problem')
        pass
    mostCards = p1Cards if len(p1Cards) else p2Cards
    return mostCards


def playTillFinishedPart2(p1Cards, p2Cards):
    while len(p1Cards) and len(p2Cards):
        break
    mostCards = p1Cards if len(p1Cards) > len(p2Cards) else p2Cards
    return mostCards


def part2(input):
    p1Cards, p2Cards = parseCards(input)
    mostCards = playTillFinishedPart2(p1Cards, p2Cards)
    result = sum([val * (i + 1) for (i, val) in enumerate(mostCards)])
    print('p1res', result)
    return result


# print('parseCards(tInput)', parseCards(tInput))
# print('reverses          ', (list(reversed([9, 2, 6, 3, 1])), list(reversed([5, 8, 4, 7, 10]))))
assert np.array_equal(parseCards(tInput), (list(reversed([9, 2, 6, 3, 1])), list(reversed([5, 8, 4, 7, 10]))))
if __name__ == '__main__':
    assert part1(tInput) == 306
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 31308
    assert part2(tInput) == 291
    part2_r = part2(rInput)
    print(['part2 real', part2_r])
