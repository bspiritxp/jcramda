from .mapping import *


def test_assign():
    assert {'a': 1, 'b': 3} == assign(dict(a=1), dict(b=3))
    assert {'a': 1, 'b': [{'c': 3}]} == assign(dict(a=1), dict(b=[dict(c=3)]))


def test_mstrip():
    assert {'a': 1} == strip_none({'a': 1, 'b': None})
    assert {'a': 1} == strip_empty({'a': 1, 'b': []})


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
