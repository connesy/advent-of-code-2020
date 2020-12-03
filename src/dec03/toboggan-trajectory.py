#!/usr/bin/env python
import os


def get_new_index_from_slope(tree_map: list, row: int, col: int, slope_rows: int, slope_cols: int) -> (int, int):
    """Get the new positional index of the map given a slope to follow expressed as
        number of columns to the right and rows down to move.
    """

    map_length = len(tree_map)
    map_width = len(tree_map[0])

    new_row = row + slope_rows
    new_col = (col + slope_cols) % map_width

    if new_row >= map_length:
        return None, None
    else:
        return new_row, new_col


def count_trees_on_path(tree_map: list, slope_rows: int, slope_cols: int) -> int:
    row, col = 0, 0
    trees = 0

    while row is not None:
        try:
            if tree_map[row][col] == '#':
                trees += 1
        except Exception:
            print(row, col)

        row, col = get_new_index_from_slope(
            tree_map=tree_map, row=row, col=col, slope_rows=slope_rows, slope_cols=slope_cols)

    print(f"Number of trees in path following slope (rows:{slope_rows}, cols:{slope_cols}): {trees}")

    return trees


def check_slopes(tree_map: list):
    slopes = [
        [1, 1],
        [1, 3],
        [1, 5],
        [1, 7],
        [2, 1]
    ]

    result = 1
    for slope in slopes:
        trees = count_trees_on_path(tree_map=tree_map, slope_rows=slope[0], slope_cols=slope[1])
        result *= trees

    print(f"The number of trees multiplied together gives: {result}")


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        tree_map = file.read().split('\n')[:-1]

    check_slopes(tree_map)
