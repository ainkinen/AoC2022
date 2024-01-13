import itertools
import os
from collections import Counter

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = complex  # y, x = real, imag
Heading = complex
Winds = set[tuple[Coord, Heading]]

heading_map: dict[str, Heading] = {
    '>': 1j,
    '<': -1j,
    '^': -1,
    'v': 1,
}

moves = set(heading_map.values()) | {0 + 0j}  # all headings & wait


def parse_winds(lines: list[str]) -> Winds:
    winds: Winds = set()

    for y, line in enumerate(lines[1:-1]):
        for x, char in enumerate(line[1:-1]):
            if char in heading_map.keys():
                loc = y + x * 1j
                winds.add((loc, heading_map[char]))

    return winds


def blow(winds: Winds, dim_y: int, dim_x: int) -> Winds:
    new_winds: Winds = set()

    for w, heading in winds:
        new_loc = w + heading
        loc_in_bounds = (new_loc.real % dim_y) + (new_loc.imag % dim_x) * 1j
        new_winds.add((loc_in_bounds, heading))

    return new_winds


def draw_winds(winds: Winds, dim_y: int, dim_x: int, expedition: Coord | None = None):
    head_chars = {value: key for key, value in heading_map.items()}
    counts = Counter(w[0] for w in winds)
    wind_map = {loc: heading for loc, heading in winds}

    print('winds:')
    for y in range(dim_y):
        for x in range(dim_x):
            loc = y + x * 1j
            if loc == expedition:
                print('E', end='')
                continue

            loc_count = counts[loc]
            if loc_count > 1:
                print(loc_count, end='')
            elif loc in wind_map:
                print(head_chars[wind_map[loc]], end='')
            else:
                print('.', end='')
        print()
    print()


def bfs(start: Coord, goal: Coord, winds: Winds, dim_y: int, dim_x: int) -> tuple[int, Winds]:
    locations: set[Coord] = {start}

    def inbound(c: Coord) -> bool:
        return (
                c == start  # start and goal are exceptions outside the wind grid
                or c == goal
                # inside wind grid
                or (0 <= c.real < dim_y and 0 <= c.imag < dim_x)
        )

    for step in itertools.count(1, 1):
        # draw_winds(winds, dim_y, dim_x)

        next_locs: set[Coord] = set()
        next_winds = blow(winds, dim_y, dim_x)
        wind_locations = {w for w, _ in next_winds}

        for loc in locations:
            for move in moves:
                new_loc = loc + move
                if new_loc == goal:
                    return step, next_winds

                if inbound(new_loc) and new_loc not in wind_locations:
                    next_locs.add(new_loc)

        winds = next_winds
        locations = next_locs

    raise Exception('should not reach here')


def part1(input_path: str = INPUT_PATH) -> int:
    lines: list[str] = read_as_lines(input_path)
    dim_y = len(lines) - 2
    dim_x = len(lines[0]) - 2

    start = -1
    goal = dim_y + (dim_x - 1) * 1j

    winds = parse_winds(lines)

    return bfs(start, goal, winds, dim_y, dim_x)[0]


def part2(input_path: str = INPUT_PATH) -> int:
    lines: list[str] = read_as_lines(input_path)
    dim_y = len(lines) - 2
    dim_x = len(lines[0]) - 2

    start = -1
    goal = dim_y + (dim_x - 1) * 1j

    winds = parse_winds(lines)

    there, winds = bfs(start, goal, winds, dim_y, dim_x)

    back, winds = bfs(goal, start, winds, dim_y, dim_x)

    there_again, winds = bfs(start, goal, winds, dim_y, dim_x)

    return there + back + there_again
