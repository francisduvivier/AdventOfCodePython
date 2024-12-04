import time

import numpy as np
from numpy.ma.extras import row_stack

from util import mapl

tInput = open('day04-testinput.txt').read().strip()
rInput = open('day04-input.txt').read().strip()


def parseInput(input):
    lines = input.splitlines()
    letters = mapl(lambda line: [letter for letter in line], lines)
    return np.array(letters)


def find_horizontal(letterMatrix, word):
    matches = 0
    for i in range(len(letterMatrix)):
        currMatch = ''
        for j in range(len(letterMatrix[i])):
            newLetter = letterMatrix[i][j]
            currMatch += newLetter
            if currMatch not in word:
                currMatch = newLetter
            elif currMatch == word:
                matches += 1
                currMatch = ''
    return matches


def part1(input):
    parsed = parseInput(input)
    matches = find_horizontals(parsed, 'XMAS')
    matches += find_verticals(parsed, 'XMAS')
    matches += find_diagonals(parsed, 'XMAS')
    print(matches)


def find_verticals(parsed, search_string):
    vertical = np.transpose(parsed)
    return find_horizontals(vertical, search_string)


def diagonals(parsed):
    diagonals = []
    diagonals.append(np.diagonal(parsed, 0))

    rows = len(parsed)
    for i in range(1, rows):
        diagonals.append(np.diagonal(parsed, -i))

    cols = len(parsed[0])
    for i in range(1, cols):
        diagonals.append(np.diagonal(parsed, i))
    return diagonals


def find_diagonals(parsed, search_string):
    matches = 0
    matches += find_horizontals(diagonals(parsed), search_string)
    matches += find_horizontals(diagonals(np.fliplr(parsed)), search_string)
    return matches


def find_horizontals(letter_matrix, search_string):
    matches = 0
    matches += find_horizontal(letter_matrix, search_string)
    matches += find_horizontal([np.flip(row) for row in letter_matrix], search_string)
    return matches


part1(tInput)
part1(rInput)


def find_XMAS(parsed):
    matches = 0
    for row in range(len(parsed)):
        for col in range(len(parsed[row])):
            if col + 2 > len(parsed[row]):
                continue
            if row + 2 > len(parsed):
                continue
            slice = parsed[row:row + 3,col:col + 3]
            if find_diagonals(slice, 'MAS') == 2:
                matches += 1
    return matches


def part2(input):
    parsed = parseInput(input)
    matches = find_XMAS(parsed)
    print(matches)


part2(tInput)
part2(rInput)
