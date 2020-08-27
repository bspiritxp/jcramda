import more_itertools as mil
from typing import Iterable, MutableSequence, Reversible, Sized, Callable, Sequence
from collections import *
from .core import curry, between, flip, of

__all__ = (
    'append', 'prepend', 'pop', 'shift', 'update', 'adjust', 'join', 'slices',
    'chunked', 'windowed', 'padded', 'nth_or_last', 'iterate', 'split_before',
    'split_after', 'split_at', 'split_into', 'split_when', 'distribute', 'adjacent',
    'locate', 'lstrip', 'rstrip', 'strip', 'take', 'tabulate', 'tail', 'consume', 'nth',
    'all_eq', 'quantify', 'ncycles', 'replace', 'map_reduce',
)


@curry
def append(x, seqs: Iterable):
    return of(seqs, x)


def prepend(x, seqs: Iterable):
    return of(x, seqs)


def pop(seqs: MutableSequence):
    return seqs.pop()


def shift(seqs: MutableSequence):
    return seqs.pop(0)


@curry
def update(index: int, v, seqs: MutableSequence):
    if between(0, len(seqs), index):
        seqs[index] = v
    return seqs


@curry
def adjust(index: int, f: Callable, seqs: MutableSequence):
    if between(0, len(seqs), index):
        seqs[index] = f(seqs[index])
    return seqs


@curry
def join(sep: str, seqs: Iterable) -> str:
    return sep.join([str(x) for x in seqs if x is not None])


@curry
def slices(_s: tuple, seqs: Sequence):
    return seqs[slice(*_s)]


# more itertools curried
chunked = flip(mil.chunked)
windowed = flip(mil.windowed)


@curry
def padded(v, n, iterable, next_multiple=False):
    return mil.padded(iterable, v, n, next_multiple)


take = curry(mil.take)
tail = curry(mil.tail)
tabulate = curry(mil.tabulate)
consume = flip(mil.consume)
nth = flip(mil.nth)


nth_or_last = flip(mil.nth_or_last)
# 递归: (f, start) -> ``start``, ``f(start)``, ``f(f(start))``, ...
iterate = curry(mil.iterate)
split_at = flip(mil.split_at)
split_before = flip(mil.split_before)
split_after = flip(mil.split_after)
split_when = flip(mil.split_when)
split_into = flip(mil.split_into)
distribute = curry(mil.distribute)
adjacent = curry(mil.adjacent)
# Yield the index of each item in *iterable* for which *pred* returns ``True``
locate = flip(mil.locate)
lstrip = flip(mil.lstrip)
rstrip = flip(mil.rstrip)
strip = flip(mil.strip)
all_eq = mil.all_equal
quantify = flip(mil.quantify)
ncycles = flip(mil.ncycles)
grouper = flip(mil.grouper)
partition = curry(mil.partition)
unique_set = flip(mil.unique_everseen)
iter_except = curry(mil.iter_except)
first_true = curry(lambda f, dv, xs: mil.first_true(xs, dv, f))


@curry
def replace(pred, sub, iterable, count=None, window_size=1):
    return mil.replace(iterable, pred, sub, count, window_size)


@curry
def map_reduce(key: Callable, emit: Callable, iterable: Iterable, reducer: Callable = None):
    from more_itertools import map_reduce
    return map_reduce(iterable, key, emit, reducer)
