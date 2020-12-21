import numpy as np
import math

tInput = open('day20-testinput.txt').read().strip().split('Tile ')[1:]
rInput = open('day20-input.txt').read().strip().split('Tile ')[1:]


def mapl(func, iterable):
    return list(map(func, iterable))


def toKey(row: int, col: int):
    return str(row) + 'rc' + str(col)


def posToKey(pos: [int, int]):
    return toKey(pos[0], pos[1])


def toRowCol(key: str):
    return mapl(int, key.split('rc'))


def mutateMatrix(startMatrix: np.array, flip: bool, rotation: int):
    rotatedCopy = np.rot90(startMatrix, int(rotation / 90))
    return np.flipud(rotatedCopy) if flip else rotatedCopy


assert np.array_equal(np.arange(4).reshape([2, 2]), np.array([[0, 1], [2, 3]]))
assert np.array_equal(mutateMatrix(np.arange(4).reshape([2, 2]), False, 0), np.array([[0, 1], [2, 3]]))
assert np.array_equal(mutateMatrix(np.arange(4).reshape([2, 2]), True, 0), np.array([[2, 3], [0, 1]]))
assert np.array_equal(mutateMatrix(np.arange(4).reshape([2, 2]), False, 90), np.array([[1, 3], [0, 2]]))
assert np.array_equal(mutateMatrix(np.arange(4).reshape([2, 2]), False, 270), np.array([[2, 0], [3, 1]]))
assert np.array_equal(mutateMatrix(np.arange(4).reshape([2, 2]), True, 270), np.array([[3, 1], [2, 0]]))
assert np.array_equal(mutateMatrix(np.arange(4).reshape([2, 2]), True, 180), np.array([[1, 0], [3, 2]]))


def toMatrix(matrixStr: str) -> np.array:
    npArrayInput = mapl(lambda line: [char for char in line], matrixStr.splitlines())
    return np.array(npArrayInput)


assert np.array_equal(toMatrix('#.\n##'), np.array([['#', '.'], ['#', '#']]))
assert not np.array_equal(toMatrix('#.\n##'), np.array([['#', '.'], ['#', '.']]))

Mutation = {'flip': bool, 'rotation': int, 'matrix': np.array}


def getMutations(matrixStr) -> [Mutation]:
    mutations = []
    startMatrix = toMatrix(matrixStr)
    for rotation in [0, 90, 180, 270]:
        for flip in [False, True]:
            mutations.append({'flip': flip, 'rotation': rotation, 'matrix': mutateMatrix(startMatrix, flip, rotation)})

    return mutations


IdMatrixMapVal = {'og': str, 'mutations': list[Mutation]}
IdMutationsMapType = dict[str, IdMatrixMapVal]


def createMatrixMap(input: [str]) -> IdMutationsMapType:
    idMatrixMap: IdMutationsMapType = dict()
    for tileData in input:
        parts = tileData.split(':')
        tileId = parts[0].strip()
        matrix = parts[1].strip()
        mutations = getMutations(matrix)
        idMatrixMap[tileId] = {'og': matrix, 'mutations': mutations}
    return idMatrixMap


def addAdjacents(tilePosKey, newTilesToCheck):
    [row, col] = toRowCol(tilePosKey)
    for rowDiff in [0, 1, -1]:
        for colDiff in [0, 1, -1]:
            if bool(rowDiff) != bool(colDiff):
                newTilesToCheck.append(toKey(row + rowDiff, col + colDiff))


testArr = []
addAdjacents(toKey(0, 0), testArr)
assert np.array_equal(testArr.sort(), ['0rc-1', '0rc1', '-1rc0', '1rc0'].sort())

MatrixVal = {'id': str, 'chosen_mutation': Mutation}


def matchesConnectingSide(mutation, tilePosKey, adjacentPosKey, chosenMutationAdjacent):
    # print('matchesConnectingSide', mutation, tilePosKey, adjacentPosKey, chosenMutationAdjacent)
    newPos = toRowCol(tilePosKey)
    adjacentPos = toRowCol(adjacentPosKey)
    [rowDiff, colDiff] = list(np.array(adjacentPos) - np.array(newPos))
    # print('[rowDiff, colDiff]', [rowDiff, colDiff])
    assert bool(rowDiff) != bool(colDiff)
    adjacentElements = getEdgeElements(chosenMutationAdjacent['matrix'], colDiff, rowDiff)
    mutationElements = getEdgeElements(mutation['matrix'], -colDiff, -rowDiff)
    return np.array_equal(adjacentElements, mutationElements)


def getEdgeElements(matrix, rowDiff, colDiff):
    if rowDiff == 0:
        return matrix[:, colDiff if colDiff == -1 else 0]
    else:
        return matrix[rowDiff if rowDiff == -1 else 0, :]


assert np.array_equal(getEdgeElements(np.array([[1, 2], [3, 4]]), 1, 0), [1, 2])
assert np.array_equal(getEdgeElements(np.array([[1, 2], [3, 4]]), -1, 0), [3, 4])
assert np.array_equal(getEdgeElements(np.array([[1, 2], [3, 4]]), 0, 1), [1, 3])
assert np.array_equal(getEdgeElements(np.array([[1, 2], [3, 4]]), 0, -1), [2, 4])


def getMatchingMutation(tileId: str, tilePosKey: str, matrix: dict[str, MatrixVal],
                        idMutationsMap: IdMutationsMapType):
    startMatrix = idMutationsMap[tileId]
    tilePos = toRowCol(tilePosKey)
    adjacents = []
    addAdjacents(tilePosKey, adjacents)
    for mutation in idMutationsMap[tileId]['mutations']:
        allOk = True
        for adjacentPosKey in adjacents:
            if adjacentPosKey in matrix and not matchesConnectingSide(mutation, tilePosKey, adjacentPosKey,
                                                                      matrix[adjacentPosKey]['chosen_mutation']):
                allOk = False
                break
        if allOk:
            return {'id': tileId, 'chosen_mutation': mutation}
    # print('gMM tilePos', tilePos, 'tilePosKey in matrix', tilePosKey in matrix)
    # print('gMM startMatrix', 'og', startMatrix['og'].replace('\n', '-'), 'muts', len(startMatrix['mutations']))
    return None


def part1(input):
    matrix = arrangeMatrix(input)
    return math.prod(getCorners(matrix))


def arrangeMatrix(input) -> dict[str, MatrixVal]:
    idMatrixMap = createMatrixMap(input)
    matrix: dict[str, MatrixVal] = dict()
    tileIdsRemaining: [str] = list(idMatrixMap.keys())
    firstId = tileIdsRemaining.pop()
    firstPosKey = toKey(0, 0)
    matrix[firstPosKey] = {'id': firstId, 'chosen_mutation': idMatrixMap[firstId]['mutations'][0]}
    tilePosKeysToCheck: [str] = []
    addAdjacents(firstPosKey, tilePosKeysToCheck)
    while len(tileIdsRemaining):
        assert len(tilePosKeysToCheck) > 0
        newTilesToCheck = []
        for tilePosKey in tilePosKeysToCheck[0:]:
            if len(tileIdsRemaining) == 0:
                break
            # print('tilePosKey go', tilePosKey)
            if tilePosKey in matrix:
                # print('tilePosKey rm', tilePosKey)
                tilePosKeysToCheck.remove(tilePosKey)
                continue
            assert len(tileIdsRemaining)
            matchingMutation = None
            for tileId in tileIdsRemaining:
                matchingMutation = getMatchingMutation(tileId, tilePosKey, matrix, idMatrixMap)
                if matchingMutation:
                    matrix[tilePosKey] = matchingMutation
                    if tilePosKey in newTilesToCheck: newTilesToCheck.remove(tilePosKey)
                    addAdjacents(tilePosKey, newTilesToCheck)
                    # print('tilePosKey rm', tilePosKey)
                    tilePosKeysToCheck.remove(tilePosKey)
                    tileIdsRemaining.remove(matchingMutation['id'])
                    break
            # if not matchingMutation:
            #     print("edge possibly found:", tilePosKey)
        # print('tilePosKeysToCheck', tilePosKeysToCheck)
        # assert len(tilePosKeysToCheck) == 0 or len(tileIdsRemaining) == 0
        tilePosKeysToCheck = newTilesToCheck
    assert len(tileIdsRemaining) == 0
    assert len(matrix) == len(idMatrixMap)
    return matrix


def getCorners(matrix: dict[str, MatrixVal]):
    minPos = getMinPos(matrix)
    maxAdd = int(math.sqrt(len(matrix))) - 1
    corners = [[0, 0], [0, maxAdd], [maxAdd, 0], [maxAdd, maxAdd]]
    return mapl(lambda corner: int(matrix[toKey(minPos[0] + corner[0], minPos[1] + corner[1])]['id']), corners)


def getMinPos(matrix: dict[str, MatrixVal]):
    minPos = [0, 0]
    for key in matrix:
        pos = toRowCol(key)
        if pos[0] <= minPos[0] and pos[1] <= minPos[1]:
            minPos = pos
    return minPos


assert np.array_equal(getCorners({'0rc0': {'id': '1'}}), [1] * 4)


def mergeMatrix(matrix: dict[str, MatrixVal]):
    minPos = getMinPos(matrix)
    len1D = int(math.sqrt(len(matrix)))
    all = []
    for row in range(minPos[0], minPos[0] + len1D):
        currRow = []
        for col in range(minPos[1], minPos[1] + len1D):
            newEl: MatrixVal = matrix[toKey(row, col)]
            newMatrix = newEl['chosen_mutation']['matrix']
            assert len(newMatrix) == 10
            print('newMatrix', '\n' + matrixToString(newMatrix), 'newMatrix[...]',
                  '\n' + matrixToString(newMatrix[1:-1, 1:-1]))
            currRow = np.concatenate((currRow, newMatrix[1:-1, 1:-1]), axis=0) if len(currRow) else newMatrix[1:-1,
                                                                                                    1:-1]
        all = np.concatenate((all, currRow), axis=1) if len(all) else currRow

    print('fullMergedMatrix', '\n' + matrixToString(all))
    return all


def matrixToString(matrix: np.array):
    asList = matrix.tolist()
    result = '\n'.join(mapl(''.join, asList))
    # print('matrixToString\n', matrix, '\nresult\n', result, )
    return result


assert matrixToString(np.array([['1', '2'], ['3', '4']])) == '12\n34'

import re
import regex


def part2(input):
    matrix = arrangeMatrix(input)
    mergedMatrix = mergeMatrix(matrix)
    print('len matrix', len(matrix))
    print('shape mergedMatrix', (mergedMatrix.shape))
    monster = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''
    monsterNumber = len(re.findall('#', monster))
    monsterRegexes = createMonsterRegexes(monster, mergedMatrix.shape[0])
    mutatedMatrixStrings = mapl(matrixToString, map(lambda m: m['matrix'], getMutations(matrixToString(mergedMatrix))))
    maxMonsters = 0
    chosenMutation = mutatedMatrixStrings[0]
    for mutatedMatrixString in mutatedMatrixStrings:
        nbMonsters = findMonsters(monsterRegexes, mutatedMatrixString)
        print('mutatedMatrixString', '\n' + mutatedMatrixString)
        if (nbMonsters > maxMonsters):
            chosenMutation = mutatedMatrixString
            maxMonsters = nbMonsters
    print('chosenMutation', chosenMutation)
    print('monsterNumber', monsterNumber)
    print('maxMonsters', maxMonsters)
    roughness = len(re.findall('#', mutatedMatrixString)) - maxMonsters * monsterNumber
    print('roughness', roughness)
    return roughness


def createMonsterRegexes(monster, rowLen):
    allRegexes = []
    monsterRowLen = len(monster.splitlines()[0])
    print('monsterRowLen', monsterRowLen)
    template = 'S' + monster.replace(' ', '.').replace('\n', 'E\nS') + 'E'
    startOptions = rowLen - monsterRowLen
    print('range(startOptions)', list(range(startOptions)))
    for startLen in range(startOptions + 1):
        sR = '.{' + str(startLen) + '}'
        eR = '.{' + str(startOptions - startLen) + '}'
        newTemplate = template.replace('S', sR).replace('E', eR)
        allRegexes.append(newTemplate)
    print('allRegexes', allRegexes)
    return allRegexes


def findMonsters(monsterRegexes, mutatedMatrixString):
    total = 0
    for monsterRegex in monsterRegexes:
        nb = len(regex.findall(monsterRegex, mutatedMatrixString, overlapped=True))
        assert nb == len(re.findall(monsterRegex, mutatedMatrixString))
        total += nb
    return total


if __name__ == '__main__':
    assert part1(tInput) == 20899048083289
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 15670959891893
    assert part2(tInput) == 273
    part2_r = part2(rInput)
    print(['part2 real', part2_r])
