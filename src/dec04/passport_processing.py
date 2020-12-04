#!/usr/bin/env python

import os
import re

hcl_pattern = re.compile(r"\#[0-9a-f]{6}")


def check_if_valid(passport: dict, check_constraints: bool = True) -> bool:
    """ Checks if a passport, expressed as a dict, has all required fields:
            byr (Birth Year)
            iyr (Issue Year)
            eyr (Expiration Year)
            hgt (Height)
            hcl (Hair Color)
            ecl (Eye Color)
            pid (Passport ID)
            cid (Country ID)  -- Optional

        If check_constraints, all fields (except cid) must obey some constraints.
            If they do not, the passport is invalid.
    """

    fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    for field in fields:
        if field not in passport:
            return False

    if check_constraints:
        # Check birth year
        if not 1920 <= int(passport['byr']) <= 2002:
            return False

        # Check issue year
        if not 2010 <= int(passport['iyr']) <= 2020:
            return False

        # Check expiration year
        if not 2020 <= int(passport['eyr']) <= 2030:
            return False

        # Check height
        if 'cm' in (hgt := passport['hgt']):
            if not 150 <= int(hgt[:-2]) <= 193:
                return False
        elif 'in' in hgt:
            if not 59 <= int(hgt[:-2]) <= 76:
                return False
        else:
            return False

        # Check hair color
        if not hcl_pattern.match(passport['hcl']):
            return False

        # Check eye color
        if not passport['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            return False

        # Check passport id
        if not len(passport['pid']) == 9:
            return False

    return True


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        passports = file.read()[:-1].split('\n\n')
        passports = [passport.replace('\n', ' ') for passport in passports]
        passports = [{(fs := field.split(':'))[0]: fs[1] for field in passport.split(' ')} for passport in passports]

    # Without constraints
    number_of_valid = sum([check_if_valid(passport, check_constraints=False) for passport in passports])
    print(f"The number of valid passports (without checking constraints) is: {number_of_valid}")

    # With constraints
    number_of_valid = sum([check_if_valid(passport) for passport in passports])
    print(f"The number of valid passports /when checking for constraints) is: {number_of_valid}")
