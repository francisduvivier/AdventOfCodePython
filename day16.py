tInput = open('day16-testinput.txt').read().strip().split('\n\n')
rInput = open('day16-input.txt').read().strip().split('\n\n')
import re


def parseRules(lines):
    rules = dict()
    for line in lines:
        lineParts = line.split(': ')
        name = lineParts[0]
        range1 = list(map(int, lineParts[1].split(' or ')[0].split('-')))
        range2 = list(map(int, lineParts[1].split(' or ')[1].split('-')))
        print(name, range1, range2)
        assert range1[0] <= range1[1]
        assert range2[0] <= range2[1]
        rules[name] = [range1, range2]
    return rules


def isValid(n, rules):
    for rule in rules:
        if rule[0][0] <= n <= rule[0][1] or rule[1][0] <= n <= rule[1][1]:
            print('Valid found for rule', rule, 'n', n)
            return True
    return False


def part1(input):
    ruleDict = parseRules(input[0].splitlines())
    rules = ruleDict.values()
    nearbyTickets = input[2].splitlines()[1:]
    print('nearbyTickets', nearbyTickets)
    errorRate = 0
    for nt in nearbyTickets:
        print(nt)
        numbers = list(map(int, nt.split(',')))
        for n in numbers:
            if not isValid(n, rules):
                errorRate += n
    return errorRate


def part2(input):
    return


if __name__ == '__main__':
    part1_t = part1(tInput)
    print(['part1 test', (part1_t)])
    assert part1_t == 71
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    # part2_r = part2(rInput)
    # print(['part2 real', part2_r])
    # assert part2(tInput) == 175594
