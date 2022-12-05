import os

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_sets(in_str: str) -> tuple[set[int], set[int]]:
    str1, str2 = in_str.split(',')
    s1, e1 = str1.split('-')
    s2, e2 = str2.split('-')

    r1 = range(int(s1), int(e1) + 1)
    r2 = range(int(s2), int(e2) + 1)

    return set(r1), set(r2)


def total_overlap(sets: tuple[set, set]) -> bool:
    s1, s2 = sets

    union = s1.union(s2)

    return s1 == union or s2 == union


def any_overlap(sets: tuple[set, set]) -> bool:
    s1, s2 = sets

    intersection = s1.intersection(s2)

    return bool(len(intersection))


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    sets = map(parse_sets, lines)

    sets_with_total_overlaps = filter(total_overlap, sets)

    return len(list(sets_with_total_overlaps))


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    sets = map(parse_sets, lines)

    sets_with_any_overlap = filter(any_overlap, sets)

    return len(list(sets_with_any_overlap))
