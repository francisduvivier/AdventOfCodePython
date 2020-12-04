import re


def isOk(line: str):
    groups = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line).groups()
    s = int(groups[0])
    e = int(groups[1])
    l = groups[2]
    p = groups[3]
    charList = [char for char in p]
    nbMatches = len(list(filter(lambda letter: letter == l, charList)))
    return s <= nbMatches <= e


def part1():
    input: str = open('input2.txt', 'r').read()
    nbOk = len(list(filter(isOk, input.split('\n'))))
    print('nbOk: ' + str(nbOk))


def isOk2(line: str):
    groups = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line).groups()
    s = int(groups[0])
    e = int(groups[1])
    l = groups[2]
    p = groups[3]
    charList = [char for char in p]

    return (charList[s - 1] == l) + (charList[e - 1] == l) == 1


def part2():
    input: str = open('input2.txt', 'r').read()
    nbOk = len(list(filter(isOk2, input.split('\n'))))
    print('nbOk: ' + str(nbOk))


if __name__ == '__main__':
    print('started\n')
    part1()
    part2()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
