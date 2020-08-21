from ._curry import curry, _


@curry
def c1(a: int, b, c=1):
    return a, b, c


@curry
def c2(a, *args):
    r = (a,) + args
    return r


@curry
def c3(a, **kwargs):
    return a, kwargs


@curry
def c4(* , a=1, b=3, c):
    return a, b, c


def test_curry_args():
    assert c1(7, 3, _)(6) == (7, 3, 6)
    assert (7, 3, 6) == c1(7)(3, _)(6)
    assert (7, 3, 6) == c1(_, 3, 6)(7)
    assert (7, 3, 6) == c1(7, 3, _)(6)
    assert (7, 3, 6) == c1(7)(3, 6)
    assert (7, 3, 6) == c1(7, _, 6)(3)
    assert (7, 3, 6) == c1(7)(_, 6)(3)
    assert c1(7, _)(3) == (7, 3, 1)
    assert c1(c=6)(7, 3) == (7, 3, 6)
    assert (7, 3, 6) == c2(_, 3, 6)(7)
    assert (7, 3, 6) == c2(_, 3)(7, 6)
    assert (7, 3, 6) == c2(7, _, 6)(3)
    assert (7, 3, 6) == c2(7, _)(3, 6)


def test_curry_kw():
    assert (1, {'c': 3}) == c3(_, c=3)(1)
    assert c3(3, b=1) == c3(b=1)(3) == (3, {'b': 1})
    assert c3(_, b=3, d=4)(6) == (6, {'b': 3, 'd': 4})
    assert c3(_, b=3, d=4)(6, e=7) == (6, {'b': 3, 'd': 4, 'e': 7})
    assert c4(a=3)(c=5) == (3, 3, 5)
