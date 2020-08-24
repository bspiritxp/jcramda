from typing import Iterable, Callable
from functools import reduce as _reduce
import itertools as its
from . import curry

__all__ = (
    'of',
    'fold',
    'maps',
    'mapof',
    'starmap',
    'i_each',
    'fmap',
    'fmapof',
)


def of(*args):
    return tuple(its.chain(*[x if isinstance(x, Iterable) else [x] for x in args]))


@curry
def fold(func, init, it):
    return _reduce(func, it, init)


@curry
def maps(func, it, *args):
    return map(func, it, *args)


@curry
def mapof(func, it, *args):
    return of(map(func, it, *args))


# starmap(fun, seq) --> fun(*seq[0]), fun(*seq[1]), ...
starmap = curry(its.starmap)


@curry
def i_each(func, end, start=0, step=1):
    result = []
    for i in its.count(start, step):
        if i >= end:
            break
        result.append(func(i))
    return *result,


@curry
def fmap(func, seqs):
    return its.chain(*map(func, seqs))


@curry
def fmapof(func, seqs):
    return tuple(its.chain(*map(func, seqs)))

