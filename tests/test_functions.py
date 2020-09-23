from jcramda.base import *
from jcramda import concat, div


def test_applyto():
    action = lambda x, y: x + y
    assert applyto(3, 4)(action) == 7


def test_call_util():
    assert call_until(lambda x: x > 10,
                      (lambda x: x*2, lambda x: x*5+1, lambda x: x * 1e2))(2) == 11
    assert call_until(lambda x: x > 10,
                      (lambda x, y: x*y, pow, lambda x, y: x * y * 1e1))(2, 5) == 32


def test_juxt():
    assert tuple(juxt(lambda x: x+2, lambda x: x*2, lambda x: x-2)(6)) == (8, 12, 4)
    assert tuple(juxt(lambda x, y: x + y, lambda x, y: x * y, lambda x, y: x ** y)(3, 2)) == (5, 6, 9)


def test_converge():
    assert converge(div, [len, sum])(range(1, 8)) == 4
    assert converge(concat, [str.upper, str.lower])('Ladf') == 'LADFladf'
