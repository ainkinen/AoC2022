import math
import os
import re
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Literal, assert_never, Union

from src.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Op = Union[Literal['+'], Literal['*']]
OpValue = Union[Literal['old'], int]


@dataclass
class Monkey:
    id: int
    items: deque[int]
    op: Op
    op_value: OpValue
    test: int
    true_dest: int
    false_dest: int


number_pattern = r'\d+'


def parse_monkey(lines: list[str]) -> Monkey:
    id_str = re.findall(number_pattern, lines[0])[0]
    item_strs = re.findall(number_pattern, lines[1])

    op_match = re.search(r'([+*]) (\w+)', lines[2])
    if not op_match:
        raise Exception(lines[2])
    op, value = op_match.groups()

    division_str = re.findall(number_pattern, lines[3])[0]
    true_str = re.findall(number_pattern, lines[4])[0]
    false_str = re.findall(number_pattern, lines[5])[0]

    return Monkey(
        id=int(id_str),
        items=deque([int(i) for i in item_strs]),
        op='+' if op == '+' else '*',
        op_value='old' if value == 'old' else int(value),
        test=int(division_str),
        true_dest=int(true_str),
        false_dest=int(false_str),
    )


def adjust_level(item: int, op: Op, op_value: OpValue) -> int:
    match op:
        case '*':
            if op_value == 'old':
                return item * item
            else:
                assert isinstance(op_value, int)
                return item * op_value
        case '+':
            if op_value == 'old':
                return item + item
            else:
                assert isinstance(op_value, int)
                return item + op_value

        case _:
            assert_never(op)


def part1(input_path: str = INPUT_PATH) -> int:
    sections = read_as_string(input_path).split('\n\n')
    monkeys = {m.id: m for m in [parse_monkey(s.split('\n')) for s in sections]}

    inspections: dict[int, int] = defaultdict(int)

    for i in range(20):
        for monkey_id, monkey in monkeys.items():

            inspections[monkey_id] += len(monkey.items)

            while monkey.items:
                item = monkey.items.popleft()
                item = adjust_level(item, monkey.op, monkey.op_value)
                item = item // 3
                to_monkey = monkey.true_dest if item % monkey.test == 0 else monkey.false_dest
                monkeys[to_monkey].items.append(item)

    sorted_inspection_counts = sorted(inspections.values(), reverse=True)

    return sorted_inspection_counts[0] * sorted_inspection_counts[1]


def part2(input_path: str = INPUT_PATH) -> int:
    sections = read_as_string(input_path).split('\n\n')
    monkeys = {m.id: m for m in [parse_monkey(s.split('\n')) for s in sections]}

    inspections: dict[int, int] = defaultdict(int)

    common_divider = math.prod(m.test for m in monkeys.values())

    for i in range(10000):
        for monkey_id, monkey in monkeys.items():

            inspections[monkey_id] += len(monkey.items)

            while monkey.items:
                item = monkey.items.popleft()
                item = adjust_level(item, monkey.op, monkey.op_value)
                item = item % common_divider
                to_monkey = monkey.true_dest if item % monkey.test == 0 else monkey.false_dest
                monkeys[to_monkey].items.append(item)

    sorted_inspection_counts = sorted(inspections.values(), reverse=True)

    return sorted_inspection_counts[0] * sorted_inspection_counts[1]
