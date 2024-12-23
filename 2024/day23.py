import time
from functools import cache

import numpy as np

from util import map_to_numbers, sub_map_to_numbers

test_input = open('day23-testinput.txt').read().strip()
real_input = open('day23-input.txt').read().strip()


def parse_input(input):
    lines = input.splitlines()
    pairs = [tuple(line.split('-')) for line in lines]
    return pairs


def create_connections_map(pairs):
    connections_map = {}
    for pair in pairs:
        for pc in pair:
            if pc not in connections_map: connections_map[pc] = []
            connections_map[pc] += [other_pc for other_pc in pair if other_pc != pc]
    return connections_map


def part1(input):
    pairs = parse_input(input)
    connections_map = create_connections_map(pairs)
    triples = set()
    for pc in connections_map:
        connections = connections_map[pc]
        for index, second in enumerate(connections):
            remainder = connections[index + 1:]
            connections_map[second].remove(pc)
            for third in remainder:
                if second in connections_map[third]:
                    new_tuple = tuple(sorted([pc, second, third]))
                    if any([sub for sub in new_tuple if sub[0] == 't']):
                        assert not (new_tuple in triples)
                        triples.add(new_tuple)

    print('triples', len(triples), triples)
    return len(triples)


assert part1(test_input) == 7
part1(real_input)


def find_longest_rec(connecteds, remaining_options, connections_map, longest_pointer):
    if len(remaining_options) + len(connecteds) <= len(longest_pointer[0]):
        return longest_pointer[0]
    if len(remaining_options) == 0:
        longest_pointer[0] = connecteds
        return connecteds
    for index, other in enumerate(remaining_options):
        connected_to_all = set(connections_map[other]).intersection(set(connecteds)) == set(connecteds)
        if connected_to_all:
            find_longest_rec(tuple(list(connecteds) + [other]), remaining_options[index + 1:], connections_map,
                             longest_pointer)
    return longest_pointer[0]


assert find_longest_rec(('A', 'B'), ['C'], {'C': ['A']}, [tuple()]) == tuple()
assert find_longest_rec(('A'), ['B', 'C'], {'C': ['A', 'B'], 'B': ['A', 'C']}, [tuple()]) == ('A', 'B', 'C')
assert find_longest_rec(('A', 'B'), [], {'C': ['A']}, [tuple()]) == ('A', 'B')
assert find_longest_rec(('A', 'B'), ['C'], {'C': ['A', 'B']}, [tuple()]) == ('A', 'B', 'C')
assert (find_longest_rec(('A', 'B'), ['C'], {'C': ['A', 'B']}, [('A', 'B')])
        == ('A', 'B', 'C'))
assert (find_longest_rec(('A', 'B'), ['C'], {'C': ['A', 'B'], }, [('A', 'B', 'D')])
        == ('A', 'B', 'D'))
assert (find_longest_rec(('A', 'B'), ['C', 'D'], {'C': ['A', 'B', 'D'], 'D': ['A', 'B', 'C']}, [('A', 'B', 'D')])
        == ('A', 'B', 'C', 'D'))


def part2(input):
    pairs = parse_input(input)
    connections_map = create_connections_map(pairs)
    longest_pointer = [tuple()]
    for pc in connections_map:
        connections = connections_map[pc]
        find_longest_rec(tuple([pc]), connections, connections_map, longest_pointer)

    result = ','.join(sorted(longest_pointer[0]))
    print('longest', result)
    return result


assert part2(test_input) == 'co,de,ka,ta'
part2(real_input)
