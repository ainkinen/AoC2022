import os

from src.solutions.day15 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH, row=10) == 26


def test_part2_returns_expected_sample_result():
    assert part2(TEST_INPUT_PATH, max_range=20) == 56000011
