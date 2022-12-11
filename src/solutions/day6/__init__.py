import os

from src.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


def count_unique(in_str: str) -> int:
    return len(set(in_str))


def find_marker(data_stream: str, marker_len: int = 4) -> int:
    for i in range(marker_len, len(data_stream)):
        start = i - marker_len
        end = i

        if count_unique(data_stream[start:end]) == marker_len:
            return i
    else:
        raise ValueError('Not found')


def part1(input_path: str = INPUT_PATH) -> int:
    in_str = read_as_string(input_path).strip()

    return find_marker(in_str)


def part2(input_path: str = INPUT_PATH) -> int:
    in_str = read_as_string(input_path).strip()

    return find_marker(in_str, marker_len=14)
