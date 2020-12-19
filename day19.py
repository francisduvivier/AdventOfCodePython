import re

tInput = open('day19-testinput.txt').read().strip()
tInput2 = open('day19-testinput2.txt').read().strip()
rInput = open('day19-input.txt').read().strip()

import re


def getRegexRec(rules, ruleString):
    print('resolving rule: ' + ruleString)
    options = []
    if re.fullmatch(r'"[a-zA-Z]"', ruleString):
        return re.search(r'[a-zA-Z]', ruleString)[0]
    elif ruleString.startswith('(?P&'):
        return ruleString
    elif re.fullmatch(r'[0-9]+', ruleString):
        rule = rules[ruleString].split(': ')[1]
        return getRegexRec(rules, rule)
    ruleOptions = ruleString.split(' | ')
    if ruleString.startswith('(?P<'):
        ruleOptions = ruleString.split('>')[1][:-1].split(' | ')
        print('ruleString', ruleString, 'ruleOptions', ruleOptions)
    allOptions = []
    for opt in ruleOptions:
        assert re.fullmatch('[0-9]+( [0-9]+)*', opt) or '(?P&' in opt
        otherRules = opt.split(' ')
        print('otherRules', otherRules)
        optionsRec = ''.join(list(map(lambda r: getRegexRec(rules, r), otherRules)))
        allOptions.append(optionsRec)
    result = '(' + '|'.join(allOptions) + ')'
    if ruleString.startswith('(?P<'):
        result = ruleString.split('>')[0] + '>' + '|'.join(allOptions) + ')'
    return result


import regex


def getValidsOptions(mRegex, strings):
    return list(filter(lambda opt: regex.fullmatch(mRegex, opt), strings))


def parseInputToRulesAndOptions(input: str):
    [rules, opts] = list(map(lambda lines: lines.splitlines(), input.split('\n\n')))
    ruleDict = dict()
    for rule in rules:
        ruleDict[rule.split(': ')[0]] = rule
    return [ruleDict, opts]


def part1(input):
    [rules, strings] = parseInputToRulesAndOptions(input)
    print(rules, strings)
    mRegex = getRegexRec(rules, '0')
    print(mRegex)
    valids = getValidsOptions(mRegex, strings)
    print('valids', valids)
    return len(valids)


def part2(input):
    [rules, strings] = parseInputToRulesAndOptions(input)
    rules['8'] = '8: (?P<acht>42 | 42 (?P&acht))'
    rules['11'] = '11: (?P<elf>42 31 | 42 (?P&elf) 31'
    print(rules, strings)
    mRegex = getRegexRec(rules, '0')
    print(mRegex)
    valids = getValidsOptions(mRegex, strings)
    print('valids', valids)
    return len(valids)


if __name__ == '__main__':
    assert part1(tInput) == 2
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 151
    assert part1(tInput2) == 3
    assert part2(tInput) == 2
    assert part2(tInput2) == 12
    part2_r = part2(rInput)
    print(['part2 real', part2_r])
    assert part2_r == 320536571743074
    mR = r'((?P<acht>((b(a(bb|ab)|b((a|b)(a|b)))|a(b(bb)|a(bb|a(a|b))))b|(((aa|ab)a|(bb)b)b|(((a|b)a|bb)a)a)a)|((b(a(bb|ab)|b((a|b)(a|b)))|a(b(bb)|a(bb|a(a|b))))b|(((aa|ab)a|(bb)b)b|(((a|b)a|bb)a)a)a)(?P&acht))(?P<elf>((b(a(bb|ab)|b((a|b)(a|b)))|a(b(bb)|a(bb|a(a|b))))b|(((aa|ab)a|(bb)b)b|(((a|b)a|bb)a)a)a)(b(b(a(ba)|b(aa))|a(b(ab|(a|b)a)|a(ba|ab)))|a(b((ab|(a|b)a)b|((a|b)a|bb)a)|a((ba)b|(ba|bb)a)))|((b(a(bb|ab)|b((a|b)(a|b)))|a(b(bb)|a(bb|a(a|b))))b|(((aa|ab)a|(bb)b)b|(((a|b)a|bb)a)a)a)(?P&elf)((ab|(a|b)a)b|((a|b)a|bb)a)))'
