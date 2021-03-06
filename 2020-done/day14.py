import math

tInput2 = '''
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''.strip().splitlines()
tInput = open('day14-testinput.txt').read().strip().splitlines()
rInput = open('day14-input.txt').read().strip().splitlines()


def part1(input):
    lines = input
    maskString = ''
    mem = dict()
    for line in lines:
        if (line.startswith('mask')):
            maskString = line[len('mask = '):]
            print(maskString)
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


import re


def generate_addresses(address, maskString):
    mutatedMaskStrings = generate_mutated_masks(maskString)
    addresses = []
    for maskString in mutatedMaskStrings:
        maskedAddress = mask_address(address, maskString)
        addresses.append(maskedAddress)
    print(addresses)
    return addresses


def mask_address(address, maskString):
    zeroMaskString = maskString.replace('_', '1')
    maskZeros = int(zeroMaskString, 2)
    masked = address & maskZeros
    onesMaskString = maskString.replace('_', '0')
    maskOnes = int(onesMaskString, 2)
    masked = masked | maskOnes
    return masked


def replaceIndex(maskString, xpos, xBit):
    return maskString[:xpos] + xBit + maskString[xpos + 1:]


def mutate_maskString(maskString, xBits, xpostions):
    mutatedMaskString = maskString
    for i, xBit in enumerate(xBits):
        xpos = xpostions[i]
        mutatedMaskString = replaceIndex(mutatedMaskString, xpos, xBit)
    print('maskString, xBits, xpostions, mutatedMaskString:\n', maskString, xBits, xpostions, mutatedMaskString)
    return mutatedMaskString


def generate_mutated_masks(maskString):
    print('generate_mutated_masks', maskString)
    xpostions = []
    for pos in re.finditer('X', maskString):
        xpostions.append(pos.start())
    mutatedMaskStrings = []
    print('xpositions', xpostions)
    for xConfig in range(int(math.pow(2, len(xpostions)))):
        xBits = '{0:b}'.format(xConfig).zfill(len(xpostions))
        mutatedMaskStrings.append(mutate_maskString(maskString, xBits, xpostions))
    print('mutatedMaskStrings', mutatedMaskStrings)
    return mutatedMaskStrings


assert generate_mutated_masks('X0X') == ['000', '001', '100', '101']


def part2(input):
    lines = input
    maskString = ''
    mem = dict()
    for line in lines:
        if (line.startswith('mask')):
            maskString = line[len('mask = '):].replace('0', '_')
            print(maskString)
        elif (line.startswith('mem[')):
            [start, end] = line[len('mem['):].split('] = ')
            value = int(end)
            address = int(start)
            maskedAddresses = generate_addresses(address, maskString)
            print('v', value, 'addr', address, '\nbval:', '{0:b}'.format(value).zfill(36), 'maskedAddresses:\n',
                  maskedAddresses)
            for maskedAddress in maskedAddresses:
                mem[maskedAddress] = value

        else:
            raise Exception('bad input: ' + line)

    return sum(mem.values())


if __name__ == '__main__':
    part1_t = part1(tInput)
    print(['part1', (part1_t)])
    assert part1_t == 165
    part1_r = part1(rInput)
    print(['part1', part1_r])
    part2_t = part2(tInput2)
    print(['part2', (part2_t)])
    assert part2_t == 208
    part2_r = part2(rInput)
    print(['part2', part2_r])
