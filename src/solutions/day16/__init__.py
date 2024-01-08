import os
import re
from collections import defaultdict
from functools import cache
from itertools import product
from typing import NamedTuple

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

OPEN_TIME = 1


class Valve(NamedTuple):
    name: str
    flow_rate: int
    tunnels: set[str]


ValveMap = dict[str, Valve]

DistanceMap = dict[tuple[str, str], int]  # from-to, distance


def parse_valve(line: str) -> Valve:
    flow_rate_pattern = r'\d+'
    flow_rate = re.findall(flow_rate_pattern, line)[0]

    name_pattern = r'[A-Z]{2}'
    name, *tunnels = re.findall(name_pattern, line)

    return Valve(name, int(flow_rate), set(tunnels))


def part1(input_path: str = INPUT_PATH) -> int:
    valves: list[Valve] = [parse_valve(line) for line in read_as_lines(input_path)]
    flows: dict[str, int] = {v.name: v.flow_rate for v in valves if v.flow_rate}
    valve_names = [v.name for v in valves]

    # Floyd-Warshall algo
    dist: DistanceMap = defaultdict(lambda: 1000000)  # Default just needs to be bigger than max time in this case
    for valve in valves:
        for to in valve.tunnels:
            dist[valve.name, to] = 1
    for k, i, j in product(valve_names, valve_names, valve_names):
        dist[(i, j)] = min(dist[(i, j)], dist[(i, k)] + dist[(k, j)])

    @cache
    def search(time_left: int, cur_loc: str = 'AA', closed_valves: frozenset[str] = frozenset(flows)):

        return max(
            [
                # flow from next valve until end
                flows[next_valve] * (time_left - dist[cur_loc, next_valve] - OPEN_TIME)
                # flows from future valves with time left
                + search(time_left - dist[cur_loc, next_valve] - OPEN_TIME, next_valve, closed_valves - {next_valve})
                for next_valve in closed_valves if dist[cur_loc, next_valve] < time_left
            ]
            + [0]  # fallback
        )

    return search(30)


def part2(input_path: str = INPUT_PATH) -> int:
    valves: list[Valve] = [parse_valve(line) for line in read_as_lines(input_path)]
    flows: dict[str, int] = {v.name: v.flow_rate for v in valves if v.flow_rate}
    valve_names = [v.name for v in valves]

    # Floyd-Warshall algo
    dist: DistanceMap = defaultdict(lambda: 1000000)  # Default just needs to be bigger than max time in this case
    for valve in valves:
        for to in valve.tunnels:
            dist[valve.name, to] = 1
    for k, i, j in product(valve_names, valve_names, valve_names):
        dist[(i, j)] = min(dist[(i, j)], dist[(i, k)] + dist[(k, j)])

    @cache
    def search(time_left: int, cur_loc: str = 'AA', closed_valves: frozenset[str] = frozenset(flows), e: bool = False):
        return max(
            [
                # flow from next valve until end
                flows[next_valve] * (time_left - dist[cur_loc, next_valve] - OPEN_TIME)
                # flows from future valves with time left
                + search(time_left - dist[cur_loc, next_valve] - OPEN_TIME, next_valve, closed_valves - {next_valve}, e)
                for next_valve in closed_valves if dist[cur_loc, next_valve] < time_left
            ]
            + [search(26, closed_valves=closed_valves) if e else 0]
        )

    return search(26, e=True)
