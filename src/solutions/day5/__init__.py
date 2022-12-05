import dataclasses
import os
import re
from functools import reduce
from itertools import zip_longest

from src.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_stacks(in_str: str) -> dict[str, list[str]]:
    stack_info_rows = in_str.split('\n')

    # transpose to get columns as lists
    columns = list(zip_longest(*stack_info_rows, fillvalue=''))

    # filter columns without any alphanum chars
    filtered_columns = [col for col in columns if any(char.isalnum() for char in col)]

    # clean out blank strings from the columns
    clean_columns = [list(filter(lambda char: char.strip(), stack)) for stack in filtered_columns]

    def collect(d: dict[str, list], col: list) -> dict[str, list]:
        key = col[-1]
        stack = list(reversed(col[:-1]))
        d[key] = stack
        return d

    return reduce(collect, clean_columns, {})


@dataclasses.dataclass
class Instruction:
    amount: int
    from_i: str
    to_i: str


def parse_instructions(in_str: str) -> list[Instruction]:
    instruction_rows = in_str.strip().split('\n')

    regex_results = map(lambda s: re.match(r'.*?(?P<amount>\d+).*?(?P<from>\d+).*?(?P<to>\d+)', s), instruction_rows)

    matches = filter(None, regex_results)

    lst = list(map(lambda m: Instruction(
        amount=int(m.group('amount')), from_i=m.group('from'), to_i=m.group('to')
    ), matches))

    return lst


def part1(input_path: str = INPUT_PATH) -> str:
    starting_stacks, instruction_list = read_as_string(input_path).split('\n\n')
    stacks = parse_stacks(starting_stacks)
    instructions = parse_instructions(instruction_list)

    for ins in instructions:
        for i in range(ins.amount):
            stacks[ins.to_i].append(stacks[ins.from_i].pop())

    last_crates = [stack[-1] for stack in stacks.values()]

    return ''.join(last_crates)


def part2(input_path: str = INPUT_PATH) -> str:
    starting_stacks, instruction_list = read_as_string(input_path).split('\n\n')
    stacks = parse_stacks(starting_stacks)
    instructions = parse_instructions(instruction_list)

    for ins in instructions:
        from_stack = stacks[ins.from_i]
        left_over, top_crates = from_stack[:-ins.amount], from_stack[-ins.amount:]
        stacks[ins.from_i] = left_over
        stacks[ins.to_i] += top_crates

    last_crates = [stack[-1] for stack in stacks.values()]

    return ''.join(last_crates)
