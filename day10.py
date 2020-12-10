import math

tInput: [str] = list(map(int, open('day10-testinput.txt', 'r').read().strip().splitlines()))
tInput2: [str] = list(map(int, open('day10-testinput2.txt', 'r').read().strip().splitlines()))
rInput: [str] = list(map(int, open('day10-input.txt', 'r').read().strip().splitlines()))


def part1and2(input):
    diffCounts = [0, 0, 0, 0]
    diffs = []
    sInput = sorted(input)
    print(sInput)
    prevN = 0
    builtInAdapter = sInput[-1] + 3
    for amount in sInput + [builtInAdapter]:
        diff = amount - prevN
        diffs.append(diff)
        if not (1 <= diff <= 3):
            print(['bad numbers', prevN, amount])
        diffCounts[diff] += 1
        prevN = amount
    print(diffCounts)
    print(diffs)
    print(diffCounts[1] * (diffCounts[3]))
    print('Part2')
    # print(math.pow(2, diffCounts[1]))
    oneSeq = [0, 0, 0, 0, 0]
    # seqs = []
    currAmount = 0
    for diff in diffs:
        if diff == 3:
            oneSeq[currAmount] += 1
            # seqs.append(currAmount)
            currAmount = 0
        else:
            currAmount += 1

    print(oneSeq)
    total = 1
    for seqSize, amount in enumerate(oneSeq[0:]):
        if amount < 1: continue
        permutable = seqSize - 1  # last i has to stay
        print(['forseqam', total, seqSize, amount])
        total *= math.floor(math.pow(calc_valid_permutations(permutable), amount))
    print(['total', total])


def calc_valid_permutations(permutable):
    print(['pm', permutable])
    if permutable < 1:
        return 1
    elif 1 <= permutable <= 2:
        return math.floor(math.pow(2, permutable))
    elif permutable == 3:
        return math.floor(math.pow(2, permutable)) - 1  # Leaving out all 3 is not fine in that case
    else:
        raise Exception(['invalid input', permutable])


if __name__ == '__main__':
    print('started\n')
    part1and2(rInput)
    # part1and2(tInput2)
