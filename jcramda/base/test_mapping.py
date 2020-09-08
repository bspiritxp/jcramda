from jcramda import co, join
from jcramda.core.itertools import repeat
from jcramda.base.mapping import *


def test_assign():
    assert {'a': 1, 'b': 3} == assign(dict(a=1), dict(b=3))
    assert {'a': 1, 'b': [{'c': 3}]} == assign(dict(a=1), dict(b=[dict(c=3)]))


def test_mstrip():
    assert {'a': 1, 'c': []} == strip_none({'a': 1, 'b': None, 'c': []})
    assert {'a': 1} == strip_empty({'a': 1, 'b': [], 'c': None})


def test_flat_concat():
    assert {'a': 1} == flat_concat({'a': 1, 'b': None})
    assert {'a': 1} == flat_concat({'a': 1, 'b': []})
    assert {'a': 1, 'b': ({'c': 3},)} == flat_concat({'a': 1}, b=[{'c': 3, 'd': None}])
    assert {'a': 1, 'b': {'c': 3}} == flat_concat(dict(a=1), b={'c': 3, 'd': ()})
    assert {'a': 1, 'c': ({'d': 5}, {'e': 6})} == flat_concat(dict(a=1), [1,2,3], dict(c=({'d': 5}, {'e': 6})))
    assert flat_concat(a=1, c=6) == {'a': 1, 'c': 6}
    assert flat_concat(1, [1, 2]) == (1, 2)
    assert flat_concat(1, 'a') == {1, 'a'}
    from collections import OrderedDict
    assert flat_concat(OrderedDict(b=3, a=1, e=None)) == {'a': 1, 'b': 3}


def test_prop_loc():
    d = dict(a=1, b=2, c=3, d={'m': 'aa', 'n': 'bb'})
    assert prop('a')(d) == loc('a')(d) == 1
    assert prop('b', d) == loc('b', d) == 2
    assert prop('e', d) is None
    assert prop('d.m')(d) == 'aa'
    assert prop('d.n', d) == 'bb'
    assert prop('d.x', d) is None
    assert propor('d.x', 'foo')(d) == 'foo'
    assert loc(2)(d) == 3
    assert loc(5, d) is None


def test_obj():
    assert obj('foo', 'bar') == dict(foo='bar')
    assert obj(('a', 'b', 'c'))({1, 2, 3}) == dict(a=1, b=2, c=3)
    assert obj(('a', 'b', 'c'), (1, 2, {4, 5})) == dict(a=1, b=2, c={4, 5})


def test_de():
    assert de(('a', 'b'))(dict(a=1, b=2, c=3)) == (1, 2)
    assert de(('a', 'd'), dict(a=1, b=2, c=3)) == (1, )
    assert de(('a', 'b', 'c'))(dict(a=1, b=2, c=[4, 5])) == (1, 2, [4, 5])


def test_key_map():
    raw = dict(a=1, b=2, c=3)
    assert key_map(co(join(''), repeat(2)))(raw) == dict(aa=1, bb=2, cc=3)
