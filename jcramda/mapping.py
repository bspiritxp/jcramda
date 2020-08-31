"""
Ramda mapping functions
"""
from collections import OrderedDict
from typing import Iterable, Union, Any, Mapping, MutableMapping

from .core import curry, delitem, props, co, first, identity, fold, each, setitem, not_a, when, \
    not_none, filter_, maps, _, of, chain, all_, truth
from .comparison import is_a_dict, is_a_func, is_a_int, is_a_list, is_iter
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
    'd_merge',
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


def d_merge(*args: dict):
    return dict(zip(chain(map(keys, args)), chain(map(values, args))))


def flat_merge(*args, **kwargs):
    dicts = filter(all_([is_a_dict, truth]), args)
    lists = filter(all_([is_a_list, truth]), args)

    result = d_merge(*dicts, kwargs)

