import os
import re
from math import prod
from typing import NamedTuple

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


class OreCount(NamedTuple):
    # priority order for tuple comparisons
    geode: int
    obs: int
    clay: int
    ore: int


class Cost(NamedTuple):
    geode: int
    obs: int
    clay: int
    ore: int


class Make(NamedTuple):
    geode: int
    obs: int
    clay: int
    ore: int


class Bot(NamedTuple):
    cost: Cost
    make: Make


class State(NamedTuple):
    ores: OreCount
    production: Make


Blueprint = list[Bot]


def parse_blueprint(line: str) -> Blueprint:
    num = [int(n) for n in re.findall(r'\d+', line)]

    return [
        Bot(Cost(0, 0, 0, num[1]), Make(0, 0, 0, 1)),  # ore bot
        Bot(Cost(0, 0, 0, num[2]), Make(0, 0, 1, 0)),  # clay bot
        Bot(Cost(0, 0, num[4], num[3]), Make(0, 1, 0, 0)),  # obsidian bot
        Bot(Cost(0, num[6], 0, num[5]), Make(1, 0, 0, 0)),  # geode bot
        Bot(Cost(0, 0, 0, 0), Make(0, 0, 0, 0)),  # non-bot, do nothing
    ]


def can_make(have: OreCount, cost: Cost) -> bool:
    return all(h >= c for h, c in zip(have, cost))


def new_count(have: OreCount, production: Make, spent: Cost = Cost(0, 0, 0, 0)) -> OreCount:
    return OreCount(*(h + p - s for h, p, s in zip(have, production, spent)))


def new_make(*p: Make) -> Make:
    return Make(*(sum(v) for v in zip(*p)))


def state_order_key(state: State) -> State:
    # Order by next turn counts, use production as a tie-breaker
    # Tuple comparison requires the values to be in the preferred order
    return State(new_count(state.ores, state.production), state.production)


def best_states(states: set[State]) -> set[State]:
    # Keep only the assumed best states to limit search space
    return set(sorted(states, key=state_order_key)[-1000:])


def solve(blueprint: Blueprint, time: int):
    states: set[State] = {State(OreCount(0, 0, 0, 0), Make(0, 0, 0, 1))}

    for t in range(time):
        new_states: set[State] = set()

        for ores, production in states:
            # branch new state for all possible new robots
            for cost, make in blueprint:
                if can_make(ores, cost):
                    new_states.add(State(new_count(ores, production, cost), new_make(production, make)))

        states = best_states(new_states)

    return max(counts.geode for (counts, _) in states)


def part1(input_path: str = INPUT_PATH) -> int:
    blueprints = list(map(parse_blueprint, read_as_lines(input_path)))
    max_geodes = [solve(bp, 24) for bp in blueprints]
    quality_levels = [i * mg for i, mg in enumerate(max_geodes, start=1)]
    return sum(quality_levels)


def part2(input_path: str = INPUT_PATH) -> int:
    blueprints = list(map(parse_blueprint, read_as_lines(input_path)))[:3]
    max_geodes = [solve(bp, 32) for bp in blueprints]
    return prod(max_geodes)
