import re


def processor1(bagLine: str):
    match = re.findall(r'(.+) bags contain', bagLine)
    container = match[0]
    contentMatch = re.findall(r'(\d+ [^.,]+) bags?[.,]', bagLine)
    contents: [str] = contentMatch
    amountMap = dict()
    for content in contents:
        amount = re.findall(r'(\d+) ', content)[0]
        color = content[len(amount) + 1:]
        amountMap[color] = int(amount)
    print(amountMap)
    print(container)
    colorMap[container] = amountMap
    return match


resMap: {str: bool} = dict()
colorMap: {str: [{str: int}]} = dict()


def checkHasPathRec(color: str, currPath=[]):
    print('checking color {' + color + '}, currPath')
    print(currPath)
    # Actual stopcondition
    if color == 'shiny gold':
        return True
    # result caching
    if color in resMap:
        return resMap[color]
    # cycle detection
    if (color in currPath):
        return False
    newCurrPath = currPath.copy()
    newCurrPath.append(color)
    result = any(map(lambda c2: checkHasPathRec(c2, newCurrPath), colorMap[color].keys()))
    resMap[color] = result
    return result


def part1():
    # input: str = open('day7-tinput.txt', 'r').read().strip().splitlines()
    input: str = open('day7-input.txt', 'r').read().strip().splitlines()
    print(input)
    for line in input:
        processor1(line)
    for color in colorMap:
        checkHasPathRec(color)
    total = 0
    for key in resMap:
        if (resMap[key]):
            total += 1
    print('Part 1 total: ' + str(total))


def countColorsRec(color: str):
    print('checking color {' + color + '}')
    # stops when colorMap[color] is empty
    total = 0
    for c2 in colorMap[color].keys():
        print('multiply {' + c2 + '}: ' + str(colorMap[color][c2]))
        subForColor = colorMap[color][c2] * countColorsRec(c2)
        total += subForColor
        print('added ' + c2 + ':  ' + str(subForColor))
    return total + 1


def part2():
    # input: list[str] = open('day7-tinput.txt', 'r').read().strip().splitlines()
    input: str = open('day7-input.txt', 'r').read().strip().splitlines()
    print(input)
    for line in input:
        processor1(line)

    result = countColorsRec('shiny gold')
    print('Part 2 total: ' + str(result - 1))  # -1 for shiny gold itself


if __name__ == '__main__':
    print('started\n')
    # part1()
    part2()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
