import time

rInput = '643719258'
tInput = '389125467'


class MyLN:
    next: "MyLN" = None
    val = 0

    def __init__(self, val):
        self.val = val


class MyLL:
    intToLinks: dict[int, MyLN] = dict()
    prevNode: MyLN = None
    currNode: MyLN = None

    def __init__(self, values):
        lastVal = values[-1]
        veryLastNode = MyLN(lastVal)
        prevNode = veryLastNode
        for val in values:
            newLinkedNode = MyLN(val) if val != lastVal else veryLastNode
            self.intToLinks[val] = newLinkedNode
            prevNode.next = newLinkedNode
            prevNode = newLinkedNode
        self.prevNode = veryLastNode
        self.currNode = veryLastNode.next

    def rotateleft(self):
        self.prevNode = self.currNode
        self.currNode = self.currNode.next

    def insertAfter(self, value, startNode, endNode):
        nodeForValue = self.intToLinks[value]
        oldNext = nodeForValue.next
        nodeForValue.next = startNode
        endNode.next = oldNext

    def popleft(self, amount):
        last = self.prevNode
        unlinkedStart = self.currNode
        for _ in range(amount):
            self.rotateleft()
        self.prevNode.next = None
        self.prevNode = last
        last.next = self.currNode
        return unlinkedStart


def playRounds(startNumbers, rounds):
    LEN = len(startNumbers)
    currNumbers = MyLL(startNumbers)
    lastTime = time.time()
    for i in range(rounds):
        if i % 100_000 == 0:
            print('-- move ' + str(i + 1) + ' --')
            end = time.time()
            diff = (end - lastTime)
            remainingRepeats = ((10_000_000 - i) / 100_000)
            print('100_000 rounds in', round(diff * 1000), 'millis, remaining: ',
                  round(remainingRepeats * diff), 'seconds')
            lastTime = end
            # print('cups: ' + ' '.join(map(str, currNumbers)))

        currNumber = currNumbers.currNode.val
        currNumbers.rotateleft()

        poppedNodeStart = currNumbers.popleft(3)
        poppedValues = toValueList(poppedNodeStart, 3)

        # print('pick up: ' + ' '.join(map(str, poppedNumbers)))

        numberToFind = ((currNumber - 2) % LEN) + 1  # (currNumber -1 -1 % 9) +1
        while numberToFind in poppedValues:
            numberToFind = ((numberToFind - 2) % LEN) + 1

        # print('destination: ' + str(numberToFind))
        currNumbers.insertAfter(numberToFind, poppedNodeStart, poppedNodeStart.next.next)
    rotations = 0
    while currNumbers.currNode.val != 1:
        if (rotations > LEN):
            print(toValueList(currNumbers.currNode, 12))
            raise Exception('problem')
        rotations += 1
        currNumbers.rotateleft()
    return currNumbers


def toValueList(nodeStart, amount):
    result = []
    currNode = nodeStart
    for _ in range(amount):
        result.append(currNode.val)
        currNode = currNode.next

    return result


def part1(input):
    startNumbers = list(map(int, input))
    print('startNumbers', startNumbers)
    result = playRounds(startNumbers, 100)
    assert result.currNode.val == 1
    joined = ''.join(map(str, toValueList(result.currNode.next, len(startNumbers) - 1)))
    print('p1res', joined)
    return joined


def part2(input):
    start = time.time()
    startNumbers = list(map(int, input))
    startNumbers.extend(range(10, 1_000_001))
    print('startNumbers', startNumbers[0], startNumbers[-1])
    myLLResult = playRounds(startNumbers, 10_000_000)
    first = myLLResult.currNode.next
    resultProduct = first.val * first.next.val
    print('p2res', resultProduct)
    end = time.time()
    print('time', (end - start))
    return resultProduct


if __name__ == '__main__':
    assert ''.join(map(str, toValueList(playRounds(list(map(int, tInput)), 10).currNode.next, 8))) == '92658374'
    assert part1(tInput) == '67384529'
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == '54896723'
    assert part2(tInput) == 149245887792
    part2_r = part2(rInput)
    print(['part2 real', part2_r])
    assert part2_r == 146304752384
