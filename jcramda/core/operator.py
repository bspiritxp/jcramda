import operator as _op
from typing import Tuple, Callable, Any, Iterable

from . import curry, flip

__all__ = (
    'lt', 'le', 'eq', 'ne', 'ge', 'gt', 'not_', 'truth', 'is_', 'is_not', 'is_a', 'is_not_a',
    'add', 'sub', 'and_', 'floordiv', 'div', 'inv', 'lshift', 'mod', 'mul', 'matmul',
    'neg', 'or_', 'pos', 'pow_', 'xor', 'concat', 'contains', 'countOf', 'delitem', 'getitem',
    'indexOf', 'setitem', 'attr', 'props', 'bind', 'iadd', 'iand', 'iconcat', 'ifloordiv',
    'ilshift', 'imod', 'imul', 'imatmul', 'ior', 'ipow', 'irshift', 'isub', 'idiv', 'ixor',
    'identity', 'when', 'always', 'if_else',
)


# Comparison ===========================
eq = curry(_op.eq)
ne = curry(_op.ne)
lt = curry(lambda a, b: _op.lt(b, a))
le = curry(lambda a, b: _op.le(b, a))
ge = curry(lambda a, b: _op.ge(b, a))
gt = curry(lambda a, b: _op.gt(b, a))

# Logical ===============================

not_ = _op.not_
truth = _op.truth
is_ = flip(_op.is_)
is_not = flip(_op.is_not)
is_a = curry(lambda types, obj: isinstance(obj, types))
is_not_a = curry(lambda types, obj: not isinstance(obj, types))

# Math

add = curry(_op.add)
sub = curry(_op.sub)
and_ = curry(_op.and_)
floordiv = curry(_op.floordiv)
div = curry(_op.truediv)
inv = _op.inv
lshift = curry(_op.lshift)
mod = curry(_op.mod)
mul = curry(_op.mul)
matmul = curry(_op.matmul)
neg = _op.neg
or_ = curry(_op.or_)
pos = _op.pos
pow_ = curry(lambda p, x: x ** p)
xor = curry(_op.xor)

# Sequence Base

concat = curry(_op.concat)
contains = curry(_op.contains)
countOf = curry(_op.countOf)
delitem = curry(_op.delitem)
getitem = curry(_op.getitem)
indexOf = curry(_op.indexOf)
setitem = curry(_op.setitem)

attr = _op.attrgetter
props = _op.itemgetter
bind = _op.methodcaller

iadd = curry(_op.iadd)
iand = curry(_op.iand)
iconcat = curry(_op.iconcat)
ifloordiv = curry(_op.ifloordiv)
ilshift = curry(_op.ilshift)
imod = curry(_op.imod)
imul = curry(_op.imul)
imatmul = curry(_op.imatmul)
ior = curry(_op.ior)
ipow = curry(_op.ipow)
irshift = curry(_op.irshift)
isub = curry(_op.isub)
idiv = curry(_op.itruediv)
ixor = curry(_op.ixor)


# customs ==============================
@curry
def identity(f, *args, **kw):
    if isinstance(f, Callable):
        return f(*args, **kw)
    return f


@curry
def when(cases: Iterable[Tuple[Callable, Any]], else_, value):
    for f, elem in cases:
        # noinspection PyBroadException
        try:
            if f(value):
                return identity(elem, value)
        except Exception:
            pass
    return identity(else_, value)


@curry
def always(x, _):
    return x


@curry
def if_else(p: Iterable[Callable], value):
    pred, success, failed = p
    return success(value) if pred(value) else failed(value)


# noinspection PyBroadException
@curry
def try_catch(p: Iterable[Callable], value):
    func, failed = p
    try:
        return func(value)
    except Exception:
        return failed(value)
