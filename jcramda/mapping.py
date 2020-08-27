"""
Ramda mapping functions
"""
from typing import Iterable, Union, Any, Mapping, MutableMapping
from .core import curry, delitem, props

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
)


@curry
def prop(prop_name: str, mapper: Mapping):
    result = mapper
    for key in prop_name.split('.'):
        result = result[key]
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
    return propor(prop_name, None, mapper)


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


map_with_keys = curry(lambda func, _keys, mapper: map(func, de(_keys, mapper)))


@curry
def remove(_keys: Iterable, mapper: MutableMapping):
    each_keys(delitem, _keys, mapper)
    return mapper
