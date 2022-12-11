import os

import pytest

from src.solutions.day6 import part1, part2, find_marker

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')


@pytest.mark.parametrize('data_stream,expected', [
    ['mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7],
    ['bvwbjplbgvbhsrlpgdmjqwftvncz', 5],
    ['nppdvjthqldpwncqszvftbrmjlhg', 6],
    ['nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10],
    ['zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11],
])
def test_find_start_marker(data_stream, expected):
    assert find_marker(data_stream) == expected


@pytest.mark.parametrize('data_stream,expected', [
    ['mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19],
    ['bvwbjplbgvbhsrlpgdmjqwftvncz', 23],
    ['nppdvjthqldpwncqszvftbrmjlhg', 23],
    ['nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29],
    ['zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26],
])
def test_find_message_start(data_stream, expected):
    assert find_marker(data_stream, marker_len=14) == expected


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == 7


def test_part2_returns_excepted_sample_result():
    assert part2(TEST_INPUT_PATH) == 19
