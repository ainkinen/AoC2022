import os
from copy import deepcopy
from math import floor

from src.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = tuple[int, int]  # y, x

Grid = list[list[str]]  # 3d grid

rocks = '-+>Io'


def rock_coords(kind: str, max_y: int) -> set[Coord]:
    coords: set[Coord]
    match kind:
        case '-':
            coords = {(0, 2), (0, 3), (0, 4), (0, 5)}
        case '+':
            coords = {(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)}
        case '>':
            coords = {(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)}
        case 'I':
            coords = {(0, 2), (1, 2), (2, 2), (3, 2)}
        case 'o':
            coords = {(0, 2), (0, 3), (1, 2), (1, 3)}
        case _:
            raise Exception(f'unknown rock type {kind}')

    return {(c[0] + max_y + 3, c[1]) for c in coords}


def shift_sideways(rock: set[Coord], grid: Grid, direction: str) -> set[Coord]:
    new_coords: set[Coord]
    match direction:
        case '<':
            new_coords = {(c[0], c[1] - 1) for c in rock}
        case '>':
            new_coords = {(c[0], c[1] + 1) for c in rock}
        case _:
            raise Exception(f'unknown direction {direction}')

    below_floor = (c[0] < 0 for c in new_coords)
    out_of_bounds = (c[1] < 0 or c[1] > 6 for c in new_coords)
    collision = (grid[c[0]][c[1]] != '.' for c in new_coords if c[0] < len(grid))

    if any(below_floor) or any(out_of_bounds) or any(collision):
        # can't move, return old coords
        return rock

    return new_coords


def sift_down(rock: set[Coord], grid: Grid):
    new_coords = {(c[0] - 1, c[1]) for c in rock}

    below_floor = (c[0] < 0 for c in new_coords)
    collision = (grid[c[0]][c[1]] != '.' for c in new_coords if c[0] < len(grid))

    if any(below_floor) or any(collision):
        # can't move
        return None

    return new_coords


def get_height(grid: Grid) -> int:
    num_empty_lines = 0
    for i, row in enumerate(reversed(grid)):
        if not all(c == '.' for c in row):
            num_empty_lines = i
            break

    return len(grid) - num_empty_lines


def print_grid(grid: Grid, rock: set[Coord] | None):
    grid_copy = deepcopy(grid)
    if rock:
        for (y, x) in rock:
            while y > len(grid_copy) - 1:
                grid_copy.append(['.'] * 7)
            grid_copy[y][x] = '@'

    for row in reversed(grid_copy):
        print('|' + ''.join(row) + '|')
    print('*-------*\n')


def part1(input_path: str = INPUT_PATH) -> int:
    num_rocks_wanted = 2022
    directions = read_as_string(input_path).strip()

    grid: Grid = []

    dir_idx = 0
    rock_count = 0
    cur_rock: set[Coord] | None = None
    while True:
        dir_mod = dir_idx % len(directions)
        rock_mod = rock_count % len(rocks)
        max_y = get_height(grid)

        if not cur_rock:
            if rock_count == num_rocks_wanted:
                break
            else:
                cur_rock = rock_coords(rocks[rock_mod], max_y)
                rock_count += 1

        # sideways
        cur_rock, dir_idx = shift_sideways(cur_rock, grid, directions[dir_mod]), dir_idx + 1

        # down
        if new_coords := sift_down(cur_rock, grid):
            cur_rock = new_coords
        else:
            for (y, x) in cur_rock:
                while y > len(grid) - 1:
                    grid.append(['.'] * 7)
                grid[y][x] = '#'
            cur_rock = None

    return get_height(grid)


def snapshot(grid: Grid) -> str:
    h = get_height(grid)

    return ''.join(''.join(row) for row in grid[h - 20:h])


def part2(input_path: str = INPUT_PATH) -> int:
    num_rocks_wanted = 1000000000000
    directions = read_as_string(input_path).strip()

    grid: Grid = []

    dir_idx = 0
    rock_count = 0
    cur_rock: set[Coord] | None = None

    heights: list[int] = []
    snapshots: list[tuple[int, int, str]] = []  # dir_mod, rock_mod, last rows
    loop_start = 0
    loop_length = 0

    while True:
        dir_mod = dir_idx % len(directions)
        rock_mod = rock_count % len(rocks)
        max_y = get_height(grid)

        if not cur_rock:
            if rock_count >= 5000:
                # Hopefully a loop is found before this
                break
            else:
                heights.append(get_height(grid))
                snap = (dir_mod, rock_mod, snapshot(grid))
                if snap in snapshots:
                    loop_start = snapshots.index(snap)
                    loop_length = rock_count - loop_start
                    break
                snapshots.append(snap)

                cur_rock = rock_coords(rocks[rock_count % len(rocks)], max_y)
                rock_count += 1

        # sideways
        cur_rock, dir_idx = shift_sideways(cur_rock, grid, directions[dir_mod]), dir_idx + 1

        # down
        if new_coords := sift_down(cur_rock, grid):
            cur_rock = new_coords
        else:
            for (y, x) in cur_rock:
                while y > len(grid) - 1:
                    grid.append(['.'] * 7)
                grid[y][x] = '#'
            cur_rock = None

    loop_height = heights[loop_start + loop_length] - heights[loop_start]

    full_repeats_needed = floor((num_rocks_wanted - loop_start) / loop_length)
    idx_after_repeats = loop_start + full_repeats_needed * loop_length
    extra_steps = num_rocks_wanted - idx_after_repeats
    extra_steps_length = heights[loop_start + extra_steps] - heights[loop_start]

    return heights[loop_start] + full_repeats_needed * loop_height + extra_steps_length
