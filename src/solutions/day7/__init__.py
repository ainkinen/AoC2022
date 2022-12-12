import dataclasses
import os
import re

from src.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclasses.dataclass
class File:
    dir: tuple[str, ...]
    name: str
    size: int

    @property
    def path(self) -> str:
        return '/'.join([*self.dir, self.name])


def read_files(in_lines: list[str]) -> list[File]:
    cwd: list[str] = ['/']
    files: list[File] = []

    for line in in_lines:
        # navigation
        if match := re.match(r'^\$ cd (?P<new_dir>.+)', line):
            new_dir = match.group('new_dir')
            if new_dir == '/':
                cwd = ['/']
            elif new_dir == '..':
                cwd.pop()
            else:
                cwd.append(new_dir)

            continue

        # files
        if match := re.match(r'^(?P<size>\d+) (?P<name>.+)', line):
            size = int(match.group('size'))
            name = match.group('name')
            files.append(File(
                dir=tuple(cwd),
                name=name,
                size=size,
            ))

        # ignored: 'ls', 'dir asd'

    return files


def folder_sizes(files: list[File]) -> dict[tuple, int]:
    f_sizes: dict[tuple, int] = {}

    for f in files:
        paths_to_process = list(f.dir)

        while paths_to_process:
            p = tuple(paths_to_process)
            f_sizes[p] = f_sizes.get(p, 0) + f.size
            paths_to_process.pop()

    return f_sizes


def part1(input_path: str = INPUT_PATH) -> int:
    input_lines = read_as_lines(input_path)

    files = read_files(input_lines)

    f_sizes = folder_sizes(files)

    max_100000 = {dir: size for dir, size in f_sizes.items() if size <= 100000}

    return sum(max_100000.values())


def part2(input_path: str = INPUT_PATH) -> int:
    input_lines = read_as_lines(input_path)

    files = read_files(input_lines)

    f_sizes = folder_sizes(files)

    total_space = 70000000
    required_space = 30000000

    currently_unused = total_space - f_sizes.get(('/',), 0)

    need_to_delete = required_space - currently_unused

    big_enough_folder_sizes = [size for dir, size in f_sizes.items() if size >= need_to_delete]

    return min(big_enough_folder_sizes)
