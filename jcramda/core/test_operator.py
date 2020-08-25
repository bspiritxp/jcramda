from ._curry import _
from .operator import *


def test_identity():
    assert 1 == identity(1)
    assert 2 == identity(lambda : 2)
    assert 4 == identity(pow_(2), 2)
    assert 4 == identity(pow_, _)(2, 2)


def test_when():
    cases = when([
        (eq(0), add(3)),
        (ge(3), pow_(2)),
        (is_a(str), lambda s: f'{s}ok')
    ], 0)
    assert 3 == cases(0)
    assert 16 == cases(4)
    assert 'test ok' == cases('test ')
    assert 0 == cases(b'fff')


def test_if_else():
    stmt = if_else((
        eq(8),
        pow_(2),
        add(3)
    ))
    assert 64 == stmt(8)
    assert 8 == stmt(5)

