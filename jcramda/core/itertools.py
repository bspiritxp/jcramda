import itertools as its
from functools import reduce as _reduce
from typing import Iterable, Callable, Any, Union

from more_itertools import with_iter, intersperse as _intersperse, consume, side_effect, ilen, \
    always_reversible as reverse, replace as _replace, one as _one

from ._curry import curry
from .compose import co
from .operator import is_a, not_a, is_none

__all__ = (
    'of',
    'flatten',
    'one',
    'fold',
    'chain',
    'first',
    'last',
    'maps',
    'map_',
    'reduce_',
    'mapof',
    'starmap',
    'foreach',
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
    'repeat',
    'reverse',
    'ireplace',
    'map_reduce',
    'scan',
)


def of(*args, cls=tuple):
    """
    将传入的参数平铺成一个tuple
    :param cls: 类，可以是 （tuple, list, set, etc...）或其他衍生可迭代容器类或方法，默认: tuple
    :param args: Iterable
    :return: cls指定的迭代类型
    """
    return cls(its.chain(*[x if isinstance(x, Iterable) else [x] for x in args]))


def flatten(*iters):
    if len(iters) == 1 and not_a(Iterable, iters[0]):
        return iters[0]
    from more_itertools import collapse
    return *collapse(iters),


def one(iterable):
    """ 如果传入的迭代器仅有一个元素，则返回这个元素，否则返回迭代器的结果（Tuple） """
    r = tuple(iterable) if is_a(Iterable, iterable) else iterable
    try:
        return _one(r)
    except (TypeError, IndexError, ValueError):
        return r


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


map_ = maps
reduce_ = fold


@curry
def mapof(func, it, *args):
    return of(map(func, it, *args))


# starmap(fun, seq) --> fun(*seq[0]), fun(*seq[1]), ...
starmap = curry(its.starmap)


@curry
def islice(rng: Union[int, tuple], iterate):
    return its.islice(iterate, *rng if isinstance(rng, tuple) else rng)


@curry
def foreach(func, seqs, chunk_size=None, before=None, after=None):
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
def repeat(n, x):
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
    funcs = reverse(filter(is_a(Callable), args))
    first_func = first(funcs)
    if is_none(first_func):
        return flatten(*args)
    seqs = of(filter(not_a(Callable), args))
    reducer = co(one, flatten,
                 maps(lambda x: fold(lambda r, f: f(r, x), first_func(x), funcs)))

    return reducer(seqs) if seqs else co(reducer, of)


# 等距插入固定元素 (e, iterable, n=1) -> Iterable
#         >>> list(intersperse('!', [1, 2, 3, 4, 5]))
#         [1, '!', 2, '!', 3, '!', 4, '!', 5]
intersperse = curry(_intersperse)


@curry
def ireplace(pred, sub, iterable, _count=None, window_size=1):
    return _replace(iterable, pred, sub, _count, window_size)


@curry
def map_reduce(key: Callable, emit: Callable, iterable: Iterable, reducer: Callable = None):
    from more_itertools import map_reduce
    return map_reduce(iterable, key, emit, reducer)


@curry
def scan(func, init, iterable):
    result = [init]
    r = init
    for x in iterable:
        r = func(r, x)
        result.append(r)
    return result
