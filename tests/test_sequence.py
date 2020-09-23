from jcramda.base.sequence import *


def test_drop():
    assert drop(3)('abcdefg') == 'defg'
    assert drop(2)([1, 2, 3, 4]) == [3, 4]
    assert drop(7, tuple(range(1, 6))) == ()


def test_adjacent():
    assert tuple(adjacent(lambda x: x == 3, range(6))) == \
           ((False, 0), (False, 1), (True, 2), (True, 3), (True, 4), (False, 5))
