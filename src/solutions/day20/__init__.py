import os

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


def mix(numbers: list[int], shuffles: int = 1) -> list[int]:
    indices: list[int] = list(range(len(numbers)))  # list of pointers to the original array

    for i in indices * shuffles:  # iterate a copy to allow mutations
        idx = indices.index(i)  # location of the number index
        indices.pop(idx)

        new_idx = (idx + numbers[i]) % len(indices)
        indices.insert(new_idx, i)

    return [numbers[ix] for ix in indices]


def get_output(numbers: list[int]) -> int:
    zero_idx = numbers.index(0)

    keys = (
        numbers[(zero_idx + 1000) % len(numbers)],
        numbers[(zero_idx + 2000) % len(numbers)],
        numbers[(zero_idx + 3000) % len(numbers)],
    )

    return sum(keys)


def part1(input_path: str = INPUT_PATH) -> int:
    numbers = [int(line) for line in read_as_lines(input_path)]

    mixed_numbers = mix(numbers)

    return get_output(mixed_numbers)


def part2(input_path: str = INPUT_PATH) -> int:
    numbers = [int(line) * 811589153 for line in read_as_lines(input_path)]

    mixed_numbers = mix(numbers, 10)

    return get_output(mixed_numbers)
