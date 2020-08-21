from typing import Callable


def compose(*funcs: Callable):
    funcs = list(funcs)

    def composed_func(*args, **kwargs):
        fn = funcs.pop()
        result = fn(*args, **kwargs)
        while len(funcs):
            result = funcs.pop()(result)
        return result

    return composed_func


co = compose


def pipe(*funcs: Callable):
    return compose(*reversed(funcs))
