import os

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = tuple[int, int]  # y, x


def move_head(head: Coord, direction: str) -> Coord:
    y, x = head
    if direction == 'U':
        return y - 1, x
    if direction == 'D':
        return y + 1, x
    if direction == 'L':
        return y, x - 1
    if direction == 'R':
        return y, x + 1

    raise ValueError(f'Unknown direction {direction}')


def move_knot(head: Coord, tail: Coord) -> Coord:
    head_y, head_x = head
    tail_y, tail_x = tail
    d_y = tail_y - head_y
    d_x = tail_x - head_x

    if abs(d_y) < 2 and abs(d_x) < 2:
        return tail

    new_y = tail_y - (d_y // abs(d_y) if d_y != 0 else 0)
    new_x = tail_x - (d_x // abs(d_x) if d_x != 0 else 0)

    return new_y, new_x


def printout(snake: list[Coord]):
    dimension = 31
    mid_point = dimension // 2
    grid: list[list[str]] = [['.' for _ in range(dimension)] for _ in range(dimension)]

    grid[mid_point][mid_point] = 's'

    for i, c in reversed(list(enumerate(snake))):
        grid[c[0] + mid_point][c[1] + mid_point] = str(i) if i else 'H'

    rows = [''.join(row) for row in grid]
    output = '\n'.join(rows)
    print('\n' + output)


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    head = tail = (0, 0)
    tail_path: list[Coord] = [tail]

    for line in lines:
        direction, steps = line[0], int(line[2:])

        for i in range(steps):
            head = move_head(head, direction)
            tail = move_knot(head, tail)
            tail_path.append(tail)

    return len(set(tail_path))


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    snake = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), ]
    tail_path: list[Coord] = [snake[-1]]

    for line_i, line in enumerate(lines):
        direction, steps = line[0], int(line[2:])

        for step in range(steps):
            for i, k in enumerate(snake):
                if i == 0:  # head
                    snake[0] = move_head(snake[0], direction)
                    continue
                snake[i] = move_knot(snake[i - 1], snake[i])

            tail_path.append(snake[-1])

    return len(set(tail_path))
