from inspect import signature, Parameter, getfullargspec
from functools import wraps, partial

_ = Parameter.empty()


def has_default_value(p: Parameter):
    return p.default != Parameter.empty


def count_holder(fn):
    if isinstance(fn, partial) and len(fn.args) > 0:
        return len(list(filter(lambda x: x == _, fn.args)))
    return 0


def update_args(fn, args):
    arg_values = list(args)
    new_args = []
    func = fn
    if count_holder(fn):
        assert len(args), 'when _ in args, must pass a value to fill it'
        for a in fn.args:
            v = a
            if v == _ and len(arg_values) > 0:
                v = arg_values.pop(0)
            new_args.append(v)
        func = partial(fn.func, *new_args, **fn.keywords)
    return partial(func, *arg_values)


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
    return [0, len(spec.args)][bool(spec.args)] == len(filled_args) and not count_holder(fn)


# def move_kw_to_pos(spec, args, kwargs):
#     params = list(args)
#     if spec.args:
#         for index, key in enumerate(spec.args):
#             if key in kwargs:
#                 fix_count = index - len(params) - 1
#     return args


def curry(fn):
    @wraps(fn.func if hasattr(fn, 'func') else fn)
    def curried(*args, **kwargs):
        spec = getfullargspec(fn.func if hasattr(fn, 'func') else fn)
        # args = move_kw_to_pos(spec, args, kwargs)
        has_args = bool(spec.args) or bool(spec.varargs)
        # has_kw = bool(spec.kwonlyargs) or bool(spec.varkw)
        holders = count_holder(fn)
        updated_fn = update_args(fn, args) if has_args else fn
        updated_fn = partial(updated_fn, **kwargs) if len(kwargs) else updated_fn
        un_fill_params = list(signature(updated_fn).parameters.values())

        direct_run = not count_holder(updated_fn) and any([
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
        return curry(updated_fn)

    return curried
