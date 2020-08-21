"""
Ramda mapping functions
"""
from typing import Mapping
from ._curry import curry


@curry
def prop(prop_name: str, mapper: Mapping):
    result = mapper
    for key in prop_name.split('.'):
        result = result[key]
    return result


@curry
def propOr(prop_name, default, mapper: Mapping):
    result = mapper
    for key in prop_name.split('.'):
        if result is None:
            break
        result = result.get(key)
    return result


@curry
def loc(prop_name, mapper: Mapping):
    return propOr(prop_name, None, mapper)
