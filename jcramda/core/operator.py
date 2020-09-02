import operator as _op
from typing import Tuple, Callable, Any, Iterable
from itertools import islice
from ._curry import curry, flip


__all__ = (
    'lt', 'le', 'eq', 'ne', 'ge', 'gt', 'not_', 'truth', 'is_', 'is_not', 'is_a', 'not_a',
    'not_none', 'is_none', 'between','not_in',
    'add', 'sub', 'and_', 'floordiv', 'div', 'inv', 'lshift', 'mod', 'mul', 'matmul',
    'neg', 'or_', 'pos', 'pow_', 'xor', 'concat', 'in_', 'countOf', 'delitem', 'getitem',
    'index', 'setitem', 'attr', 'props', 'bind',
    # 'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imod', 'imul', 'imatmul', 'ior', 'ipow',
    # 'irshift', 'isub', 'idiv', 'ixor',
    'identity', 'when', 'always', 'if_else', 'all_', 'any_',
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
and_ = curry(lambda a, b: a and b)
or_ = curry(lambda a, b: a or b)

# Math

add = curry(_op.add)
sub = flip(_op.sub)
floordiv = flip(_op.floordiv)
div = flip(_op.truediv)
inv = _op.inv
lshift = flip(_op.lshift)
mod = flip(_op.mod)
mul = curry(_op.mul)
matmul = flip(_op.matmul)
neg = _op.neg
pos = _op.pos
pow_ = flip(_op.pow)
xor = curry(_op.xor)

# Sequence Base

concat = curry(_op.concat)
in_ = curry(_op.contains)
not_in = curry(lambda a, b: b not in a)
countOf = flip(_op.countOf)
delitem = flip(_op.delitem)
getitem = flip(_op.getitem)
setitem = curry(lambda d, key, value: _op.setitem(d, key, value))

attr = _op.attrgetter
props = _op.itemgetter
bind = _op.methodcaller

# iadd = flip(_op.iadd)
# iand = flip(_op.iand)
# iconcat = flip(_op.iconcat)
# ifloordiv = flip(_op.ifloordiv)
# ilshift = flip(_op.ilshift)
# imod = flip(_op.imod)
# imul = flip(_op.imul)
# imatmul = flip(_op.imatmul)
# ior = flip(_op.ior)
# ipow = flip(_op.ipow)
# irshift = flip(_op.irshift)
# isub = flip(_op.isub)
# idiv = flip(_op.itruediv)
# ixor = flip(_op.ixor)


# customs ==============================
@curry
def index(x, xs, start=0, end=None):
    try:
        return _op.indexOf(islice(xs, start, end), x)
    except ValueError:
        return None


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


@curry
def all_(funcs: Iterable[Callable[[Any], bool]], v):
    return all(map(lambda f: f(v), funcs))


@curry
def any_(funcs: Iterable[Callable[[Any], bool]], v):
    for f in funcs:
        if f(v):
            return True
    return False
