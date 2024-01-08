import os

from src.solutions.day16 import part1, part2, ValveMap, parse_valve, Valve
from src.utils.files import read_as_lines

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')

valves: ValveMap = {valve.name: valve for valve in map(parse_valve, read_as_lines(TEST_INPUT_PATH))}


def test_parse_valve():
    assert parse_valve('Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE') == Valve(
        name='DD',
        flow_rate=20,
        tunnels={'CC', 'AA', 'EE'}
    )


def test_part1_returns_excepted_sample_result(monkeypatch):
    assert part1(TEST_INPUT_PATH) == 1651


def test_part2_returns_expected_sample_result():
    assert part2(TEST_INPUT_PATH) == 1707
