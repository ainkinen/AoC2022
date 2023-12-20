import os
import re
from functools import cmp_to_key
from typing import Union, assert_never

from src.utils.files import read_as_lines, read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

PacketValue = Union[int, list['PacketValue']]
Packet = int | list[PacketValue]


def parse_packet(in_str: str) -> Packet:
    # Run eval only if input looks expected
    assert len(re.sub(r'[\d,\[\]]', '', in_str)) == 0
    return eval(in_str)


def compare_numbers(a: int, b: int) -> int:
    # 1 = correct order, -1 = wrong order, 0 = Dunno
    if a < b:
        return 1

    if a > b:
        return -1

    return 0


def assert_order(a: Packet, b: Packet) -> int:
    # 1 = correct order, -1 = wrong order, 0 = Dunno
    ab = (a, b)
    match ab:
        case int(), int():
            return compare_numbers(ab[0], ab[1])

        case int(), list():
            return assert_order([a], b)

        case list(), int():
            return assert_order(a, [b])

        case list(), list():
            for (l, r) in zip(ab[0], ab[1]):
                res = assert_order(l, r)
                if res != 0:
                    return res

            return assert_order(len(ab[0]), len(ab[1]))

        case _:
            assert_never(ab[0])


def part1(input_path: str = INPUT_PATH) -> int:
    pairs = read_as_string(input_path).split('\n\n')

    line_pairs = [list(map(parse_packet, pair.strip().split('\n'))) for pair in pairs]

    order_correctness = [assert_order(a, b) for (a, b) in line_pairs]

    correct_ids = [idx for idx, correctness in enumerate(order_correctness, 1) if correctness == 1]

    return sum(correct_ids)


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    packets = [parse_packet(line) for line in lines if line != '']

    divider_1: Packet = [[2]]
    divider_2: Packet = [[6]]
    with_dividers = [*packets, divider_1, divider_2]

    sorted_packets = sorted(with_dividers, key=cmp_to_key(assert_order), reverse=True)

    idx1 = sorted_packets.index(divider_1) + 1
    idx2 = sorted_packets.index(divider_2) + 1

    return idx1 * idx2
