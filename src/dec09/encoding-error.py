#!/usr/bin/env python

import os
from collections import deque


def find_mismatch(xmas: list, preamble: int = 25) -> tuple:
    running_list = deque(xmas[:preamble])
    mismatch = None
    i = preamble

    while mismatch is None:
        next_number = xmas[i]
        for number in running_list:
            if next_number - number in running_list:
                break
        else:
            mismatch = next_number
            return mismatch, i + 1

        running_list.popleft()
        running_list.append(next_number)
        i += 1


def find_weakness(xmas: list, number: int, min_length: int = 2) -> int:
    running_list = deque(xmas[:min_length])
    i = min_length

    while not (s := sum(running_list)) == number:
        if s < number:
            running_list.append(xmas[i])
            i += 1
        else:
            running_list.popleft()

    return sum([min(running_list), max(running_list)])



if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        contents = file.read()[:-1].split('\n')
    xmas = [int(n) for n in contents]

    mismatch, lineno = find_mismatch(xmas)
    print(f"The first number that isn't a sum of two prior numbers is: {mismatch} on line {lineno}")

    encryption_weakness = find_weakness(xmas, mismatch)
    print(f"The encryption weakness is: {encryption_weakness}")
