from jcramda.core import (identity, pow_, _, add, sub, floordiv, div, mod, mul, or_, and_, not_,
                          truth, is_, is_a, not_a, concat, in_, not_in, countof, getitem, index,
                          attr, props, bind, when, eq, ge, if_else, always, combine, of)


def test_identity():
    assert 1 == identity(1)
    assert 2 == identity(lambda : 2)
    assert 4 == identity(pow_(2), 2)
    assert 4 == identity(pow_, _)(2, 2)


def test_combine():
    assert of(combine(range(4), 3)) == ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
    assert of(combine((1, 2, 3))(2)) == ((1, 2), (1, 3), (2, 3))


def test_when():
    cases = when(
        (eq(0), add(3)),
        (ge(3), pow_(2)),
        (is_a(str), lambda s: f'{s}ok'),
        else_=0)
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


def test_always():
    assert 1 == always(1, 3)
    assert 'b' == always('b', 'a')


def test_base():
    assert add(3, 4) == add(3)(4) == 7
    assert sub(2, 8) == sub(2)(8) == sub(_, 8)(2) == 6
    assert floordiv(2, 5) == floordiv(2)(5) == floordiv(_, 5)(2) == 2
    assert div(2, 4) == div(2)(4) == div(_, 4)(2) == 2
    assert mod(3, 10) == mod(_, 10)(3) == mod(3)(10) == 1
    assert mul(2, 3) == mul(2)(3) == 6
    assert or_(True)(False) is True
    assert and_(True)(False) is False
    assert not_(True) is False
    assert truth([]) is False
    assert is_(True)(True)
    assert is_a((int, float))(3.1)
    assert is_a(int)(3)
    assert not_a((int, float))('a')
    assert not_a(int)('a')


def test_seq():
    assert concat((1, 2, 3))((4, 5)) == (1, 2, 3, 4, 5)
    assert concat('abc')('def', 'g') == 'abcdefg'
    assert in_(_, 3)((1, 2, 3,)) == in_((1, 2, 3))(3)
    assert not_in(_, 3)((1, 2, 4)) == not_in((1, 2, 4))(3)
    assert countof(3)((1, 2, 3)) == 1
    assert getitem(3)((1, 2, 3, 4)) == 4
    assert index(3)((3, 2, 1, 3)) == 0


def test_getter():
    class TestObj:
        pass
    tobj = TestObj()
    tobj.testattr = 1
    tobj.chain = TestObj()
    tobj.chain.t = 2
    assert attr('testattr')(tobj) == 1
    assert attr('chain.t')(tobj) == 2
    assert props('a', 'b')({'a': 4, 'b': 5}) == (4, 5)
    assert props('b', 'a')({'a': 4, 'b': 5}) == (5, 4)


def test_bind():
    assert bind('lower')('AbD') == 'abd'
    assert bind('replace', 'b', 'f')('fabsdfff') == 'fafsdfff'

