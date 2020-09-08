from ..core import co, curry


__all__ = (
    'applyto',
    'juxt',
    'call_until',
    'func_digest',
)


class applyto:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kw = kwargs

    def __call__(self, fn):
        return fn(*self._args, **self._kw)


@curry
def juxt(funcs, _value):
    """
    call some functions with a same param value.
    :param funcs:
    :param _value:
    :return: a list with functions call result
    """
    return map(applyto(_value), funcs)


@curry
def call_until(pred, funcs, v, *args, **kwargs):
    for func in funcs:
        r = func(v, *args, **kwargs)
        if pred(r):
            return r
    return None


def func_digest(f):
    from inspect import signature
    from pickle import dumps
    from .text import hexdigest
    return hexdigest('sha256', dumps(signature(f)))
