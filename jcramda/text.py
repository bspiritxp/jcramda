from typing import Iterable, AnyStr
from .core import (
    curry, bind
)

__all__ = (
    'capitalize', 'casefold', 'center', 'encode', 'endswith', 'expandtabs', 'find',
    'format_map', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier',
    'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join',
    'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust',
    'rpartition', 'rsplit', 'rstrip', 'scount', 'sformat', 'split', 'splitlines', 'startswith',
    'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill',
)

# string method curried ========================================


@curry
def replace(old_str, new_str, s, _count=-1):
    return s.replace(old_str, new_str, count=_count)


@curry
def startswith(prefix, s: str, start=None, end=None):
    return s.startswith(prefix, start, end)


@curry
def endswith(suffix, s: str, start=None, end=None):
    return s.endswith(suffix, start, end)


@curry
def sformat(template: str, s, *args, **kwargs):
    return template.format(s, *args, **kwargs)


@curry
def strip(s: str, chars=None):
    return s.strip(chars)


@curry
def lstrip(s: str, chars=None):
    return s.lstrip(chars)


@curry
def rstrip(s: str, chars=None):
    return s.rstrip(chars)


@curry
def scount(sub, s: str, start=None, end=None):
    return s.count(sub, start, end)


@curry
def encode(encoding, s: str, errors='ignore'):
    return s.encode(encoding, errors)


@curry
def expandtabs(tab_size, s: str):
    return s.expandtabs(tab_size)


@curry
def find(sub, s: str, start=None, end=None):
    return s.find(sub, start, end)


@curry
def rfind(sub, s: str, start=None, end=None):
    return s.rfind(sub, start, end)


@curry
def join(sep: str, seqs: Iterable) -> str:
    return sep.join([str(x) for x in seqs if x is not None])


@curry
def ljust(width, s: str, fillchar=None):
    return s.ljust(width, fillchar)


@curry
def rjust(width, s: str, fillchar=None):
    return s.rjust(width, fillchar)


@curry
def translate(opts: dict, s: str):
    return s.translate(str.maketrans(opts))


@curry
def rindex(sub, s: str, start=None, end=None):
    return s.rindex(sub, start, end)


@curry
def split(sep, s: str, limit=None):
    return s.split(sep, limit)


@curry
def rsplit(sep, s: str, limit=None):
    return s.rsplit(sep, limit)


lower = bind('lower')
upper = bind('upper')
capitalize = bind('capitalize')
casefold = bind('casefold')
center = bind('center')
format_map = curry(lambda mapping, s: s.format_map(mapping))
isalnum = bind('isalnum')
isalpha = bind('isalpha')
isascii = bind('isascii')
isdecimal = bind('isdecimal')
isdigit = bind('isdigit')
isidentifier = bind('isidentifier')
islower = bind('islower')
isnumeric = bind('isnumeric')
isprintable = bind('isprintable')
isspace = bind('isspace')
istitle = bind('istitle')
isupper = bind('isupper')
partition = curry(lambda sep, s: s.partition(sep))
rpartition = curry(lambda sep, s: s.rpartition(sep))
splitlines = bind('splitlines')
swapcase = bind('swapcase')
title = bind('title')
zfill = curry(lambda length, s: s.zfill(length))


# custom =======================================================
def hex_token(size):
    from secrets import token_hex
    return token_hex(size)


def url_safe_token(size):
    from secrets import token_urlsafe
    return token_urlsafe(size)


def hex_uuid():
    from uuid import uuid4
    return uuid4().hex


def camelcase(s: AnyStr):
    pass
