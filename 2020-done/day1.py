def printifOk(n1, n2, n3):
    if (n1 + n2 + n3) == 2020:
        print('solution: ' + str(n1 * n2 * n3))


def part2():
    input: str = open('day1-input.txt', 'r').read()
    numbers = list(map(int, input.split('\n')))
    for n1 in numbers:
        for n2 in numbers:
            for n3 in numbers:
                printifOk(n1, n2, n3)

if __name__ == '__main__':
    print('started\n')
    part2()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
