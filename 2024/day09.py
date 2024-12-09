import time

from util import map_to_numbers

tInput = open('day09-testinput.txt').read().strip()
rInput = open('day09-input.txt').read().strip()


def parseInput(input):
    filesAndFree = [char for char in input]
    return filesAndFree


def calc_checksum(defragemented):
    return sum([index*number for index, number in enumerate(defragemented)])


def defragment(all_blocks):
    file_blocks = [ block for block in all_blocks if block != '.' ]
    replaced = 0
    for(index, block) in enumerate(all_blocks):
        if block == '.':
            all_blocks[index] = file_blocks.pop()
            replaced +=1
    valid_file_blocks = all_blocks[:-replaced]
    return valid_file_blocks


def part1(input):
    disk_info = parseInput(input)
    all_blocks = []
    for index in range(len(disk_info)):
        nb_blocks = disk_info[index]
        for j in range(int(nb_blocks)):
            if int(index) % 2 == 0:
                file_id = int(index / 2)
                all_blocks.append(file_id)
            else:
                all_blocks.append('.')
    # print(all_blocks)
    defragemented = defragment(all_blocks)
    # print('defragemented',defragemented)
    result = calc_checksum(defragemented)
    print(result)
    return result


assert part1(tInput) == 1928
part1(rInput)
