import time

from util import mapl

tInput = open('day25-testinput.txt').read().strip().splitlines()
rInput = open('day25-input.txt').read().strip().splitlines()

def part1(input):
    numbers = mapl(int, input)

    return None

if __name__ == '__main__':
    assert part1(tInput) == 14897079
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    # assert part1_r == 411
    # assert part2(tInput) == 2208
    # part2_r = part2(rInput)
    # print(['part2 real', part2_r])
    # assert part2_r == 4092
