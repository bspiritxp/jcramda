"""
Ramda mapping functions
"""
from typing import Iterable, Union, Any, Mapping
from .core import curry


__all__ = (
    'prop',
    'propor',
    'loc',
    'obj',
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


def obj(keys: Union[str, Iterable[Any]], values):
    if isinstance(keys, str):
        return {keys: values}
    return dict(zip(keys, values))
