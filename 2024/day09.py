import time

from util import map_to_numbers

tInput = open('day09-testinput.txt').read().strip()
rInput = open('day09-input.txt').read().strip()


def parseInput(input):
    filesAndFree = [char for char in input]
    return filesAndFree


def calc_checksum(defragemented):
    return sum([index * number for (index, number) in enumerate(defragemented) if number != '.'])


def defragment(all_blocks):
    file_blocks = [block for block in all_blocks if block != '.']
    replaced = 0
    for (index, block) in enumerate(all_blocks):
        if block == '.':
            all_blocks[index] = file_blocks.pop()
            replaced += 1
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
assert part1(rInput) == 6216544403458


def get_free_space_size(all_blocks, left_index):
    for index in range(left_index + 1, len(all_blocks)):
        if all_blocks[index] != '.':
            return index - left_index
    return len(all_blocks) - left_index


def find_file(all_blocks, right_index):
    file_id = None
    file_end_index = right_index
    for try_index in range(right_index, -1, -1):
        if all_blocks[try_index] != '.':
            file_id = all_blocks[try_index]
            file_end_index = try_index
            break
    if file_id is None:
        return None, None, None
    file_start_index = 0
    for try_index in range(file_end_index, -1, -1):
        if all_blocks[try_index] != file_id:
            file_start_index = try_index + 1
            break
    file_size = file_end_index - file_start_index + 1
    return file_id, file_start_index, file_size


def find_free(blocks, file_start_index, file_size):
    for try_index in range(file_start_index):
        if blocks[try_index] == '.':
            free_space = get_free_space_size(blocks, try_index)
            if free_space >= file_size:
                return try_index
    return None


def try_place_file(blocks, file_id, file_start_index, file_size):
    new_file_start_index = find_free(blocks, file_start_index, file_size)
    if new_file_start_index is not None:
        blocks[new_file_start_index:new_file_start_index + file_size] = [file_id] * file_size
        blocks[file_start_index:file_start_index + file_size] = ['.'] * file_size


def defragment2(all_blocks):
    defragemented = all_blocks.copy()
    right_index = len(defragemented) - 1
    while True:
        (file_id, file_start_index, file_size) = find_file(defragemented, right_index)
        if file_start_index == 0:
            break
        try_place_file(defragemented, file_id, file_start_index, file_size)
        right_index = file_start_index - 1

    return defragemented


def part2(input):
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
    defragemented = defragment2(all_blocks)
    # print('defragemented',defragemented)
    result = calc_checksum(defragemented)
    print(result)
    return result


assert part2(tInput) == 2858
assert part2(rInput) == 6237075041489
