import os
from enum import Enum

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


class Play(int, Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def _score_round(plays: tuple[Play, Play]) -> int:
    you, opponent = plays[1], plays[0]

    match you, opponent:
        # wins
        case (Play.ROCK, Play.SCISSORS) | (Play.PAPER, Play.ROCK) | (Play.SCISSORS, Play.PAPER):
            return you.value + 6
        # ties
        case (Play.ROCK, Play.ROCK) | (Play.PAPER, Play.PAPER) | (Play.SCISSORS, Play.SCISSORS):
            return you.value + 3
        # losses
        case (Play.ROCK, Play.PAPER) | (Play.PAPER, Play.SCISSORS) | (Play.SCISSORS, Play.ROCK):
            return you.value + 0
        # fallback
        case _ as e:
            print(e)
            raise ValueError('Unknown combo')


_map_to_play = dict(
    A=Play.ROCK,
    B=Play.PAPER,
    C=Play.SCISSORS,
    X=Play.ROCK,
    Y=Play.PAPER,
    Z=Play.SCISSORS,
)

_map_result_to_play = {
    (Play.ROCK, 'X'): (Play.ROCK, Play.SCISSORS),
    (Play.ROCK, 'Y'): (Play.ROCK, Play.ROCK),
    (Play.ROCK, 'Z'): (Play.ROCK, Play.PAPER),
    (Play.PAPER, 'X'): (Play.PAPER, Play.ROCK),
    (Play.PAPER, 'Y'): (Play.PAPER, Play.PAPER),
    (Play.PAPER, 'Z'): (Play.PAPER, Play.SCISSORS),
    (Play.SCISSORS, 'X'): (Play.SCISSORS, Play.PAPER),
    (Play.SCISSORS, 'Y'): (Play.SCISSORS, Play.SCISSORS),
    (Play.SCISSORS, 'Z'): (Play.SCISSORS, Play.ROCK),
}


def _round_to_plays(rd: list[str]) -> tuple[Play, Play]:
    play0 = _map_to_play.get(rd[0])
    play1 = _map_to_play.get(rd[1])
    if play0 is None or play1 is None:
        raise ValueError(f'unknown round: {rd}')

    return play0, play1


def _plays_from_result(rd: list[str]) -> tuple[Play, Play]:
    opponent_play = _map_to_play.get(rd[0])
    result = rd[1]
    if opponent_play is None or result is None:
        raise ValueError(f'unknown round: {rd}')

    plays = _map_result_to_play.get((opponent_play, result))

    if plays:
        return plays
    else:
        raise ValueError(f'unknown round: {rd}')


def part1(input_path: str = INPUT_PATH) -> int:
    # ['A', 'Y']
    rounds = map(lambda line: line.split(" "), read_as_lines(input_path))

    # (Play.ROCK, Play.PAPER)
    plays = map(_round_to_plays, rounds)

    # 8
    scores = map(_score_round, plays)

    return sum(scores)


def part2(input_path: str = INPUT_PATH) -> int:
    # ['A', 'Y']
    rounds = map(lambda line: line.split(" "), read_as_lines(input_path))

    # (Play.ROCK, Play.ROCK) draw
    plays = map(_plays_from_result, rounds)

    # 4
    scores = map(_score_round, plays)

    return sum(scores)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
