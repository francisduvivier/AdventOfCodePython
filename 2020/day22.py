import time


tInput = open('day22-testinput.txt').read().strip()
rInput = open('day22-input.txt').read().strip()


def parseCards(input):
    [_, p1CardStr, p2CardStr] = input.split(':')
    p1Cards: list[int] = p1CardStr.split('\n\n')[0].strip().splitlines()
    p2Cards: list[int] = p2CardStr.strip().splitlines()
    p1Cards.reverse()
    p2Cards.reverse()
    return p1Cards, p2Cards


def part1(input):
    p1Cards, p2Cards = parseCards(input)
    mostCards = playTillFinishedPart1(p1Cards, p2Cards)
    result = sum([int(val) * (i + 1) for (i, val) in enumerate(mostCards)])
    print('p1res', result)
    return result


def playTillFinishedPart1(p1Cards, p2Cards):
    while len(p1Cards) and len(p2Cards):
        p1Card = p1Cards.pop()
        p2Card = p2Cards.pop()
        if int(p1Card) > int(p2Card):
            p1Cards.insert(0, p1Card)
            p1Cards.insert(0, p2Card)
        elif int(p1Card) < int(p2Card):
            p2Cards.insert(0, p2Card)
            p2Cards.insert(0, p1Card)
        else:
            raise Exception('problem')
        pass
    mostCards = p1Cards if len(p1Cards) else p2Cards
    return mostCards


def p1WinsRec(p1Card, p1Cards, p2Card, p2Cards, configKey):
    if p1Card > len(p1Cards) or p2Card > len(p2Cards):
        return p1Card > p2Card

    if configKey in solutionCache:
        # print('already seen config,returning cached val:', solutionCache[configKey], len(p1Cards), len(p2Cards))
        return solutionCache[configKey]
    p1Wins, _ = playTillFinishedPart2(p1Cards[-p1Card:], p2Cards[-p2Card:])
    # print('p1Wins rec', p1Wins)
    return p1Wins


def configToKey(p1Cards, p2Cards):
    return ','.join(p1Cards) + ';'.join(p2Cards)


maxRound = 0
solutionCache = dict()


def playTillFinishedPart2(p1Cards, p2Cards):
    global maxRound
    alreadySeenConfigSet = set()
    # print('recursing into', [p1Cards, p2Cards])
    round = 0
    while len(p1Cards) and len(p2Cards):
        round += 1
        if maxRound < round:
            # print('maxRound', round)
            maxRound = round
        # print('Doing round', round)
        # print("Player 1's deck:", list(reversed(p1Cards)))
        # print("Player 2's deck:", list(reversed(p2Cards)))
        newConfigKey = configToKey(p1Cards, p2Cards)
        if newConfigKey in alreadySeenConfigSet:
            # print('already seen config, letting p1 win')
            return True, p1Cards
        alreadySeenConfigSet.add(newConfigKey)
        p1Card = p1Cards.pop()
        p2Card = p2Cards.pop()
        if p1WinsRec(int(p1Card), p1Cards, int(p2Card), p2Cards, newConfigKey):
            solutionCache[newConfigKey] = True
            # print('p1 Wins round', round)
            p1Cards.insert(0, p1Card)
            p1Cards.insert(0, p2Card)
        else:
            solutionCache[newConfigKey] = False
            # print('p2 Wins round', round)
            p2Cards.insert(0, p2Card)
            p2Cards.insert(0, p1Card)
    p1Wins = len(p1Cards) > len(p2Cards)
    mostCards = p1Cards if p1Wins else p2Cards
    return p1Wins, mostCards


def part2(input):
    start = time.time()
    p1Cards, p2Cards = parseCards(input)
    (_, mostCards) = playTillFinishedPart2(p1Cards, p2Cards)
    result = sum([int(val) * (i + 1) for (i, val) in enumerate(mostCards)])
    print('p2res', result)
    end = time.time()
    print('time', (end - start))
    return result


# print('parseCards(tInput)', parseCards(tInput))
# print('reverses          ', (list(reversed([9, 2, 6, 3, 1])), list(reversed([5, 8, 4, 7, 10]))))
# assert np.array_equal(parseCards(tInput), (list(reversed([9, 2, 6, 3, 1])), list(reversed([5, 8, 4, 7, 10]))))
if __name__ == '__main__':
    assert part1(tInput) == 306
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 31308
    # assert part2('Player 1:\n43\n19\n\nPlayer 2:\n2\n29\n14') != None
    assert part2(tInput) == 291
    part2_r = part2(rInput)
    print(['part2 real', part2_r])
    assert part2_r == 33647
