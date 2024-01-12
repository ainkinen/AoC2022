import os

from src.solutions.day19 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == 33


def test_part2_returns_expected_sample_result():
    assert part2(TEST_INPUT_PATH) == 56 * 62
