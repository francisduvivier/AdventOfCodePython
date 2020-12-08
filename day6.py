import re



def yesLetters(group):
    persons = group.split('\n')
    uniqueLetters = ''
    for person in persons:
        for letter in person:
            if letter not in uniqueLetters:
                uniqueLetters += letter
    return len(uniqueLetters)


def part1():
    # input: str = open('day6-tinput.txt', 'r').read().strip()
    input: str = open('day6-input.txt', 'r').read().strip()
    groups = input.split('\n\n')
    res = sum(map(yesLetters, groups))
    print('part 1: ' + str(res))

def yesLetters2(group):
    persons = group.split('\n')
    filtered: str = persons[0]
    for person in persons[1:]:
        for letter in filtered:
            if letter not in person:
                filtered = filtered.replace(letter, '')
    return len(filtered)

def part2():
    # input: str = open('day6-tinput.txt', 'r').read().strip()
    input: str = open('day6-input.txt', 'r').read().strip()
    groups = input.split('\n\n')
    res = sum(map(yesLetters2, groups))
    print('part2 : ' + str(res))

    return


if __name__ == '__main__':
    print('started\n')
    part1()
    part2()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
