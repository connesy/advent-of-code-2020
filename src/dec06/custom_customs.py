#!/usr/bin/env python

import os


def collect_distinct_answers(group: list) -> int:

    group_answers = group.replace('\n', '')
    distinct_answers = set(group_answers)
    count_answers = len(distinct_answers)

    return count_answers


def count_agreements(group: list) -> int:

    group_answers = group.split('\n')
    if len(group_answers) == 1:
        return len(group_answers[0])

    collected_answers = set()
    for answer in group_answers[0]:
        for answers in group_answers[1:]:
            if answer not in answers:
                break
        else:
            collected_answers.add(answer)

    return len(collected_answers)


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        group_answers = file.read()[:-1].split('\n\n')

    answers = 0
    for group in group_answers:
        answers += collect_distinct_answers(group)

    print(f"The total number of distinct answers: {answers}")

    agreements = 0
    for group in group_answers:
        agreements += count_agreements(group)

    print(f"The total number of agreements: {agreements}")
