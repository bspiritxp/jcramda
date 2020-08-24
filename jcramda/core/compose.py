from typing import Callable, Iterable, Optional
from functools import reduce, partial


__all__ = (
    'compose',
    'pipe',
    'co',
    'chain',
)


def compose(*fns: Callable):
    assert len(fns) > 1
    funcs = list(reversed(fns))

    def composed_func(*args, **kwargs):
        init_value = funcs[0](*args, **kwargs)
        return reduce(lambda r, f: f(r), funcs[1:], init_value)

    return composed_func


co = compose


def pipe(*funcs: Callable):
    return compose(*reversed(funcs))


def chain(*args):
    if not isinstance(args[-1], Callable):
        *fs, seqs = args
        funcs = list(reversed(fs))
    else:
        funcs = list(reversed(args))
        seqs = None
    assert all(map(lambda x: isinstance(x, Callable), funcs))
    if len(funcs) == 1:
        mapper = co(tuple, partial(map, funcs[0]))
        return mapper(seqs) if seqs else mapper

    def reducer(xs):
        return reduce(lambda r, f: f(r, xs), funcs[1:], funcs[0](xs))

    return reducer(seqs) if seqs else reducer
