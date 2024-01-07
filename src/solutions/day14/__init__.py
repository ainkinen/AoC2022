import os
import re
from collections import Counter
from typing import NamedTuple

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


class Coord(NamedTuple):
    y: int
    x: int


Grid = dict[Coord, str]  # loc -> content


def parse_line(line: str) -> list[Coord]:
    pattern = r'(\d+),(\d+)'
    coord_pairs = re.findall(pattern, line)

    return [Coord(int(pair[1]), int(pair[0])) for pair in coord_pairs]


def parse_grid(lines: list[str]) -> Grid:
    grid: Grid = {}

    for line in lines:
        coords = parse_line(line)

        cur = coords[0]
        for loc in coords[1:]:
            min_y, max_y = sorted((cur.y, loc.y))
            min_x, max_x = sorted((cur.x, loc.x))
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    grid[Coord(y, x)] = '#'
            cur = loc

    return grid


def get_ranges(grid: Grid) -> tuple[range, range]:
    min_y = min(grid.keys(), key=lambda k: k.y).y
    max_y = max(grid.keys(), key=lambda k: k.y).y
    min_x = min(grid.keys(), key=lambda k: k.x).x
    max_x = max(grid.keys(), key=lambda k: k.x).x

    return range(min_y, max_y + 1), range(min_x, max_x + 1)


def draw_grid(grid: Grid):
    print()
    range_y, range_x = get_ranges(grid)
    print(f'bounds: {range_y=} {range_x=}')
    for y in range(range_y.stop):
        for x in range_x:
            print(grid.get(Coord(y, x), '.'), end='')
        print()


def next_loc(grid: Grid, cur_loc: Coord) -> Coord | None:
    deltas = ((1, 0), (1, -1), (1, 1))

    for delta in deltas:
        dy, dx = delta
        new_loc = Coord(cur_loc.y + dy, cur_loc.x + dx)
        if new_loc not in grid:
            return new_loc

    return None


def drop_sand(grid: Grid, max_y: int, is_part2: bool = False) -> Coord | None:
    loc = Coord(0, 500)  # start

    while True:
        if is_part2:
            if loc.y == max_y:
                return loc
        else:
            if loc.y > max_y:
                return None

        if new_loc := next_loc(grid, loc):
            loc = new_loc
        else:
            return loc


def part1(input_path: str = INPUT_PATH) -> int:
    grid = parse_grid(read_as_lines(input_path))
    # draw_grid(grid)
    range_y, _ = get_ranges(grid)

    while new_sand := drop_sand(grid, range_y.stop):
        grid[new_sand] = 'o'

    # draw_grid(grid)
    counter = Counter(grid.values())

    return counter.get('o', 0)


def part2(input_path: str = INPUT_PATH) -> int:
    grid = parse_grid(read_as_lines(input_path))
    # draw_grid(grid)
    range_y, _ = get_ranges(grid)

    while new_sand := drop_sand(grid, range_y.stop, is_part2=True):
        grid[new_sand] = 'o'
        if new_sand == Coord(0, 500):
            break

    # draw_grid(grid)
    counter = Counter(grid.values())

    return counter.get('o', 0)
