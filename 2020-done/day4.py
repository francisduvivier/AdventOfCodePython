tocheck = [
    'byr',  # (Birth Year)
    'iyr',  # (Issue Year)
    'eyr',  # (Expiration Year)
    'hgt',  # (Height)
    'hcl',  # (Hair Color)
    'ecl',  # (Eye Color)
    'pid',  # (Passport ID)
    # 'cid',  # (Country ID)
]

import re


def isOkLine(line: str):
    return all(map(lambda tc: re.match(r'.*' + tc + '.*', line), tocheck))


def part1():
    input: str = open('day4-input.txt', 'r').read()
    lines = map(lambda e: e.replace('\n', ' '), input.split('\n\n'))
    lines = filter(isOkLine, lines)
    print('hi ' + str(len(list(lines))))

    # Press the green button in the gutter to run the script.


def goodHeight(val):
    match = re.match('^(\d+)(cm|in)$', val)
    digits = int(match.groups()[0])
    if match.groups()[1] == 'cm':
        return 150 <= digits <= 193  # // the number must be at least 150 and at most 193.
    elif match.groups()[1] == 'in':
        return 59 <= digits <= 76  # // the number must be at least 59 and at most 76.
    return False


rules = {
    'byr': lambda val: re.match('^\d\d\d\d$', val) and int(val) >= 1920 and int(val) <= 2002
    # (Birth Year) four digits; at least 1920 and at most 2002.
    , 'iyr': lambda val: re.match('^\d\d\d\d$', val) and int(val) >= 2010 and int(val) <= 2020
    # (Issue Year) four digits; at least 2010 and at most 2020.
    , 'eyr': lambda val: re.match('^\d\d\d\d$', val) and int(val) >= 2020 and int(val) <= 2030
    # (Expiration Year) four digits; at least 2020 and at most 2030.
    , 'hgt': lambda val: re.match('^(\d+)(cm|in)$', val) and goodHeight(val)
    , 'hcl': lambda val: re.match('^#[0-9a-f]{6}$', val)
    # (Hair Color) a # followed by exactly six characters 0-9 or a-f.
    , 'ecl': lambda val: re.match('^(amb|blu|brn|gry|grn|hzl|oth)$', val)
    # (Eye Color) exactly one of: amb blu brn gry grn hzl oth.
    , 'pid': lambda val: re.match('^\d{9}$', val)  # (Passport ID) a nine-digit number, including leading zeroes.
}


def ruleFollowed(line, tc):
    match = re.match(r'.*' + tc + ':([^ ]+)' + '.*', line)
    if (match and match.groups()):
        return rules[tc](match.groups()[0])
    else:
        return ''


def isOkLine2(line: str):
    return all(map(lambda tc: ruleFollowed(line, tc), tocheck))


def part2():
    input: str = open('day4-input.txt', 'r').read()
    lines = map(lambda e: e.replace('\n', ' '), input.split('\n\n'))
    lines = filter(isOkLine2, lines)
    print('solution: ' + str(len(list(lines))))


if __name__ == '__main__':
    print('started\n')
    part1()
    part2()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
