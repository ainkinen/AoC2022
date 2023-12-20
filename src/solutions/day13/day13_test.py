import os

from src.solutions.day13 import part1, part2, assert_order

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')


def test_assert_order():
    assert assert_order(0, 1) == 1
    assert assert_order(1, 0) == -1
    assert assert_order(1, 1) == 0

    assert assert_order([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) == 1

    assert assert_order([[1], [2, 3, 4]], [[1], 4]) == 1

    assert assert_order([9], [[8, 7, 6]]) == -1

    assert assert_order([[4, 4], 4, 4], [[4, 4], 4, 4, 4]) == 1

    assert assert_order([7, 7, 7, 7], [7, 7, 7]) == -1

    assert assert_order([], [3]) == 1

    assert assert_order([[[]]], [[]]) == -1

    assert assert_order([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]) == -1


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == 13


def test_part2_returns_expected_sample_result():
    assert part2(TEST_INPUT_PATH) == 140
