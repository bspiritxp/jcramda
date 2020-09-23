from jcramda.base import join
from jcramda.core import repeat, co, _
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
    assert {'a': 1, 'c': ({'d': 5}, {'e': 6})} == flat_concat(dict(a=1), [1, 2, 3],
                                                              dict(c=({'d': 5}, {'e': 6})))
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
    assert prop('d.x', default='foo')(d) == 'foo'
    assert loc(2)(d) == 3
    assert loc(5, d) is None


def test_obj():
    assert obj('foo', 'bar') == dict(foo='bar')
    assert obj(('a', 'b', 'c'))({1, 2, 3}) == dict(a=1, b=2, c=3)
    assert obj(('a', 'b', 'c'), (1, 2, {4, 5})) == dict(a=1, b=2, c={4, 5})


def test_de():
    assert des(('a', 'b'))(dict(a=1, b=2, c=3)) == (1, 2)
    assert des(('a', 'd'), dict(a=1, b=2, c=3)) == (1, None)
    assert des(('a', 'b', 'c'))(dict(a=1, b=2, c=[4, 5])) == (1, 2, [4, 5])
    assert des(('a', 'd', 'b'))(dict(a=1, b=3)) == (1, None, 3)


def test_pick():
    assert pickall(('a', 'b'))(dict(a=1, b=2, c=3)) == {'a': 1, 'b': 2}
    assert pick(('a', 'b'))(dict(a=1, b=2, c=3)) == {'a': 1, 'b': 2}
    assert pickall(('a', 'd'))(dict(a=1, b=2, c=3)) == {'a': 1, 'd': None}
    assert pick(('a', 'd'))(dict(a=1, b=2, c=3)) == {'a': 1}
    assert pickall(('a', 'b', 'c'))(dict(a=1, b=2, c=[4, 5], d=6)) == {'a': 1, 'b': 2, 'c': [4, 5]}
    assert pick(('a', 'b', 'c'))(dict(a=1, b=2, c=[4, 5], d=6)) == {'a': 1, 'b': 2, 'c': [4, 5]}
    assert pickall(('a', 'd', 'b'))(dict(a=1, b=3)) == {'a': 1, 'd': None, 'b': 3}
    assert pick(('a', 'd', 'b'))(dict(a=1, b=3)) == {'a': 1, 'b': 3}


def test_key_map():
    raw = dict(a=1, b=2, c=3)
    assert key_map(co(join(''), repeat(2)))(raw) == dict(aa=1, bb=2, cc=3)


def test_map_update():
    test_dict = {'a': 2}
    assert map_update(lambda item: {item[0]: item[1] * 2}, {}, firstitem(test_dict)) == {'a': 4}


def test_obj_zip():
    assert obj_zip(('a', 'b', 'c'))((1, 2, 3)) == {'a': 1, 'b': 2, 'c': 3}
    assert obj_zip(_, (4, 5, 6))(('b', 'c', 'd')) == {'b': 4, 'c': 5, 'd': 6}


def test_invert():
    assert invert({'a': 1, 'b': 2}) == {1: 'a', 2: 'b'}
    assert invert({'a': 1, 'b': 2, 'c': 1}) == {1: ('a', 'c'), 2: 'b'}


def test_key_tree():
    assert key_tree({'a': 1, 'b': 2}) == ['a', 'b']
    assert key_tree({'a': 1, 'b': {'c': 3}}) == ['a', 'b', 'b.c']
    assert key_tree({'a': 1, 'b': {'c': [1, {'d': 5}]}}) \
        == ['a', 'b', 'b.c', 'b.c.0', 'b.c.1', 'b.c.1.d']


def test_path():
    assert path('a', {'a': 1}) == 1
    assert path('a')({'b': 3}) is None
    assert path('a.b')({'a': {'b': 3}}) == 3
    assert path(('a', 1, 'b'))({'a': [1, {'b': 4}]}) == 4
    assert path('a.1.b')({'a': [1, {'b': 4}]}) == 4

    assert path_eq('a.1.b', 4)(dict(a=[1, {'b': 4}]))
    assert not path_eq('a.b', 1, {'a': {'c': 1}})
    assert path_eq('a.1.b', lambda x: x % 2 == 0, {'a': [1, {'b': 4}]})
