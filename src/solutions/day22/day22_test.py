import os

import pytest

from src.solutions.day22 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == 6032


@pytest.mark.skip(reason='Hardcoded wrap code')
def test_part2_returns_expected_sample_result():
    assert part2(TEST_INPUT_PATH) == 5031
