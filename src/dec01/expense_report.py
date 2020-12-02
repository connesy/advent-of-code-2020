#!/usr/bin/env python
import os


def process_expense_report(report: list, value: int):
    for i, a in enumerate(report):
        for b in report[i:]:
            if a + b == value:
                return (a, b, a * b)


def process_expense_report_part2(report: list, value: int):
    for i, a in enumerate(report):
        for j, b in enumerate(report[i:]):
            for c in report[j:]:
                if a + b + c == value:
                    return (a, b, c, a * b * c)


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/report.txt', 'r') as file:
        report = [int(value) for value in file.read().split('\n')[:-1]]

    a, b, result = process_expense_report(report, value=2020)
    print(f"{a = }, {b = }, {result = }")

    a, b, c, result = process_expense_report_part2(report, value=2020)
    print(f"{a = }, {b = }, {c = }, {result = }")
