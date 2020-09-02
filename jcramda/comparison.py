from typing import Dict, List, Tuple, AnyStr, Callable, Iterable, Mapping, Sequence
from .core import curry, flip, co, lt, le, gt, ge, eq, attr, is_a, all_, not_a

__all__ = (
    'len_lt', 'len_le', 'len_eq', 'len_gt', 'len_ge', 'is_zero', 'is_nan',
    'attr_eq', 'is_a_dict', 'is_a_list', 'is_a_tuple', 'is_a_str', 'is_a_func',
    'is_a_int', 'is_iter', 'is_a_mapper', 'is_seq', 'is_simple_iter', 'nostr_seq',
)


len_lt = curry(lambda n, x: len(x) < n)
len_le = curry(lambda n, x: len(x) <= n)
len_eq = curry(lambda n, x: len(x) == n)
len_gt = curry(lambda n, x: len(x) > n)
len_ge = curry(lambda n, x: len(x) >= n)


is_zero = eq(0)


def is_nan(x):
    return str(x).lower() in ('nan', 'null', 'none')


@curry
def attr_eq(attr_name, value, obj):
    return co(
        eq(value),
        attr(attr_name),
    )(obj)


# typing

is_a_dict = is_a(Dict)
is_a_mapper = is_a(Mapping)
is_a_tuple = is_a(Tuple)
is_a_list = is_a(List)
is_a_str = is_a(AnyStr)
is_a_func = is_a(Callable)
is_a_int = is_a(int)
is_iter = is_a(Iterable)
is_simple_iter = all_([is_iter, not_a((bytes, str, Mapping))])
is_seq = is_a(Sequence)
nostr_seq = all_([is_seq, not_a((bytes, str))])

