import os
from typing import Iterator

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = tuple[int, int]  # y, x
Grid = dict[Coord, int]
Path = list[Coord]


def height(char: str) -> int:
    if char == 'S':
        char = 'a'

    if char == 'E':
        char = 'z'

    return ord(char) - 97


def find_symbol(symbol: str, lines: list[str]) -> Iterator[Coord]:
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == symbol:
                yield y, x


def shortest_path_length(start: Coord, end: Coord, grid: Grid) -> int | None:
    seen: set[Coord] = {start}
    open_paths: list[Path] = [[start]]

    while open_paths:
        next_paths: list[Path] = []

        for path in open_paths:
            cur_loc = path[-1]
            if cur_loc == end:
                return len(path) - 1  # start not included in length

            cur_height = grid[cur_loc]
            y, x = cur_loc

            moves = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
            for coord in moves:
                if coord not in seen and coord in grid and grid[coord] <= cur_height + 1:
                    # step is valid
                    next_paths.append([*path, coord])
                    seen.add(coord)

        open_paths = next_paths

    return None


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)
    grid: Grid = {(y, x): height(char) for y, line in enumerate(lines) for x, char in enumerate(line)}

    start = next(find_symbol('S', lines))
    end = next(find_symbol('E', lines))

    shortest_path = shortest_path_length(start, end, grid)
    if not shortest_path:
        raise Exception('No path found')

    return shortest_path


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)
    grid: Grid = {(y, x): height(char) for y, line in enumerate(lines) for x, char in enumerate(line)}

    starts = [*find_symbol('S', lines), *find_symbol('a', lines)]
    end = next(find_symbol('E', lines))

    path_lengths = [shortest_path_length(start, end, grid) for start in starts]

    return min(filter(None, path_lengths))
