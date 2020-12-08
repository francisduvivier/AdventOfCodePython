import re

from assemblyrunner import runAssembly


def processor1(line: str):
    pass


def part1():
    # input: str = open('day8-tinput.txt', 'r').read().strip()
    input: [str] = open('day8-input.txt', 'r').read().strip()
    result = runAssembly(input)
    print('Part 1 total: ' + str((result)))
    return int(result.split(' ')[-1])


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
            return result


if __name__ == '__main__':
    print('started\n')
    assert part1() == 1610
    assert part2() == 1703

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
