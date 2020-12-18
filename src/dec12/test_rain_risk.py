#!/usr/bin/env python
# flake8: NOQA
from rain_risk import ship_command_mapping, waypoint_command_mapping
import pytest


def init_ship():
    x = y = d = 0
    v = 90
    return (x, y, d, v)


def init_waypoint():
    sx, sy = 5, 2
    wx, wy = 10, 3
    return (sx, sy, wx, wy)


class TestDirectionMapping:

    @pytest.mark.parametrize("command,expected", [
        ("N", (  0,  90,   0)),
        ("S", (  0, -90,   0)),
        ("E", ( 90,   0,   0)),
        ("W", (-90,   0,   0)),
        ("L", (  0,   0,  90)),
        ("R", (  0,   0, 270)),
        ("F", ( 90,   0,   0)),
    ])
    def test_ship_command_once(self, command, expected):
        x, y, d, v = init_ship()
        new_x, new_y, new_d = ship_command_mapping[command](x, y, d, v)
        assert (new_x, new_y, new_d) == expected

    @pytest.mark.parametrize("command1,command2,expected", [
        ("N", "N", (  0, 180,   0)),
        ("N", "S", (  0,   0,   0)),
        ("N", "E", ( 90,  90,   0)),
        ("N", "W", (-90,  90,   0)),
        ("E", "W", (  0,   0,   0)),
        ("S", "W", (-90, -90,   0)),
        ("N", "R", (  0,  90, 270)),
        ("R", "N", (  0,  90, 270)),
        ("S", "L", (  0, -90,  90)),
        ("L", "S", (  0, -90,  90)),
        ("F", "F", (180,   0,   0)),
        ("R", "F", (  0, -90, 270)),
    ])
    def test_ship_commands_twice(self, command1, command2, expected):
        x, y, d, v = init_ship()
        x1, y1, d1 = ship_command_mapping[command1](x, y, d, v)
        x2, y2, d2 = ship_command_mapping[command2](x1, y1, d1, v)
        assert (x2, y2, d2) == expected

    @pytest.mark.parametrize("command,value,expected", [
        ("N",   1, (  5,   2,  10,   4)),
        ("S",   1, (  5,   2,  10,   2)),
        ("E",   1, (  5,   2,  11,   3)),
        ("W",   1, (  5,   2,   9,   3)),
        ("L",  90, (  5,   2,   4,   7)),
        ("L", 180, (  5,   2,   0,   1)),
        ("L", 270, (  5,   2,   6,  -3)),
        ("R",  90, (  5,   2,   6,  -3)),
        ("R", 180, (  5,   2,   0,   1)),
        ("R", 270, (  5,   2,   4,   7)),
        ("F",   1, ( 10,   3,  15,   4)),
        ("F",   2, ( 15,   4,  20,   5)),
    ])
    def test_waypoint_command_once(self, command, value, expected):
        sx, sy, wx, wy = init_waypoint()
        new_sx, new_sy, new_wx, new_wy = waypoint_command_mapping[command](sx, sy, wx, wy, value)
        assert (new_sx, new_sy, new_wx, new_wy) == expected
