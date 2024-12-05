import time

from util import mapl, sub_map_to_numbers

tInput = open('day05-testinput.txt').read().strip()
rInput = open('day05-input.txt').read().strip()


def mapToNumbers(arr):
    return list(map(int, arr))


def parseInput(input):
    [ruleLines, sequences] = input.split('\n\n')
    rules = mapl(lambda line: line.split('|'), ruleLines.splitlines())
    sequences = mapl(lambda line: line.split(','), sequences.splitlines())
    return (rules, sequences)

def create_before_map(rules):
    key_is_before_set_map = {}
    for rule in rules:
        [before, after] = rule
        if before not in key_is_before_set_map:
            key_is_before_set_map[before] = set()
        key_is_before_set_map[before].add(after)
    return key_is_before_set_map

def follows_rules(sequence, rules):
    # print(sequence)
    done_numbers_set = set()
    key_is_before_set_map = create_before_map(rules)
    for el in sequence:
        must_be_after_set = key_is_before_set_map[el] if el in key_is_before_set_map else set()
        broken_rules = must_be_after_set.intersection(done_numbers_set)
        if len(broken_rules)>0:
            return False
        done_numbers_set.add(el)

    return True

def part1(input):
    (rules, sequences) = parseInput(input)

    # print(rules)
    # print(sequences)
    result = 0
    for sequence in sequences:
        if follows_rules(sequence, rules):
            result += int(sequence[int((len(sequence) - 1) / 2)])
    print(result)

part1(tInput)
part1(rInput)
