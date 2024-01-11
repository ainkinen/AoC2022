import os
from itertools import product
from typing import NamedTuple

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


class Voxel(NamedTuple):
    y: int
    x: int
    z: int


def parse_voxel(line: str) -> Voxel:
    return Voxel(*map(int, line.split(',')))


def immediate_contacts(v: Voxel) -> set[Voxel]:
    surrounding_deltas = product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1])
    contact_deltas = filter(lambda d: sum(abs(i) for i in d) == 1, surrounding_deltas)

    return {Voxel(v[0] + d[0], d[1] + v[1], d[2] + v[2]) for d in contact_deltas}


def num_free_faces(v: Voxel, all_voxels: set[Voxel]) -> int:
    return sum(1 for c in immediate_contacts(v) if c not in all_voxels)


def part1(input_path: str = INPUT_PATH) -> int:
    all_voxels: set[Voxel] = {parse_voxel(line) for line in read_as_lines(input_path)}
    return sum(num_free_faces(v, all_voxels) for v in all_voxels)


def get_ranges(voxels: set[Voxel]) -> tuple[range, range, range]:  # y, x, z
    min_y = min(voxels, key=lambda v: v.y).y
    max_y = max(voxels, key=lambda v: v.y).y
    min_x = min(voxels, key=lambda v: v.x).x
    max_x = max(voxels, key=lambda v: v.x).x
    min_z = min(voxels, key=lambda v: v.z).z
    max_z = max(voxels, key=lambda v: v.z).z

    return range(min_y, max_y + 1), range(min_x, max_x + 1), range(min_z, max_z + 1)


def map_surrounding_space(voxels: set[Voxel]) -> set[Voxel]:
    ry, rx, rz = get_ranges(voxels)

    start = Voxel(ry.stop, rx.stop, rz.stop)  # guaranteed to be outside the droplet

    queue: list[Voxel] = [start]  # Assumes that the origin is always in the internal space
    visited: set[Voxel] = set()

    def in_extended_range(v: Voxel):
        return (
                ry.start - 1 <= v.y < ry.stop + 1
                and rx.start - 1 <= v.x < rx.stop + 1
                and rz.start - 1 <= v.z < rz.stop + 1
        )

    while queue:
        current_voxel = queue.pop()
        contacts = immediate_contacts(current_voxel)
        empty_contacts = [c for c in contacts if c not in (voxels | visited) and in_extended_range(c)]
        queue.extend(empty_contacts)
        visited.add(current_voxel)

    return visited


def num_external_faces(v: Voxel, surrounding_space: set[Voxel]) -> int:
    return sum(1 for c in immediate_contacts(v) if c in surrounding_space)


def part2(input_path: str = INPUT_PATH) -> int:
    all_voxels: set[Voxel] = {parse_voxel(line) for line in read_as_lines(input_path)}
    surrounding_space: set[Voxel] = map_surrounding_space(all_voxels)

    return sum(num_external_faces(v, surrounding_space) for v in all_voxels)
