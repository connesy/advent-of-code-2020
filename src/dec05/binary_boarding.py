#!/usr/bin/env python

import os

binary_mapping = str.maketrans({'F': '0', 'B': '1', 'L': '0', 'R': '1'})


def process_boarding_pass(boarding_pass: str) -> tuple:

    binary_boarding_pass = boarding_pass.translate(binary_mapping)

    row_string = binary_boarding_pass[:7]
    col_string = binary_boarding_pass[7:]

    row = int(row_string, 2)
    col = int(col_string, 2)

    seat_id = row * 8 + col

    return (row, col, seat_id)


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        boarding_passes = file.read()[:-1].split('\n')

        seats = [process_boarding_pass(boarding_pass) for boarding_pass in boarding_passes]

        rows, cols, seat_ids = zip(*seats)
        print(max(seat_ids))

        seat_ids = set(seat_ids)
        for seat in range(max(seat_ids)):
            if seat - 1 in seat_ids and seat not in seat_ids and seat + 1 in seat_ids:
                print(f"Should be this seat: {seat}")
