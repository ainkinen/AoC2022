import os

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


def part1(input_path: str = INPUT_PATH) -> int:
    cmds = read_as_lines(input_path)

    x = 1
    cycle = 1
    pc = 0
    next_x: int | None = None

    values: list[int] = []

    while cycle < 221:
        if pc >= len(cmds):
            return x

        op = cmds[pc][:4]
        cmd_value = cmds[pc][5:]

        if cycle in [20, 60, 100, 140, 180, 220]:
            values.append(cycle * x)

        if op == 'noop':
            pc += 1

        if op == 'addx':

            if next_x:
                x, next_x = x + next_x, None
                pc += 1
            else:
                next_x = int(cmd_value)

        cycle += 1

    return sum(values)


def part2(input_path: str = INPUT_PATH) -> str:
    cmds = read_as_lines(input_path)

    x = 1
    cycle = 1
    pc = 0
    next_x: int | None = None

    image = ''

    while pc < len(cmds):

        op = cmds[pc][:4]
        cmd_value = cmds[pc][5:]

        mod = (cycle - 1) % 40
        if mod == 0:
            image += '\n'
        image += '#' if x - 1 <= mod <= x + 1 else '.'

        if op == 'noop':
            pc += 1

        if op == 'addx':

            if next_x:
                x, next_x = x + next_x, None
                pc += 1
            else:
                next_x = int(cmd_value)

        cycle += 1

    return image.strip()
