import operator as _op
from typing import Tuple, Callable, Any, Iterable

from . import curry, flip

__all__ = (
    'lt', 'le', 'eq', 'ne', 'ge', 'gt', 'not_', 'truth', 'is_', 'is_not', 'is_a', 'not_a',
    'not_none', 'is_none', 'between',
    'add', 'sub', 'and_', 'floordiv', 'div', 'inv', 'lshift', 'mod', 'mul', 'matmul',
    'neg', 'or_', 'pos', 'pow_', 'xor', 'concat', 'in_', 'countOf', 'delitem', 'getitem',
    'indexOf', 'setitem', 'attr', 'props', 'bind', 'iadd', 'iand', 'iconcat', 'ifloordiv',
    'ilshift', 'imod', 'imul', 'imatmul', 'ior', 'ipow', 'irshift', 'isub', 'idiv', 'ixor',
    'identity', 'when', 'always', 'if_else',
)


# Comparison ===========================
eq = curry(_op.eq)
ne = curry(_op.ne)
lt = flip(_op.lt)
le = flip(_op.le)
ge = flip(_op.ge)
gt = flip(_op.gt)
between = curry(lambda min_, max_, x: min_ <= x < max_)

# Logical ===============================

not_ = _op.not_
truth = _op.truth
is_ = flip(_op.is_)
is_not = flip(_op.is_not)
is_a = curry(lambda types, obj: isinstance(obj, types))
not_a = curry(lambda types, obj: not isinstance(obj, types))
is_none = is_(None)
not_none = is_not(None)

# Math

add = curry(_op.add)
sub = flip(_op.sub)
and_ = curry(_op.and_)
floordiv = flip(_op.floordiv)
div = flip(_op.truediv)
inv = _op.inv
lshift = flip(_op.lshift)
mod = flip(_op.mod)
mul = curry(_op.mul)
matmul = flip(_op.matmul)
neg = _op.neg
or_ = curry(_op.or_)
pos = _op.pos
pow_ = flip(_op.pow)
xor = curry(_op.xor)

# Sequence Base

concat = curry(_op.concat)
in_ = curry(_op.contains)
not_in = curry(lambda a, b: b not in a)
countOf = curry(_op.countOf)
delitem = flip(_op.delitem)
getitem = flip(_op.getitem)
indexOf = flip(_op.indexOf)
setitem = curry(lambda b, a, c: _op.setitem(a, b, c))

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
