import itertools as its
from .itertools import *
from ._curry import _, flip


def test_map_and_of():
    assert (1, 2, 3) == of(1, 2, 3)
    assert (1, 1, 1) == of(its.repeat(1, 3))
    assert ((1, 1, 1),) == of(((1, 1, 1),))
    assert (2, 4, 6) == mapof(lambda x: x*2)([1, 2, 3])
    assert [10, 14, 18] == list(maps(lambda x, y: (x+y)*2)([1, 2, 3], [4, 5, 6]))
    assert [2, 4, 6] == list(maps(lambda x: x*2)((1, 2, 3)))
    assert [1, 3, 5] == list(fmap(lambda x: [x])((1, 3, 5)))
    assert (1, 3, 5) == fmapof(lambda x: [x])((1, 3, 5))


def test_each():
    result = []

    def each_a(item):
        idx, value = item
        result.append(idx + value)

    foreach(each_a, enumerate((1, 2, 3)))
    assert [1, 3, 5] == result


def test_chain():
    from jcramda.base.sequence import append
    from .operator import add, pow_, floordiv, mul, sub
    assert chain((1, 2, 3), (4, 5, 6), (7, (8, 9))) == of(range(1, 10))
    assert of(chain(append, first, [1, 2, 3])) == (1, 2, 3, 1)
    assert of(chain(pow_(2))((1, 2, 3, 4))) == (1, 4, 9, 16)
    # append(head([1, 2, 3]), [1, 2, 3])
    # 3 ** (3 + 1) == 81
    assert chain(pow_, add(1), 3) == 81
    # ( 8 // ( 8 - 4 ) ) * 8
    assert chain(mul, flip(floordiv), sub(_, 4))(8) == 16
