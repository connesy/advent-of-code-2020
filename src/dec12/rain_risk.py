#!/usr/bin/env python

import os
from math import cos, sin, radians


ship_command_mapping = {
    'N': lambda x, y, d, v: (x, y + v, d),
    'S': lambda x, y, d, v: (x, y - v, d),
    'E': lambda x, y, d, v: (x + v, y, d),
    'W': lambda x, y, d, v: (x - v, y, d),
    'L': lambda x, y, d, v: (x, y, (d + v) % 360),
    'R': lambda x, y, d, v: (x, y, (d - v) % 360),
    'F': lambda x, y, d, v: (x + int(cos(radians(d)) * v), y + int(sin(radians(d)) * v), d),
}


def waypoint_left(sx, sy, wx, wy, v):
    if v == 90:
        wx, wy = sx - (wy - sy), sy + (wx - sx)

    elif v == 180:
        sx, sy, wx, wy = waypoint_left(sx, sy, wx, wy, 90)
        sx, sy, wx, wy = waypoint_left(sx, sy, wx, wy, 90)

    elif v == 270:
        sx, sy, wx, wy = waypoint_right(sx, sy, wx, wy, 90)

    return sx, sy, wx, wy


def waypoint_right(sx, sy, wx, wy, v):
    if v == 90:
        wx, wy = sx + (wy - sy), sy - (wx - sx)

    elif v == 180:
        sx, sy, wx, wy = waypoint_right(sx, sy, wx, wy, 90)
        sx, sy, wx, wy = waypoint_right(sx, sy, wx, wy, 90)

    elif v == 270:
        sx, sy, wx, wy = waypoint_left(sx, sy, wx, wy, 90)

    return sx, sy, wx, wy


def waypoint_forward(sx, sy, wx, wy, v):
    x_diff = wx - sx
    y_diff = wy - sy
    new_sx = sx + v * x_diff
    new_sy = sy + v * y_diff
    new_wx = wx + v * x_diff
    new_wy = wy + v * y_diff
    return new_sx, new_sy, new_wx, new_wy


waypoint_command_mapping = {
    'N': lambda sx, sy, wx, wy, v: (sx, sy, wx, wy + v),
    'S': lambda sx, sy, wx, wy, v: (sx, sy, wx, wy - v),
    'E': lambda sx, sy, wx, wy, v: (sx, sy, wx + v, wy),
    'W': lambda sx, sy, wx, wy, v: (sx, sy, wx - v, wy),
    'L': waypoint_left,
    'R': waypoint_right,
    'F': waypoint_forward,
}


def travel(directions, verbose=False):
    """ Moves the ship according to the given directions using the specified command mapping"""

    x, y, d = 0, 0, 0

    for direction in directions:
        command, value = direction[0], int(direction[1:])
        x, y, d = ship_command_mapping[command](x, y, d, value)

        if verbose:
            print(f"Moving ship {command}{value} - Ship now at ({x=}; {y=} facing {d=} degrees")

    return x, y, d


def travel_waypoint(directions, init_wx, init_wy, verbose=False):
    """ Moves the ship according to the given directions using the specified command mapping"""

    sx, sy = 0, 0
    wx, wy = init_wx, init_wy

    for direction in directions:
        command, value = direction[0], int(direction[1:])
        sx, sy, wx, wy = waypoint_command_mapping[command](sx, sy, wx, wy, value)

        if verbose:
            print(f"Moving ship {command}{value} - Ship now at ({sx=}; {sy=}) and waypoint at ({wx=}; {wy=})")

    return sx, sy, wx, wy


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        directions = file.read().splitlines()

    final_x, final_y, final_d = travel(directions)
    manhattan_dist = abs(final_x) + abs(final_y)
    print(f"The final position was ( {final_x=} ; {final_y=} ) and facing in the direction {final_d} degrees.")
    print(f"The Manhattan distance from (0;0) to here is: {manhattan_dist}")

    final_sx, final_sy, final_wx, final_wy = travel_waypoint(directions, init_wx=10, init_wy=1, verbose=True)
    manhattan_dist = abs(final_sx) + abs(final_sy)
    print(f"The final position was ( {final_sx=} ; {final_sy=} ).")
    print(f"The Manhattan distance from (0;0) to here is: {manhattan_dist}")
