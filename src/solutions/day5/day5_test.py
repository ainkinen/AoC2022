import os

from src.solutions.day5 import part1, part2, parse_stacks, parse_instructions, Instruction

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')


def test_parse_stacks():
    input_str = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3"""

    assert parse_stacks(input_str) == {
        '1': ['Z', 'N'],
        '2': ['M', 'C', 'D'],
        '3': ['P'],
    }


def test_parse_instructions():
    input_str = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    assert parse_instructions(input_str) == [
        Instruction(1, '2', '1'),
        Instruction(3, '1', '3'),
        Instruction(2, '2', '1'),
        Instruction(1, '1', '2'),
    ]


def test_part1_returns_excepted_sample_result():
    assert part1(TEST_INPUT_PATH) == 'CMZ'


def test_part2_returns_excepted_sample_result():
    assert part2(TEST_INPUT_PATH) == 'MCD'
