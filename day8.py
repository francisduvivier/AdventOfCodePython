import re

from assemblyrunner import runAssembly


def processor1(line: str):
    pass


def part1():
    # input: str = open('day8-tinput.txt', 'r').read().strip()
    input: [str] = open('day8-input.txt', 'r').read().strip()
    result = runAssembly(input)
    print('Part 1 total: ' + str((result)))


def part2():
    # input: str = open('day8-tinput.txt', 'r').read().strip()
    input: str = open('day8-input.txt', 'r').read().strip()
    mutations = []
    for toChange in re.finditer(r'jmp', input):
        mutations.append(input[:toChange.regs[0][0]] + 'nop' + input[toChange.regs[0][1]:])
    for toChange in re.finditer(r'nop', input):
        mutations.append(input[:toChange.regs[0][0]] + 'jmp' + input[toChange.regs[0][1]:])
    for mut in mutations:
        result = runAssembly(mut)
        if 'error' not in str(result):
            print('Part 2 total: ' + str((result)))
            return


if __name__ == '__main__':
    print('started\n')
    # part1()
    part2()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
