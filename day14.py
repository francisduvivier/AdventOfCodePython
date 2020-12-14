import math

tInput = open('day14-testinput.txt').read().strip().splitlines()
rInput = open('day14-input.txt').read().strip().splitlines()

import re


def part1(input):
    lines = input
    maskString = ''
    mem = dict()
    for line in lines:
        if (line.startswith('mask')):
            maskBitString = line[len('mask = '):]
            print(maskBitString)
            maskString = maskBitString
        elif (line.startswith('mem[')):
            [start, end] = line[len('mem['):].split('] = ')
            value = int(end)
            address = int(start)
            zeroMaskString = maskString.replace('X', '1')
            maskZeros = int(zeroMaskString, 2)
            maskedVal = value & maskZeros
            onesMaskString = maskString.replace('X', '0')
            maskOnes = int(onesMaskString, 2)
            maskedVal = maskedVal | maskOnes
            print('v', value, 'addr', address, 'masked', maskedVal, '\nbval:', '{0:b}'.format(value).zfill(36),
                  '\nX=>1:', zeroMaskString, '\nX=>0:', onesMaskString)
            mem[address] = maskedVal

        else:
            raise Exception('bad input: ' + line)

    return sum(mem.values())


if __name__ == '__main__':
    part1_t = part1(tInput)
    print(['part1', (part1_t)])
    assert part1_t == 165
    part1_r = part1(rInput)
    print(['part1', part1_r])
