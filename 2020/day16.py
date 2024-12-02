tInput = open('day16-testinput.txt').read().strip().split('\n\n')
rInput = open('day16-input.txt').read().strip().split('\n\n')


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


def followsRule(n, rule):
    return rule[0][0] <= n <= rule[0][1] or rule[1][0] <= n <= rule[1][1]


def isValid(n, rules):
    for rule in rules:
        if followsRule(n, rule):
            # print('Valid found for rule', rule, 'n', n)
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


def allTicketsComply(rule, okTickets, index):
    ticketValues = [t[index] for t in okTickets]
    # print('ticketValues for index', index, ticketValues)
    return all(map(lambda n: followsRule(n, rule), ticketValues))


def part2(input):
    ruleDict = parseRules(input[0].splitlines())
    rules = ruleDict.values()
    nearbyTickets = input[2].splitlines()[1:]
    print('nearbyTickets', nearbyTickets)
    okTickets = []
    for nt in nearbyTickets:
        print(nt)
        numbers = list(map(int, nt.split(',')))
        if all(map(lambda n: isValid(n, rules), numbers)):
            okTickets.append(numbers)
    print(okTickets)

    myTicket = list(map(int,input[1].splitlines()[1].split(',')))
    indexes = list(range(len(okTickets[0])))
    # Find ticket rule mapping
    # We'll append the index to the rule, so rule[2] == [indexes]
    find_and_add_rule_options(indexes, okTickets, ruleDict)
    solve_rule_options(rules)
    print(ruleDict)
    part2_solution = 1
    for ruleName in ruleDict:
        if ruleName.startswith('departure'):
            ruleIndex = ruleDict[ruleName][2][0]
            part2_solution *= myTicket[ruleIndex]
    print('Part2: ', part2_solution)
    return all([len(r[2]) == 1 for r in rules])


def find_and_add_rule_options(indexes, okTickets, ruleDict):
    for ruleName in ruleDict:
        rule = ruleDict[ruleName]
        rule.append([])
        for index in indexes:
            if allTicketsComply(rule, okTickets, index):
                rule[2].append(index)
        print('rule: ruleName', ruleName, 'rule', 'indexes', rule[2])
        assert len(rule[2]) >= 1


def solve_rule_options(rules):
    remaining = [r for r in rules]
    while len(remaining) > 0:
        certainRules = list(filter(lambda rem: len(rem[2]) <= 1, remaining))
        assert len(certainRules) > 0
        for certain in certainRules:
            assert len(certain[2]) == 1
            remaining.remove(certain)
            for rem in remaining:
                rem[2].remove(certain[2][0])


tInput2 = '''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9'''.split('\n\n')

if __name__ == '__main__':
    part1_t = part1(tInput)
    print(['part1 test', (part1_t)])
    assert part1_t == 71
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part2(tInput2)
    part2_r = part2(rInput)
    # print(['part2 real', part2_r])
