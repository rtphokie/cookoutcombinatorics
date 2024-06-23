import unittest
import yaml
from itertools import product, permutations, combinations


def get_menu(file_path='cookoutmenu.yaml'):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def build_dictionaries(choices):
    result = {}
    for choice in choices:
        for name, calories in choice['calories'].items():
            if name not in result:
                result[name] = {'calories': 0, 'cost': 0}
            result[name]['calories'] += calories
            result[name]['cost'] += choice['cost']
            if 'months' in choice:
                result[name]['available months'] = choice['months']

    return result


def cookout_combinatorics():
    data = get_menu()
    entrees = build_dictionaries(data['entree'].values())
    sides = build_dictionaries([data['side']])
    side_combinations = list(combinations(sides.keys(), r=2))
    side_combinations.extend([(side, side) for side in sides.keys()])
    beverages = build_dictionaries(data['beverage'].values())
    beverages.update(build_dictionaries(data['shake seasonal'].values()))

    total_combinations = len(entrees) * len(side_combinations) * len(beverages)
    total_combinations_with_toppings = (len(entrees) + (5 * 262142)) * len(side_combinations) * len(beverages)

    total_combinations = len(entrees) * len(side_combinations) * len(beverages)
    # 5 sandwiches: small, regular, and big double burgers as well as regular chicken or chicken strip sandwiche0ww:
    total_combinations_with_toppings = (len(entrees) + (5 * 262142)) * len(side_combinations) * len(beverages)
    print(f"entress: {len(entrees):,}")
    print(f"sides: {len(sides):,} for {len(side_combinations):,} combinations")
    print(f"beverages: {len(beverages):,}")
    print(f"total: {total_combinations:,}")
    print(f"total with toppings: {total_combinations_with_toppings:,}")
    return total_combinations, total_combinations_with_toppings


def get_topping_combinations():
    data = get_menu()

    choices = list(data['burger toppings'].keys())
    burger_options = []
    for r in range(1, len(choices) + 1):
        perm = combinations(choices, r=r)
        burger_options += list(perm)

    dog_options = []
    hotdogtoppings = ['ketchup', 'mustard', 'slaw', 'onion', 'chili']
    for r in range(1, len(hotdogtoppings) + 1):
        perm = combinations(hotdogtoppings, r=r)
        dog_options += list(perm)
    return burger_options, dog_options


class MyTestCase(unittest.TestCase):
    def test_topings(self):
        burger_options, dog_options = get_topping_combinations()
        print(f"burger and chicken toppings: {len(burger_options):,}")
        print(f"hot dog toppings: {len(dog_options):,}")

    def test_beverages(self):
        data = get_menu()
        beverages = build_dictionaries(
            [data['beverage'], data['shake'], data['shake seasonal']['winter'], data['shake seasonal']['summer']])
        self.assertEqual(59, len(beverages))

    def test_entrees(self):
        data = get_menu()
        entrees = build_dictionaries([data['entree']['tray'], data['entree']['junior tray']])
        self.assertEqual(20, len(entrees))

    def test_sides(self):
        data = get_menu()
        sides = build_dictionaries([data['side']])
        self.assertEqual(15, len(sides))


if __name__ == '__main__':
    cookout_combinatorics()
