import re

tInput = open('day19-testinput.txt').read().strip()
rInput = open('day19-input.txt').read().strip()

import re


def getRegexRec(rules, ruleString):
    print('resolving rule: ' + ruleString)
    options = []
    if re.search(r'[a-zA-Z]', ruleString):
        return re.search(r'[a-zA-Z]', ruleString)[0]
    elif re.fullmatch(r'[0-9]+', ruleString):
        rule = rules[int(ruleString)].split(': ')[1]
        return getRegexRec(rules, rule)
    ruleOptions = ruleString.split(' | ')
    allOptions = []
    for opt in ruleOptions:
        print('BAD OPT', opt)
        assert re.fullmatch('[0-9]+( [0-9]+)*', opt)
        otherRules = opt.split(' ')
        print('otherRules', otherRules)
        optionsRec = ''.join(list(map(lambda r: getRegexRec(rules, r), otherRules)))
        allOptions.append(optionsRec)
    return '(' + '|'.join(allOptions) + ')'


import math


# def countOptionsRec(matches):
#     if not isinstance(matches, list):
#         return 1
#     return math.prod(map(countOptionsRec, matches))
def getValidsOptions(regex, strings):
    return list(filter(lambda opt: re.fullmatch(regex, opt), strings))


def parseInputToRulesAndOptions(input: str):
    [rules, opts] = list(map(lambda lines: lines.splitlines(), input.split('\n\n')))
    rules.sort(key=lambda line: int(line.split(': ')[0]))
    return [rules, opts]


def part1(input):
    [rules, strings] = parseInputToRulesAndOptions(input)
    print(rules, strings)
    regex = getRegexRec(rules, '0')
    print(regex)
    valids = getValidsOptions(regex, strings)
    print('valids', valids)
    return len(valids)


if __name__ == '__main__':
    assert part1(tInput) == 2
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    # assert part1_r == 14208061823964
    # part2_r = part2(rInput)
    # print(['part2 real', part2_r])
    # assert part2_r == 320536571743074
