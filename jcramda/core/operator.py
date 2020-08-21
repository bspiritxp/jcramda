import operator as _op
from . import curry


__all__ = (
    'lt', 'le', 'eq', 'ne', 'ge', 'gt', 'not_', 'truth', 'is_', 'is_not', 'is_a', 'is_not_a',
    'add', 'sub', 'and_', 'floordiv', 'div', 'inv', 'lshift', 'mod', 'mul', 'matmul',
    'neg', 'or_', 'pos', 'pow_', 'xor', 'concat', 'contains', 'countOf', 'delitem', 'getitem',
    'indexOf', 'setitem', 'attr', 'props', 'bind','iadd', 'iand', 'iconcat', 'ifloordiv', 
    'ilshift', 'imod', 'imul', 'imatmul', 'ior', 'ipow', 'irshift', 'isub', 'idiv', 'ixor',      
)

# Comparison ===========================

lt = curry(_op.lt)
le = curry(_op.le)
eq = curry(_op.eq)
ne = curry(_op.ne)
ge = curry(_op.ge)
gt = curry(_op.gt)


# Logical ===============================

not_ = _op.not_
truth = _op.truth
is_ = curry(_op.is_)
is_not = curry(_op.is_not)
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


iadd        = curry(_op.iadd)
iand        = curry(_op.iand)
iconcat     = curry(_op.iconcat)
ifloordiv   = curry(_op.ifloordiv)
ilshift     = curry(_op.ilshift)
imod        = curry(_op.imod)
imul        = curry(_op.imul)
imatmul     = curry(_op.imatmul)
ior         = curry(_op.ior)
ipow        = curry(_op.ipow)
irshift     = curry(_op.irshift)
isub        = curry(_op.isub)
idiv        = curry(_op.itruediv)
ixor        = curry(_op.ixor)
