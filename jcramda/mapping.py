"""
Ramda mapping functions
"""
from collections import OrderedDict
from typing import Iterable, Union, Any, Mapping, MutableMapping, Sequence

from .comparison import is_a_dict, is_a_func, is_a_int, is_iter, is_a_mapper, is_seq
from .core import (curry, delitem, props, co, first, fold, each, setitem, not_a, not_none, of,
                   truth, all_, truth, is_a)
from .sequence import nth

__all__ = (
    'prop',
    'propor',
    'loc',
    'obj',
    'keys',
    'values',
    'remove',
    'de',
    'map_with_keys',
    'map_update',
    'map_apply',
    'firstitem',
    'obj_zip',
    'update_path',
    'key_map',
    'trans_keys',
    'dpop',
    'sorted_by_key',
    'assign',
    'mstrip',
    'strip_none',
    'strip_empty',
    'flat_concat',
)

not_dict = not_a(dict)


@curry
def prop(prop_name: str, mapper: Mapping):
    result = mapper
    for key in prop_name.split('.'):
        result = result.get(key)
    return result


@curry
def propor(prop_name, default, mapper: Mapping):
    result = mapper
    for key in prop_name.split('.'):
        if result is None:
            break
        result = result.get(key, default)
    return result


@curry
def loc(prop_name, mapper: Mapping):
    if hasattr(mapper, 'get'):
        return mapper.get(prop_name)
    if hasattr(mapper, 'loc'):
        return mapper.loc[prop_name]
    if is_a_int(prop_name):
        return nth(prop_name)(mapper)


def obj(_keys: Union[str, Iterable[Any]], _values):
    if isinstance(_keys, str):
        return {_keys: _values}
    return dict(zip(_keys, _values))


def keys(mapper: Mapping):
    return mapper.keys()


def values(mapper: Mapping):
    return mapper.values()


@curry
def de(_keys: Iterable, mapper: Mapping):
    return props(*filter(lambda k: k in mapper, _keys))(mapper)


@curry
def each_keys(func, _keys, mapper):
    for key in _keys:
        if key in mapper:
            func(key)


@curry
def map_update(f, d, v):
    """

    :param f: (v) -> dict
    :param d: dict  updated dict
    :param v: a value
    :return: dict
    """
    d.update(f(v))
    return d


map_with_keys = curry(lambda func, _keys, mapper: map(func, de(_keys, mapper)))

# ( f: (x) -> dict, seqs: [x1, x2 ... xn] ) -> { **f(x1), **f(x2) ... **f(xn) }
map_apply = curry(lambda f, seqs: fold(map_update(f), {}, seqs))


@curry
def remove(_keys: Iterable, mapper: MutableMapping):
    each_keys(delitem, _keys, mapper)
    return mapper


# (d: dict) -> d.values()[0]
firstitem = co(first, values)

obj_zip = curry(lambda _ks, _vs: dict(zip(_ks, _vs)))


@curry
def update_path(_path: str, upset, d: MutableMapping):
    paths = reversed(_path.split('.'))
    new_value = upset(prop(_path, d)) if is_a_func(upset) else upset
    query = fold(lambda r, k: {k: r}, {paths[0]: new_value}, paths[1:])
    d.update(query)
    return d


@curry
def key_map(fn, d: Mapping):
    if not is_a_dict(d):
        return d
    r = {}
    each(lambda k: setitem(r, fn(k), d[k]), d.keys())
    return r


@curry
def trans_keys(key_fn, d, deep=False):
    if is_iter(d):
        result = [trans_keys(key_fn, item, deep) if is_a_dict(item) else item for item in d]
    elif is_a_dict(d):
        result = key_map(key_fn, d)
    else:
        return d

    if deep:
        for key in result:
            result[key] = trans_keys(key_fn, result[key], deep)

    return result


@curry
def dpop(key, d: MutableMapping):
    return d.pop(key)


@curry
def sorted_by_key(key_f, d, reverse=False):
    return OrderedDict(sorted(d.items(), key=key_f, reverse=reverse))


def assign(*args: dict):
    mappers = of(filter(is_a_dict, args))
    if not mappers:
        return {}
    return dict(zip(of(*map(keys, mappers)), of(*map(values, mappers))))


@curry
def mstrip(f, mapper: Mapping):
    return type(mapper)(filter(f, mapper.items()))


strip_none = mstrip(lambda item: not_none(item[1]))
strip_empty = mstrip(lambda item: truth(item[1]))


def flat_concat(*args, **kwargs):
    """ 平铺传入的字典
    如果传入参数中有Mapping，则只处理Mapping
    如果传入参数中没有Mapping，则会处理 Sequence[Mapping]
    否则什么都不处理
    :param args:
    :param kwargs:
    :return:
    """
    dicts = filter(all_([is_a_mapper, truth]), args)
    lists = of(*filter(all_([is_a((list, tuple)), truth]), args))

    merged = assign(*dicts, kwargs)
    if merged:
        return strip_empty(map_apply(
            lambda item: {item[0]:
                          flat_concat(item[1]) if is_a((Mapping, list, tuple), item[1]) else item[1]},
            merged.items()
        ))
    return of(map(lambda x: flat_concat(x)
                  if is_a((Mapping, list, tuple), x) else x, lists)) or {*filter(truth, args)}
