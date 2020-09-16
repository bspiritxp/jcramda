from inspect import signature, Parameter, getfullargspec, FullArgSpec
from functools import wraps, partial
from typing import Callable, List


__all__ = (
    'EmptyParam',
    'curry',
    'flip',
    'is_curried',
    '_',
)


EmptyParam = Parameter.empty
_ = EmptyParam


def has_default_value(p: Parameter):
    return p.default is not Parameter.empty


def _count_holder(fn):
    if isinstance(fn, partial) and len(fn.args) > 0:
        return len(list(filter(lambda x: x is EmptyParam, fn.args)))
    return 0


def _count_args(spec: FullArgSpec):
    return len(spec.args) + len(spec.kwonlyargs)


def update_args(fn, *args, **kws):
    arg_values = list(args)
    new_args = []
    func = fn
    if _count_holder(fn):
        assert len(args), 'when _ in args, must pass a value to fill it'
        kws.update(fn.keywords)
        for v in fn.args:
            if v is _ and len(arg_values) > 0:
                v = arg_values.pop(0)
            new_args.append(v)
        return partial(fn.func, *(new_args + arg_values), **kws)
    return partial(func, *arg_values, **kws) if len(arg_values) > 0 or len(kws) > 0 else func


def is_filled(fn, spec):
    if bool(spec.varargs):
        return False
    filled_args = ()
    func = fn
    while isinstance(func, partial):
        filled_args += func.args
        for key in func.keywords:
            if key in spec.args:
                filled_args += (func.keywords[key],)
        func = func.func
    return [0, len(spec.args)][bool(spec.args)] == len(filled_args) and not _count_holder(fn)


def _get_params(fn) -> List[Parameter]:
    return list(filter(lambda p: p.kind not in (p.VAR_KEYWORD, p.VAR_POSITIONAL),
                       signature(fn).parameters.values()))


def _no_fill_params(params: List[Parameter]):
    return len(list(filter(lambda p: p.default is p.empty, params)))


def _all_curry(fn):
    """
    * 废弃
    :param fn:
    :return:
    """
    @wraps(fn.func if hasattr(fn, 'func') else fn)
    def curried(*args, **kwargs):
        spec = getfullargspec(fn.func if hasattr(fn, 'func') else fn)
        # args = move_kw_to_pos(spec, args, kwargs)
        has_args = bool(spec.args) or bool(spec.varargs)
        # has_kw = bool(spec.kwonlyargs) or bool(spec.varkw)
        holders = _count_holder(fn)
        updated_fn = update_args(fn, *args) if has_args else fn
        updated_fn = partial(updated_fn, **kwargs) if len(kwargs) else updated_fn
        un_fill_params = _get_params(updated_fn)

        direct_run = not _count_holder(updated_fn) and any([
            # 没有需要填充的参数
            len(un_fill_params) == 0,
            not bool(spec.kwonlyargs) and is_filled(updated_fn, spec),
            # 所有未填充的参数都有默认值，且此次调用未传入参数
            all(map(has_default_value, un_fill_params)) and len(args) - holders <= 0,
            # 带占位符或位置参数都已填充时，剩余参数 ALL IS 动态参数
            holders and all(map(lambda p: p.kind in (
                Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD), un_fill_params))
        ])
        if direct_run:
            return updated_fn()
        return _all_curry(updated_fn)

    return curried


def _simple_curry(fn):
    @wraps(fn)
    def curried(*args, **kwargs):
        updated_fn = update_args(fn, *args, **kwargs)
        params = _get_params(updated_fn)
        can_run = all([
            _count_holder(updated_fn) == 0,
            _no_fill_params(params) == 0,
        ])
        return updated_fn() if can_run else _simple_curry(updated_fn)
    curried.__curried__ = True
    return curried


def _proxy_curry(fn: Callable):
    spec = getfullargspec(fn)
    # 只有一个参数或者没有参数时：返回方法本身
    if not (_count_args(spec) > 1 or spec.varargs or spec.varkw):
        return fn
    return _simple_curry(fn)


curry = _proxy_curry


def is_curried(f):
    return hasattr(f, '__curried__') and f.__curried__


def flip(f):
    """
    反转一个【双参数】方法的参数位置

    ps: 如果需要修改多参数方法的位置，请使用 `_` 占位符
    :param f:
    :return:
    """
    @curry
    @wraps(f)
    def flipped(a, b, *args, **kwargs):
        return f(b, a, *args, **kwargs)
    flipped.__doc__ = f'**fliped two params on head**\n{flipped.__doc__}'
    return flipped
