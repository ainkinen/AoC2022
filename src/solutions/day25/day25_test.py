import os

import pytest

from src.solutions.day25 import part1, snafu_to_int, int_to_snafu

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')

cases = [
    [1, '1'],
    [2, '2'],
    [3, '1='],
    [4, '1-'],
    [5, '10'],
    [6, '11'],
    [7, '12'],
    [8, '2='],
    [9, '2-'],
    [10, '20'],
    [15, '1=0'],
    [20, '1-0'],
    [2022, '1=11-2'],
    [12345, '1-0---0'],
    [314159265, '1121-1110-1=0']
]


@pytest.mark.parametrize('integer, snafu', cases)
def test_snafu_to_int(snafu: str, integer: int):
    assert snafu_to_int(snafu) == integer


@pytest.mark.parametrize('integer, snafu', cases)
def test_int_to_snafu(integer: int, snafu: str):
    assert int_to_snafu(integer) == snafu


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == '2=-1=0'
