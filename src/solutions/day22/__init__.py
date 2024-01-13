import os
import re

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = complex  # y, x = real, imag
Heading = complex
Grid = dict[Coord, str]


def wrap(coord: Coord, heading: Heading, grid: Grid) -> Coord:
    match heading:
        case 1j:
            # >
            row = [c for c in grid.keys() if c.real == coord.real]
            return min(row, key=lambda c: c.imag)
        case -1j:
            # <
            row = [c for c in grid.keys() if c.real == coord.real]
            return max(row, key=lambda c: c.imag)
        case 1:
            # v
            column = [c for c in grid.keys() if c.imag == coord.imag]
            return min(column, key=lambda c: c.real)
        case -1:
            # ^
            column = [c for c in grid.keys() if c.imag == coord.imag]
            return max(column, key=lambda c: c.real)
        case _:
            raise Exception(f'unknown heading {heading}')


def move(coord: Coord, heading: Heading, grid: Grid) -> Coord:
    next_step = coord + heading

    if next_step not in grid:
        # out of bounds, wrap to other side
        next_step = wrap(next_step, heading, grid)

    tile = grid[next_step]
    if tile == '#':
        # cannot move, return the starting point
        return coord

    # valid move, return new loc
    return next_step


def part1(input_path: str = INPUT_PATH) -> int:
    *grid_rows, _, directions_str = read_as_lines(input_path)
    grid: Grid = {(y + x * 1j): c for y, row in enumerate(grid_rows) for x, c in enumerate(row) if c in '.#'}

    heading: Heading = 1j
    loc: Coord = grid_rows[0].index('.') * 1j

    for command in re.split(r'([RL])', directions_str):

        match command:
            # turns
            case 'R':
                heading *= -1j
            case 'L':
                heading *= 1j
            # steps
            case _:
                for i in range(int(command)):
                    new_loc = move(loc, heading, grid)
                    if new_loc == loc:
                        break
                    loc = new_loc

    return int(1000 * (loc.real + 1) + 4 * (loc.imag + 1) + [1j, 1, -1j, -1].index(heading))


def cube_wrap(coord: Coord, heading: Heading) -> tuple[Coord, Heading]:
    x, y = coord.real, coord.imag
    match heading, x // 50, y // 50:
        case 1j, 0, _:
            return complex(149 - x, 99), -1j
        case 1j, 1, _:
            return complex(49, x + 50), -1
        case 1j, 2, _:
            return complex(149 - x, 149), -1j
        case 1j, 3, _:
            return complex(149, x - 100), -1
        case -1j, 0, _:
            return complex(149 - x, 0), 1j
        case -1j, 1, _:
            return complex(100, x - 50), 1
        case -1j, 2, _:
            return complex(149 - x, 50), 1j
        case -1j, 3, _:
            return complex(0, x - 100), 1
        case 1, _, 0:
            return complex(0, y + 100), 1
        case 1, _, 1:
            return complex(100 + y, 49), -1j
        case 1, _, 2:
            return complex(-50 + y, 99), -1j
        case -1, _, 0:
            return complex(50 + y, 50), 1j
        case -1, _, 1:
            return complex(100 + y, 0), 1j
        case -1, _, 2:
            return complex(199, y - 100), -1
        case _:
            raise Exception(f'unexpected wrap {heading, coord}')


def cube_move(coord: Coord, heading: Heading, grid: Grid) -> tuple[Coord, Heading]:
    next_step = coord + heading
    next_heading = heading

    if next_step not in grid:
        # out of bounds, wrap to next cube face
        next_step, next_heading = cube_wrap(next_step, heading)

    tile = grid[next_step]
    if tile == '#':
        # cannot move, return the starting point
        return coord, heading

    # valid move, return new loc
    return next_step, next_heading


def part2(input_path: str = INPUT_PATH) -> int:
    *grid_rows, _, directions_str = read_as_lines(input_path)
    grid: Grid = {(y + x * 1j): c for y, row in enumerate(grid_rows) for x, c in enumerate(row) if c in '.#'}

    heading: Heading = 1j
    loc: Coord = grid_rows[0].index('.') * 1j

    for idx, command in enumerate(re.split(r'([RL])', directions_str)):

        match command:
            # turns
            case 'R':
                heading *= -1j
            case 'L':
                heading *= 1j
            # steps
            case _:
                for i in range(int(command)):
                    new_loc, heading = cube_move(loc, heading, grid)
                    if new_loc == loc:
                        break
                    loc = new_loc

    return int(1000 * (loc.real + 1) + 4 * (loc.imag + 1) + [1j, 1, -1j, -1].index(heading))
