import math

tInput = open('day13-testinput.txt').read().strip().splitlines()
rInput = open('day13-input.txt').read().strip().splitlines()

def part1(input):
    return


if __name__ == '__main__':
    part_t = part1(tInput)
    print(['part1', (part_t)])
    assert part_t == 295
    part1_r = part1(rInput)
    print(['part1', part1_r])