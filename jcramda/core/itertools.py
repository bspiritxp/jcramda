from typing import Iterable, Callable, Any, Union
from functools import reduce as _reduce
import itertools as its
from . import curry

__all__ = (
    'of',
    'fold',
    'maps',
    'mapof',
    'starmap',
    'each',
    'ieach',
    'foreach',
    'fmap',
    'fmapof',
    'filter_',
    'filter_not',
    'dropwhile',
    'takewhile',
    'slice_',
    'product',
    'permute',
    'combine',
    'zip_',
)


def of(*args):
    """
    将传入的参数平铺成一个tuple
    :param args: Iterable
    :return: tuple
    """
    return tuple(its.chain(*[x if isinstance(x, Iterable) else [x] for x in args]))


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
def each(func, seqs):
    for index, item in enumerate(seqs):
        func(index, item)


@curry
def ieach(func, end, start=0, step=1):
    for i in range(start, end, step):
        if i >= end:
            break
        func(i)


@curry
def foreach(func, seqs):
    for item in seqs:
        func(item)


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
    return tuple(its.repeat(x, n))


dropwhile = curry(its.dropwhile)
takewhile = curry(its.takewhile)


@curry
def filter_(func, seqs):
    return filter(func, seqs)


filter_not = curry(its.filterfalse)


@curry
def slice_(rng: range, seq: Iterable):
    return seq[rng.start:rng.stop:rng.step]


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
