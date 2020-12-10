#!/usr/bin/env python

import os
from functools import lru_cache


def find_differences(adapters: list) -> tuple:
    differences = {1: 0, 2: 0, 3: 0}

    for i, _ in enumerate(adapters[:-1]):
        diff = adapters[i + 1] - adapters[i]
        differences[diff] += 1

    return differences


def build_dict(adapters: list) -> dict:
    d = {}
    for i, adapter in enumerate(adapters):
        d[adapter] = [a for a in adapters[i:] if adapter + 3 >= a > adapter]

    return d


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        adapters = file.read()[:-1].split('\n')

    adapters = list(sorted([int(adapter) for adapter in adapters]))
    adapters = [0, *adapters, max(adapters) + 3]  # Add starting and end points to list

    differences = find_differences(adapters)

    print(f"Differences: {differences}")
    print(f"Number of 1-jolt differences multiplied by number of 3-jolt differences: {differences[1] * differences[3]}")

    # Build dictionary containing a list of possible next adapters for each adapter value
    possibilities = build_dict(adapters)

    # Define function inline to avoid having to pass in possibilities dict every time, as that cannot be cached
    @lru_cache(maxsize=None)
    def count_arangements(starting_value: int) -> int:
        """ Count the number of arangements when starting from starting_value """

        if len(possibilities[starting_value]) == 0:
            return 1

        arangements = 0  # One way of selecting the starting starting_value
        for next_value in possibilities[starting_value]:
            arangements += count_arangements(starting_value=next_value)

        return arangements

    arangements = count_arangements(starting_value=0)

    print(f"The total number of arangements are: {arangements}")
