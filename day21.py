tInput = open('day21-testinput.txt').read().strip().splitlines()
rInput = open('day21-input.txt').read().strip().splitlines()
from util import mapl
import numpy as np


def lineToArray(line):
    [ingredients, allergens] = line.split('(contains ')
    ingredients = ingredients.strip().split(' ')
    allergens = allergens.strip()[:-1].split(', ')
    return [ingredients, allergens]


def isSuperset(foodIndexes, allergenIndexes):
    next1 = next((ai for ai in allergenIndexes if ai not in foodIndexes), None)
    return next1 == None


assert not isSuperset([0], [0, 1])
assert isSuperset([1, 2, 3, 4], [1, 3])
assert isSuperset([1, 3], [1, 3])
assert not isSuperset([2, 3, 4], [1, 3])


def part1(input):
    [_, foodMap, okFoods, _] = calcMaps(input)
    print('okFoods', okFoods)
    result = sum(map(lambda food: len(foodMap[food]), okFoods))
    # print('result', result)
    return result


def calcMaps(input):
    parsedInput = mapl(lineToArray, input)
    remainingOkIngredients = np.concatenate(np.array(mapl(lambda tup: tup[0], parsedInput), dtype=object)).tolist()
    print('remainingOkIngredients', remainingOkIngredients)
    allergenMap = dict()
    foodMap = dict()
    for i, food in enumerate(parsedInput):
        for allergen in food[1]:
            if allergen in allergenMap:
                allergenMap[allergen].append(i)
            else:
                allergenMap[allergen] = [i]
        for food in food[0]:
            if food in foodMap:
                foodMap[food].append(i)
            else:
                foodMap[food] = [i]
    okFoods = []
    foodToAllergenMap = dict()
    for food in foodMap:
        foodIndexes = foodMap[food]
        badFood = False
        for allergen in allergenMap:
            if isSuperset(foodIndexes, allergenMap[allergen]):
                badFood = True
                if food in foodToAllergenMap:
                    foodToAllergenMap[food].append(allergen)
                    print('multiple food to allergen mappings found for food', food, 'allergens',
                          foodToAllergenMap[food])
                else:
                    foodToAllergenMap[food] = [allergen]
        if not badFood:
            okFoods.append(food)
    return foodToAllergenMap, foodMap, okFoods, allergenMap


def solveAllergenOptions(foodToAllergenMap):
    remainingFoods = [f for f in foodToAllergenMap]
    while len(remainingFoods) > 0:
        certainFoods = list(filter(lambda rem: len(foodToAllergenMap[rem]) <= 1, remainingFoods))
        assert len(certainFoods) > 0
        for cFood in certainFoods:
            [certainAllergen] = foodToAllergenMap[cFood]
            remainingFoods.remove(cFood)
            for rem in remainingFoods:
                if certainAllergen in foodToAllergenMap[rem]:
                    foodToAllergenMap[rem].remove(certainAllergen)


def part2(input):
    [foodToAllergenMap, foodMap, okFoods, allergenMap] = calcMaps(input)
    assert len(foodToAllergenMap) == len(allergenMap)
    solveAllergenOptions(foodToAllergenMap)

    # print('result', result)
    badFoods = [f for f in foodToAllergenMap]
    badFoods.sort(key=lambda f: foodToAllergenMap[f][0])
    return ','.join(badFoods)


if __name__ == '__main__':
    assert part1(tInput) == 5
    part1_r = part1(rInput)
    print(['part1 real', part1_r])
    assert part1_r == 2282
    assert part2(tInput) == 'mxmxvkd,sqjhc,fvjkl'
    part2_r = part2(rInput)
    print(['part2 real', part2_r])
