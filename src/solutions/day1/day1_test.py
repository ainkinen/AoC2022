import os

from src.solutions.day1 import sum_elf, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')


def test_returns_sum_of_rows():
    in_str = '1\n' \
             '2\n' \
             '3\n'

    assert sum_elf(in_str) == 6


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == 24000


def test_part2_returns_expected_sample_result():
    assert part2(TEST_INPUT_PATH) == 45000
