import os

from src.solutions.day10 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), 'test_input_2.txt')

part2_output = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
""".strip()


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == -1
    assert part1(TEST_INPUT_2_PATH) == 13140


def test_part2_returns_expected_sample_result():
    assert part2(TEST_INPUT_2_PATH) == part2_output
