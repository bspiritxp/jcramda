import itertools as its
from jcramda.core import *


def test_map_and_of():
    assert (1, 2, 3) == of(1, 2, 3)
    assert (1, 1, 1) == of(its.repeat(1, 3))
    assert ((1, 1, 1),) == of(((1, 1, 1),))
    assert (2, 4, 6) == mapof(lambda x: x*2)([1, 2, 3])
    assert [10, 14, 18] == list(map_(lambda x, y: (x+y)*2)([1, 2, 3], [4, 5, 6]))
    assert [2, 4, 6] == list(map_(lambda x: x*2)((1, 2, 3)))
    assert [1, 3, 5] == list(fmap(lambda x: [x])((1, 3, 5)))
    assert (1, 3, 5) == fmapof(lambda x: [x])((1, 3, 5))


def test_each():
    result = []

    def each_a(item):
        idx, value = item
        result.append(idx + value)

    foreach(each_a, enumerate((1, 2, 3)))
    assert [1, 3, 5] == result

    foreach(each_a)(enumerate((4, 5, 6)))
    assert [1, 3, 5, 4, 6, 8] == result


def test_chain():
    from jcramda.base.sequence import append
    from jcramda.core import add, pow_, floordiv, mul, sub, _
    assert chain((1, 2, 3), (4, 5, 6), (7, (8, 9))) == of(range(1, 10))
    assert of(chain((1, 2, 3), _)((4, 5))) == (1, 2, 3, 4, 5)
    assert of(chain(append, first)([1, 2, 3])) == (1, 2, 3, 1)
    # assert of(chain(append, first, [1, 2, 3])) == (1, 2, 3, 1)
    assert chain(pow_(2))(3, 4, 5) == (9, 16, 25)
    # assert chain(pow_(2), (3, 4, 5)) == (9, 16, 25)
    # append(head([1, 2, 3]), [1, 2, 3])
    # 3 ** (3 + 1) == 81
    assert chain(pow_, add(1))(3) == 81
    # ( 8 // ( 8 - 4 ) ) * 8
    assert chain(mul, floordiv, sub(4))(8) == 16


def test_filter():
    iterable = range(1, 100)
    assert of(filter_(None)([1, 2, 3, None, 4])) == (1, 2, 3, 4)
    assert of(filter_not(None)([1, 2, 3, None, 4])) == (None,)
    assert of(filter_not(lambda x: x > 90)(iterable)) == of(range(1, 91))
    assert of(filter_except(int, (TypeError, ValueError))(
        [1, 'a', '2', 0.5, None, {1}])) == (1, '2', 0.5)


def test_first():
    from itertools import count as _c
    assert first([1, 2, 3]) == 1
    assert first(_c(5)) == 5
    assert first('eaasdfasdf') == 'e'
    assert first(()) is None


def test_select():
    assert of(select([1, 0, 1, 1, 0])(range(1, 6))) == (1, 3, 4)
