from typing import Iterable
from jcramda.core._curry import curry


__all__ = (
    'head',
    'append',
    'tail',
)


def head(seqs: Iterable):
    return seqs[0]


@curry
def append(x, seqs: Iterable) -> list:
    return [*seqs, x]


def tail(xs):
    return xs[-1]
