import os

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

snafu_chars = '=-012'
snafu_digits: dict[str, int] = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}


def snafu_to_int(snafu: str) -> int:
    digits = [snafu_digits[char] for char in snafu]

    powers = [d * 5 ** i for i, d in enumerate(reversed(digits))]

    return sum(powers)


def int_to_snafu(integer: int) -> str:
    snafu = ''

    while integer:
        integer, mod = divmod(integer + 2, 5)
        snafu += snafu_chars[mod]

    return snafu[::-1]


def part1(input_path: str = INPUT_PATH) -> str:
    snafus = read_as_lines(input_path)

    integer_sum = sum(map(snafu_to_int, snafus))

    return int_to_snafu(integer_sum)
