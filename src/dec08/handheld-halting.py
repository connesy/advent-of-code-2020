#!/usr/bin/env python

import os


def get_instruction(s: str) -> tuple:
    instruction, argument = s.split(' ')
    sign, argument = argument[0], argument[1:]

    if sign == '+':
        argument = int(argument)
    elif sign == '-':
        argument = -int(argument)
    else:
        raise ValueError(f"argument was {sign}{argument}")

    return (instruction, argument)


def check_code(code: list, verbose=True) -> tuple:
    acc = 0
    pos = new_pos = 0
    executed = set()

    while new_pos not in executed:
        pos = new_pos
        if pos == len(code):
            return acc, True

        instruction, argument = get_instruction(code[pos])
        executed.add(pos)

        if verbose:
            print(f"{pos}: {instruction} {argument}")

        if instruction == 'acc':
            acc += argument
            new_pos += 1
        elif instruction == 'jmp':
            new_pos += argument
        elif instruction == 'nop':
            new_pos += 1
        else:
            raise ValueError(instruction)

    return acc, False


def fix_code(code: list) -> tuple:
    for i, line in enumerate(code):
        instruction, argument = get_instruction(line)

        fixed_code = code[:]
        if instruction == 'acc':
            continue
        elif instruction == 'jmp':
            fixed_code[i] = f'nop {fixed_code[i][4:]}'
        elif instruction == 'nop':
            fixed_code[i] = f'jmp {fixed_code[i][4:]}'

        print(f'Trying line {i}: {code[i]} -> {fixed_code[i]} ...')

        accumulator, terminated = check_code(fixed_code, verbose=False)
        if terminated:
            return accumulator, terminated
        else:
            continue


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)

    with open(f'{cwd}/puzzle_input.txt', 'r') as file:
        code = file.read()[:-1].split('\n')

    accumulator, terminated = check_code(code)
    if not terminated:
        print(f"The value in the accumulator immediately before looping was: {accumulator}")

    accumulator, terminated = fix_code(code)
    if terminated:
        print(f"The value in the accumulator immediately after termination was: {accumulator}")
    else:
        print("No fix found")
