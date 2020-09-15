from .sequence import *


def test_drop():
    assert drop(3)('abcdefg') == 'defg'
    assert drop(2)([1, 2, 3, 4]) == [3, 4]
    assert drop(7, tuple(range(1, 6))) == ()
