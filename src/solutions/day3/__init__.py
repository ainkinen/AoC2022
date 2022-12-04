import os
import re
from typing import Iterator

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


def rucksack_sets(in_str: str) -> tuple[set[str], set[str]]:
    split_point = len(in_str) // 2
    pocket1 = in_str[0:split_point]
    pocket2 = in_str[split_point:]

    return set(pocket1), set(pocket2)


def common_item(sets: tuple[set[str], set[str]]) -> str:
    intersection = sets[0].intersection(sets[1])
    return next(iter(intersection))


def score_items(in_str: str) -> int:
    if re.match(r'^[a-z]$', in_str):
        # a-z -> 1-26
        return ord(in_str) - 96
    elif re.match(r'^[A-Z]$', in_str):
        # A-Z -> 27-52
        return ord(in_str) - 38
    else:
        raise ValueError


def chunks(lst: list[str], n: int) -> Iterator[tuple[str, ...]]:
    for i in range(0, len(lst), n):
        yield tuple(lst[i:i + n])


def chunks_of(lst: list, num: int) -> list[tuple[str, ...]]:
    return list(chunks(lst, num))


def common_item_in_group(group: tuple[str, ...]) -> str:
    sack1, sack2, sack3 = group
    set1 = set(sack1)
    set2 = set(sack2)
    set3 = set(sack3)

    intersection = set1.intersection(set2).intersection(set3)

    return next(iter(intersection))


def part1(input_path: str = INPUT_PATH) -> int:
    input_lines = read_as_lines(input_path)

    sacks = map(rucksack_sets, input_lines)

    common_items = map(common_item, sacks)

    scores = map(score_items, common_items)

    return sum(scores)


def part2(input_path: str = INPUT_PATH) -> int:
    input_lines = read_as_lines(input_path)

    groups = chunks_of(input_lines, 3)

    common_items = map(common_item_in_group, groups)

    scores = map(score_items, common_items)

    return sum(scores)
