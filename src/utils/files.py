from os import PathLike


def read_as_string(path: str | bytes | PathLike):
    with open(path) as f:
        return f.read()
