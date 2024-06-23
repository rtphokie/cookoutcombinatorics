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
    beverages_summer = build_dictionaries([data['beverage'], data['shake'], data['shake seasonal']['summer']])
    beverages_winter = build_dictionaries( [data['beverage'], data['shake'], data['shake seasonal']['winter']])
    beverages = build_dictionaries( [data['beverage'], data['shake']])

    burger_options, dog_options = get_topping_combinations()


    total_combinations = len(entrees) * len(side_combinations) * len(beverages)
    total_combinations_summer = len(entrees) * len(side_combinations) * len(beverages_summer)
    total_combinations_winter = len(entrees) * len(side_combinations) * len(beverages_winter)
    # 6 sandwiches: small, regular, and big double burgers as well as regular, spicy and chicken strip sandwiche0ww:
    total_combinations_with_toppings = (len(entrees)-1 + (6 * len(burger_options))  + (2*len(dog_options))) * len(side_combinations) * len(beverages)
    # removing 1 from the entrees for the cajun chicken sandwich with is effetively created as one of the topping combinations.
    # keeping all other entreees to serve as plain options.
    print(f"entress: {len(entrees):,}")
    print(f"sides: {len(sides):,} for {len(side_combinations):,} combinations")
    print(f"beverages: {len(beverages):,}")
    print(f"total: {total_combinations:,}")
    print(f"total summer: {total_combinations_summer:,}")
    print(f"total winter: {total_combinations_winter:,}")

    print()
    print(f"burger toppings: {len(burger_options):,}")
    print(f"dog toppings: {len(dog_options):,}")
    print(f"total with toppings: {total_combinations_with_toppings:,}")

    orders={}
    for entree in entrees.keys():
        for side in side_combinations:
            for beverage in beverages.keys():
                calories=entrees[entree]['calories']+sides[side[0]]['calories']+sides[side[1]]['calories']+beverages[beverage]['calories']
                if side[0] == side[1]:
                    order = f"{entree}, double up {side[0]}, and a {beverage} ({calories} calories)"
                else:
                    order = f"{entree}, with {side[0]} and {side[1]}, and a {beverage} ({calories} calories)"
                orders[order]=calories
    with open('order_combinations.text', 'w') as outfile:
        outfile.write("\n".join(orders.keys()))
    highest_calories = max(orders.values())
    lowest_calories = min(orders.values())
    highest_calorie_orders = [key for key in orders if orders[key] ==highest_calories]
    lowest_calorie_orders = [key for key in orders if orders[key] ==lowest_calories]
    print(f"highest calorie orders ({highest_calories} calories):\n -")
    print("\n -".join(highest_calorie_orders))
    print(f"lowest calorie orders ({lowest_calories} calories):\n -")
    print("\n -".join(lowest_calorie_orders))

    return total_combinations, total_combinations_with_toppings



def get_topping_combinations():
    """
    Returns all possible combinations of burger toppings and hot dog toppings.
    From just a single topping to all possible toppings.  Note: plain is not included here

    Returns:
        burger_options (list): A list of all possible combinations of burger and chicken sandwich toppings
        dog_options (list): A list of all possible combinations of hot dog toppings.
    """
    data = get_menu()

    choices = list(data['burger toppings'].keys())
    burger_options = []
    for r in range(1, len(choices) + 1):
        perm = combinations(choices, r=r)
        burger_options += list(perm)

    dog_options = []
    hotdogtoppings = list(data['dog toppings'].keys())
    for r in range(1, len(hotdogtoppings) + 1):
        perm = combinations(hotdogtoppings, r=r)
        dog_options += list(perm)
    return burger_options, dog_options


class MyTestCase(unittest.TestCase):
    def test_topings(self):
        burger_options, dog_options = get_topping_combinations()
        # print(f"burger and chicken toppings: {len(burger_options):,}")
        # print(f"hot dog toppings: {len(dog_options):,}")
        self.assertEqual(262143, len(burger_options))
        self.assertEqual(3, len(dog_options))

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
        self.assertEqual(16, len(sides))

    def test_main(self):
        cookout_combinatorics()

if __name__ == '__main__':
    cookout_combinatorics()
