import os

from src.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


def sum_elf(in_str: str) -> int:
    lines = in_str.strip().split('\n')

    return sum(map(int, lines))


def part1(input_path: str = INPUT_PATH) -> int:
    input_by_elf = read_as_string(input_path).split('\n\n')

    elf_sums = map(sum_elf, input_by_elf)

    return max(elf_sums)


def part2(input_path: str = INPUT_PATH) -> int:
    input_by_elf = read_as_string(input_path).split('\n\n')

    elf_sums = map(sum_elf, input_by_elf)

    sorted_sums = list(reversed(sorted(elf_sums)))

    return sum(sorted_sums[0:3])
