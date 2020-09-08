import more_itertools as mil
from typing import Iterable, MutableSequence, Reversible, Sized, Callable, Sequence
from collections import *
from jcramda.core import curry, between, flip, of, islice

__all__ = (
    'append', 'prepend', 'pop', 'shift', 'update', 'adjust', 'slices',
    'chunked', 'windowed', 'padded', 'nth_or_last', 'iterate', 'split_before',
    'split_after', 'split_at', 'split_into', 'split_when', 'distribute', 'adjacent',
    'locate', 'lstrip_f', 'rstrip_f', 'strip_f', 'take', 'tabulate', 'tail', 'consume', 'nth',
    'all_eq', 'quantify', 'ncycles', 'find_one', 'iter_except', 'unique_set', 'grouper',
    'partition_f', 'update_range',
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
def update_range(upset, seqs: Sequence, start=0, stop=None, step=1):
    r = list(seqs)
    for i, v in islice((start, stop, step), enumerate(r)):
        r[i] = upset(v)
    return r


@curry
def adjust(index: int, f: Callable, seqs: MutableSequence):
    if between(0, len(seqs), index):
        seqs[index] = f(seqs[index])
    return seqs


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
lstrip_f = flip(mil.lstrip)
rstrip_f = flip(mil.rstrip)
strip_f = flip(mil.strip)
all_eq = mil.all_equal
quantify = flip(mil.quantify)
ncycles = flip(mil.ncycles)
grouper = flip(mil.grouper)
partition_f = curry(mil.partition)
unique_set = flip(mil.unique_everseen)
iter_except = curry(mil.iter_except)
find_one = curry(lambda f, xs: mil.first_true(xs, None, f))

