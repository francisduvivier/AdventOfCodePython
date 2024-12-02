def part1():
    # input: str = open('day9-tinput.txt', 'r').read().strip()
    input: [str] = list(map(int, open('day9-input.txt', 'r').read().strip().splitlines()))
    i = 0
    for n1 in input[25:]:
        found = False
        for n2 in input[i:i + 25]:
            for n3 in input[i:i + 25]:
                if n2 != n3 and n2 + n3 == n1:
                    found = True
                    break
            if found: break
        if not found: break
        i += 1

    bad = input[i + 25]
    print('Part 1 Result: ' + str((bad)))
    return bad


def part2(sumToFind):
    print('looking for sum ' + str(sumToFind))
    input: [str] = list(map(int, open('day9-input.txt', 'r').read().strip().splitlines()))
    print(len(input))
    for i1, n1 in enumerate(input):
        currSum = n1
        print(['i1', i1, 'n1', n1])
        for i2, n2 in enumerate(input[i1 + 1:]):
            currSum += n2
            # print(['n2', n2, 'cs', currSum])
            if currSum > sumToFind:
                break
            if currSum == sumToFind:
                print(n2)
                all = input[i1: i1 + i2 + 2]
                print(all)
                return max(all) + min(all)


if __name__ == '__main__':
    print('started\n')
    p1result = part1()
    p2result = part2(p1result)
    print('Part2: ' + str(p2result))
