import operator
import os
from collections import Counter
from functools import reduce

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = complex  # y,x = real, imag

# Adjacent positions -> move direction
moves: list[tuple[set[complex], complex]] = [
    ({-1 - 1j, -1, -1 + 1j}, -1),  # NW, N, NE -> N
    ({1 - 1j, 1, 1 + 1j}, 1),  # SW, S, SE -> S
    ({-1 - 1j, -1j, 1 - 1j}, -1j),  # NW, W, SW -> W
    ({1 + 1j, 1j, -1 + 1j}, 1j),  # NE, E, SE -> E
]

all_adjacent: set[Coord] = reduce(operator.or_, (m[0] for m in moves))


def parse_elves(lines: list[str]) -> set[Coord]:
    return {(y + x * 1j) for y, row in enumerate(lines) for x, char in enumerate(row) if char == '#'}


def get_new_loc(elf: Coord, turn_idx: int, elves: set[Coord]) -> Coord | None:
    if all((elf + c) not in elves for c in all_adjacent):
        # surrounds are empty, no move
        return None

    for i in range(4):
        move_idx = (turn_idx + i) % 4
        adjacent, move = moves[move_idx]

        # if all adjacent coords are free, return the move
        if all((elf + c) not in elves for c in adjacent):
            return elf + move

    # No valid move
    return None


def get_ranges(elves: set[Coord]) -> tuple[range, range]:
    min_y = int(min(elves, key=lambda c: c.real).real)
    max_y = int(max(elves, key=lambda c: c.real).real)

    min_x = int(min(elves, key=lambda c: c.imag).imag)
    max_x = int(max(elves, key=lambda c: c.imag).imag)

    return range(min_y, max_y + 1), range(min_x, max_x + 1)


def draw_elves(elves: set[Coord]):
    ry, rx = get_ranges(elves)

    for y in ry:
        for x in rx:
            print('#' if y + x * 1j in elves else '.', end='')
        print()


def part1(input_path: str = INPUT_PATH) -> int:
    elves: set[Coord] = parse_elves(read_as_lines(input_path))

    for turn_idx in range(10):

        # calculate moves
        elf_moves: dict[Coord, Coord] = {}
        for elf in elves:
            new_loc = get_new_loc(elf, turn_idx, elves)
            if new_loc is not None:
                elf_moves[elf] = new_loc
        destination_counts = Counter(elf_moves.values())
        # remove collisions
        elf_moves = {elf: move for elf, move in elf_moves.items() if destination_counts[move] == 1}

        # update locations
        elves = {elf_moves[elf] if elf in elf_moves else elf for elf in elves}

    ry, rx = get_ranges(elves)
    len_y = ry.stop - ry.start
    len_x = rx.stop - rx.start
    area = len_y * len_x
    return area - len(elves)


def part2(input_path: str = INPUT_PATH) -> int:
    elves: set[Coord] = parse_elves(read_as_lines(input_path))

    turn_idx = 0
    while True:

        # calculate moves
        elf_moves: dict[Coord, Coord] = {}
        for elf in elves:
            new_loc = get_new_loc(elf, turn_idx, elves)
            if new_loc is not None:
                elf_moves[elf] = new_loc
        destination_counts = Counter(elf_moves.values())
        # remove collisions
        elf_moves = {elf: move for elf, move in elf_moves.items() if destination_counts[move] == 1}

        if not elf_moves:
            return turn_idx + 1

        # update locations
        elves = {elf_moves[elf] if elf in elf_moves else elf for elf in elves}

        turn_idx += 1
