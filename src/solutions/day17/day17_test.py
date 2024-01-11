import os

from src.solutions.day17 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'not_doc_test_input.txt')


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == 3068


def test_part2_returns_expected_sample_result():
    assert part2(TEST_INPUT_PATH) == 1514285714288
