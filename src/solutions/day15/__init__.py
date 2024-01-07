import os
import re
from itertools import combinations, product
from typing import NamedTuple

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


class Coord(NamedTuple):
    y: int
    x: int


Grid = dict[Coord, str]


def parse_sensors(lines: list[str]) -> dict[Coord, Coord]:
    pattern = r'(-?\d+)'
    sensors: dict[Coord, Coord] = {}

    for line in lines:
        numbers = re.findall(pattern, line)
        sensors[Coord(int(numbers[1]), int(numbers[0]))] = Coord(int(numbers[3]), int(numbers[2]))

    return sensors


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


def md(a: Coord, b: Coord) -> int:
    return abs(a.y - b.y) + abs(a.x - b.x)


def part1(input_path: str = INPUT_PATH, row=2_000_000) -> int:
    sensors = parse_sensors(read_as_lines(input_path))

    beacons = set(sensors.values())
    distances: dict[Coord, int] = {sensor: md(sensor, beacon) for sensor, beacon in sensors.items()}

    sensors_in_range = set(sensor for sensor, d in distances.items() if abs(row - sensor.y) <= d)

    min_x = min((sensor.x - d for sensor, d in distances.items() if sensor in sensors_in_range))
    max_x = max((sensor.x + d for sensor, d in distances.items() if sensor in sensors_in_range))

    count = 0

    for x in range(min_x, max_x + 1):
        y = row
        loc = Coord(y, x)

        if loc in beacons:
            continue

        if any(md(sensor, loc) <= distances[sensor] for sensor in sensors_in_range):
            count += 1

    return count


def part2(input_path: str = INPUT_PATH, max_range: int = 4_000_000) -> int:
    sensors = parse_sensors(read_as_lines(input_path))

    distances: dict[Coord, int] = {sensor: md(sensor, beacon) for sensor, beacon in sensors.items()}

    # The only empty spot must be at the edge of two ranges
    # Check intersections of sensor md diamond edges
    a_coeffs: set[int] = set()
    b_coeffs: set[int] = set()

    for ((y, x), r) in distances.items():
        a_coeffs.add(y - x + r + 1)
        a_coeffs.add(y - x - r - 1)
        b_coeffs.add(x + y + r + 1)
        b_coeffs.add(x + y - r - 1)

    for a in a_coeffs:
        for b in b_coeffs:
            loc = Coord((a + b) // 2, (b - a) // 2)
            if all(0 <= axis <= max_range for axis in loc):
                if all(md(loc, sensor) > distances[sensor] for sensor in distances.keys()):
                    return 4_000_000 * loc.x + loc.y

    raise Exception('not found')
