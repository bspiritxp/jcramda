from .functions import *


def test_applyto():
    action = lambda x, y: x + y
    assert applyto(3, 4)(action) == 7


def test_call_util():
    assert call_until(lambda x: x > 10,
                      (lambda x: x*2, lambda x: x*5+1, lambda x: x * 1e2))(2) == 11
    assert call_until(lambda x: x > 10,
                      (lambda x, y: x*y, pow, lambda x, y: x * y * 1e1))(2, 5) == 32
