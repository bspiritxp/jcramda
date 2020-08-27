from typing import Iterable, Callable, Any, Union, Sized, Optional
from functools import reduce as _reduce
import itertools as its
from more_itertools import with_iter, intersperse as _intersperse, consume, side_effect, ilen, \
    always_reversible as reverse, one
from ._curry import curry
from .operator import is_a, not_a

__all__ = (
    'of',
    'flatten',
    'one',
    'fold',
    'chain',
    'first',
    'last',
    'maps',
    'mapof',
    'starmap',
    'each',
    'fmap',
    'fmapof',
    'filter_',
    'filter_not',
    'dropwhile',
    'takewhile',
    'product',
    'permute',
    'combine',
    'zip_',
    'islice',
    'with_iter',
    'ilen',
    'reverse',
)


def of(*args):
    """
    将传入的参数平铺成一个tuple
    :param args: Iterable
    :return: tuple
    """
    return tuple(its.chain(*[x if isinstance(x, Iterable) else [x] for x in args]))


def flatten(*iters):
    from more_itertools import collapse
    return *collapse(iters),


def first(iterable):
    return next(iter(iterable), None)


def last(iterable):
    try:
        return iterable[-1]
    except (TypeError, AttributeError, KeyError):
        from collections import deque
        return deque(iterable, maxlen=1)[0]


@curry
def fold(func, init, it):
    """
    统合数据，即传统的 reduce 方法
    :param func:
    :param init:
    :param it:
    :return:
    """
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
def islice(rng: Union[int, tuple], iterate):
    return its.islice(iterate, *rng if isinstance(rng, tuple) else rng)


@curry
def each(func, seqs, chunk_size=None, before=None, after=None):
    return consume(side_effect(func, seqs, chunk_size, before, after))


@curry
def count(func: Callable[[int], Any],
          end: Union[int, Callable[[int, Any], bool]],
          start=0, step=1):
    """
    统计函数的执行次数
    :param func: 要执行的函数，参数传入当前次数
    :param end: 结束控制
        int: 根据次数控制，i < end
        (int, f(i)) -> bool: 返回True则中断
    :param start: 计数开始数，默认0
    :param step: 步长，默认1
    :return: int 执行次数
    """
    for i in its.count(start, step):
        if isinstance(end, int) and i >= end:
            return i
        r = func(i)
        if isinstance(end, Callable) and end(i, r):
            return i


@curry
def fmap(func, seqs):
    return its.chain(*map(func, seqs))


@curry
def fmapof(func, seqs):
    return tuple(its.chain(*map(func, seqs)))


@curry
def repeat(x, n):
    return its.repeat(x, n)


dropwhile = curry(its.dropwhile)
takewhile = curry(its.takewhile)


@curry
def filter_(func, seqs):
    return filter(func, seqs)


filter_not = curry(its.filterfalse)


@curry
def product(func, matrix):
    return map(func, its.product(*matrix))


@curry
def permute(seqs, r):
    """
    排列
    :param seqs: Iterable[_T]
    :param r: int
        如果 r 是0则返回全排列
    :return: Iterable[Tuple[_T]]
    """
    return its.permutations(seqs, r) if r else its.permutations(seqs)


@curry
def combine(seqs, r):
    """
    组合
    :param seqs:
    :param r:
    :return:
    """
    return its.combinations(seqs, r)


@curry
def zip_(fill_value, seq, *seqs):
    return its.zip_longest(seq, *seqs, fillvalue=fill_value)


@curry
def groupby(func, iterable):
    return its.groupby(iterable, func),


def chain(*args):
    funcs = of(reverse(filter(is_a(Callable), args)))
    f_count = len(funcs)
    if f_count <= 0:
        return flatten(*args)

    seqs = first(filter(not_a(Callable), args))
    if f_count == 1:
        reducer = maps(first(funcs))
        return reducer(seqs) if len(args) > f_count else reducer

    def reducer(xs):
        init_value = first(funcs)(xs)
        return _reduce(lambda r, f: f(r, xs), funcs[1:], init_value)

    return reducer(seqs) if seqs else reducer


# 等距插入固定元素 (e, iterable, n=1) -> Iterable
#         >>> list(intersperse('!', [1, 2, 3, 4, 5]))
#         [1, '!', 2, '!', 3, '!', 4, '!', 5]
intersperse = curry(_intersperse)

