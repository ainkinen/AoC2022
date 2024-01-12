import operator
import os

from sympy import Symbol, solve, Eq  # , Rational

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

Monkeys = dict[str, str]  # name, job

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def part1(input_path: str = INPUT_PATH) -> int:
    monkeys: Monkeys = {name: job for name, job in list(line.split(': ') for line in (read_as_lines(input_path)))}

    def get_result(name: str) -> int:
        job = monkeys[name]
        try:
            return int(job)
        except ValueError:
            m1, op, m2 = job.split(' ')
            return ops[op](get_result(m1), get_result(m2))

    return round(get_result('root'))


def part2(input_path: str = INPUT_PATH) -> int:
    monkeys: Monkeys = {name: job for name, job in list(line.split(': ') for line in (read_as_lines(input_path)))}

    human = Symbol('human')

    def flatten(name: str):
        if name == 'humn':
            return human

        job = monkeys[name]
        try:
            return int(job)
        except ValueError:
            m1, op, m2 = job.split(' ')
            r1, r2 = flatten(m1), flatten(m2)

            return ops[op](r1, r2)

    side1, _, side2 = monkeys['root'].split(' ')
    eq1, eq2 = flatten(side1), flatten(side2)

    solutions = solve(Eq(eq1, eq2), human, dict=True)

    return round(solutions[0][human])
