#!/usr/bin/env python

import os
import re

# https://regexr.com/5hs27
bag_pattern = re.compile(r"^(?P<first>([a-zA-Z]*\s){2})bags contain\s((?P<bags>(\d\s([a-zA-Z]*\s?){2}bag[s]?(,\s|.))+)|(?P<nobags>no other bags))")


def remove_suffix(string, suffix):
    if string.endswith(suffix):
        return string[:-len(suffix)]
    else:
        return string


def process_rules(rules: str) -> dict:

    rule_dict = {}

    for rule in rules:
        re_match = bag_pattern.match(rule)

        primary_bag = re_match.group('first').rstrip(' ')

        if re_match.group('nobags') is not None:
            rule_dict[primary_bag] = None
        else:
            rule_dict[primary_bag] = {}

            other_bags = re_match.group('bags').split(', ')
            for bag_desc in other_bags:
                n_bags = int(bag_desc[0])
                bag = remove_suffix(remove_suffix(remove_suffix(bag_desc, '.'), 's'), ' bag')[2:]

                rule_dict[primary_bag][bag] = n_bags

    return rule_dict


def find_bags_containing(bag_rules: dict, bag: str) -> set:

    bags_containing = set()

    for bag_color, contains in bag_rules.items():
        if contains is None:
            continue

        if bag in contains:
            bags_containing.add(bag_color)

        bags_containing.update(check_bags(bag_rules, bag_color, bag))

    return bags_containing


def check_bags(bag_rules: dict, bag_color: str, bag: str) -> set:
    bags_containing = set()

    for other_bag, value in bag_rules[bag_color].items():
        if other_bag == bag:
            bags_containing.add(bag_color)
        elif bag_rules[other_bag] is None:
            continue
        else:
            new_bags = check_bags(bag_rules, other_bag, bag)
            if new_bags != set():
                bags_containing.update({bag_color, *new_bags})

    return bags_containing


def count_required_bags(bag_rules: dict, bag: str) -> int:
    required_bags = 1

    for bag_color, value in bag_rules[bag].items():
        if bag_rules[bag_color] is None:
            required_bags += value
        else:
            required_bags += value * count_required_bags(bag_rules, bag_color)

    return required_bags


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        rules = file.read()[:-1].split('\n')

    bag_rules = process_rules(rules)

    my_bag = 'shiny gold'
    bags_containing = find_bags_containing(bag_rules, my_bag)
    print(f"The number of bags that can contain at least one {my_bag} bag is: {len(bags_containing)}")
    print(bags_containing)

    required_bags = count_required_bags(bag_rules, my_bag) - 1
    print(f"The total number of bags contained in one {my_bag} bag is: {required_bags}")
