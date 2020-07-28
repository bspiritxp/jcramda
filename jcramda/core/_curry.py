from inspect import signature, Parameter, getfullargspec
from functools import wraps, partial

_ = Parameter.empty()


def has_default_value(p: Parameter):
    return p.default != Parameter.empty


def has_holder(fn, pos: int = None):
    if isinstance(fn, partial) and len(fn.args) > 0:
        assert pos is None or [pos, abs(pos) - 1][pos < 0] < len(fn.args), \
            'checked position is out of bound'
        return _ in fn.args if pos is None else fn.args[pos] == _
    return False


def update_args(fn, args):
    arg_values = list(args)
    new_args = []
    func = fn
    if has_holder(fn):
        assert len(args), 'when _ in args, must pass a value to fill it'
        for a in fn.args:
            v = a
            if v == _ and len(arg_values) > 0:
                v = arg_values.pop(0)
            new_args.append(v)
        func = partial(fn.func, *new_args, **fn.keywords)
    return partial(func, *arg_values)


def curry(fn):
    @wraps(fn.func if hasattr(fn, 'func') else fn)
    def curried(*args, **kwargs):
        spec = getfullargspec(fn.func if hasattr(fn, 'func') else fn)
        has_args = bool(spec.args) or bool(spec.varargs)
        has_kws = bool(spec.kwonlyargs) or bool(spec.varkw)
        if has_args and len(args) + len(kwargs) == 0:
            return fn(*args, **kwargs)
        if has_kws and len(kwargs) == 0:
            return fn(**kwargs)
        last_is_holder = has_holder(fn, -1)
        updated_fn = update_args(fn, args) if has_args and len(
            args) else fn
        updated_fn = partial(updated_fn, **kwargs) if len(kwargs) else updated_fn
        un_fill_params = list(signature(updated_fn).parameters.values())

        direct_run = not has_holder(updated_fn) and (
                len(un_fill_params) == 0 or all(map(has_default_value, un_fill_params))
                or last_is_holder and all(map(lambda p: p.kind in (
                    Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD), un_fill_params))
        )
        if direct_run:
            return updated_fn()
        return curry(updated_fn)

    return curried
