#!/usr/bin/env python
import os
import re
re_groups = re.compile(r"(?P<values>\d+\-\d+)\s(?P<letter>\w)\s*:\s*(?P<password>\w+)")


def analyse_password_policy(password_policy: str) -> bool:
    """
    Expects a password policy string in the form "1-3 b: arfts".
    The password policy indicates the lowest and highest number of times a given letter must appear for the password
    to be valid. For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.
    """
    result = re_groups.match(password_policy)

    try:
        counts = result.group('values')
        letter = result.group('letter')
        password = result.group('password')
    except Exception as exc:
        print(password_policy)
        raise exc

    counts_min, counts_max = counts.split('-')

    if int(counts_min) <= password.count(letter) <= int(counts_max):
        return True
    else:
        return False


def analyse_password_policy_new_rules(password_policy: str) -> bool:
    """
    Expects a password policy string in the form "1-3 b: arfts".
    Each policy describes two positions in the password, where 1 means the first character, 2 means the second
    character, and so on (not zero-indexing). Exactly one of these positions must contain the given letter.
    Other occurrences of the letter are irrelevant for the purposes of policy enforcement.
    """
    result = re_groups.match(password_policy)

    try:
        positions = result.group('values')
        letter = result.group('letter')
        password = result.group('password')
    except Exception as exc:
        print(password_policy)
        raise exc

    position1, position2 = positions.split('-')
    position1 = int(position1) - 1
    position2 = int(position2) - 1

    if bool(password[position1] == letter) != bool(password[position2] == letter):
        return True
    else:
        return False


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    valid_passwords_old_rules = []
    valid_passwords_new_rules = []
    with open(f'{cwd}/passwords.txt', 'r') as file:
        while (password_policy := file.readline().strip('\n')):
            valid_old = analyse_password_policy(password_policy)
            if valid_old:
                valid_passwords_old_rules.append(password_policy)

            valid_new = analyse_password_policy_new_rules(password_policy)
            if valid_new:
                valid_passwords_new_rules.append(password_policy)

    print(f"Number of valid passwords, old rules: {len(valid_passwords_old_rules)}")
    print(f"Number of valid passwords, new rules: {len(valid_passwords_new_rules)}")
