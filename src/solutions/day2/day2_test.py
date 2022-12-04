import os

from src.solutions.day2 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == 15


def test_part2_returns_excepted_sample_result():
    assert part2(TEST_INPUT_PATH) == 12
