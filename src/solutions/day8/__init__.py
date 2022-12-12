import os
from itertools import zip_longest, product

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Grid = list[list[int]]


def coords(dimension: int):
    yield from product(range(dimension), range(dimension))


def part1(input_path: str = INPUT_PATH) -> int:
    rows = list(map(lambda s: tuple(map(int, s)), read_as_lines(input_path)))
    columns = list(zip_longest(*rows))

    dimension = len(rows[0])

    visible_trees: set[tuple] = set()

    # visible_trees.update([(0, x) for x in range(dimension)])
    # visible_trees.update([(dimension - 1, x) for x in range(dimension)])
    # visible_trees.update([(y, 0) for y in range(dimension)])
    # visible_trees.update([(y, dimension - 1) for y in range(dimension)])

    for y, x, in coords(dimension):
        left = rows[y][0:x]
        right = rows[y][x + 1:]
        top = columns[x][0:y]
        bottom = columns[x][y + 1:]

        if any([
            all(map(lambda t_len: t_len < rows[y][x], left)),
            all(map(lambda t_len: t_len < rows[y][x], right)),
            all(map(lambda t_len: t_len < rows[y][x], top)),
            all(map(lambda t_len: t_len < rows[y][x], bottom))
        ]):
            visible_trees.add((y, x))

    return len(visible_trees)


def part2(input_path: str = INPUT_PATH) -> int:
    rows: Grid = [[int(char) for char in line] for line in read_as_lines(input_path)]
    columns: Grid = [list(i) for i in zip(*rows)]

    top_score = 0

    for y, x in coords(len(rows)):
        current_tree = rows[y][x]

        up = 0
        up_trees = list(reversed(columns[x][:y]))
        for tree in up_trees:
            up += 1
            if tree >= current_tree:
                break

        left = 0
        left_trees = list(reversed(rows[y][:x]))
        for tree in left_trees:
            left += 1
            if tree >= current_tree:
                break

        right = 0
        right_trees = rows[y][x + 1:]
        for tree in right_trees:
            right += 1
            if tree >= current_tree:
                break

        down = 0
        down_trees = columns[x][y + 1:]
        for tree in down_trees:
            down += 1
            if tree >= current_tree:
                break

        new_score = up * left * right * down
        top_score = max(top_score, new_score)

    return top_score
