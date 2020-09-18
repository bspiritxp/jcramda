import hashlib
import re
from random import choices
from typing import Iterable, AnyStr
from jcramda.core import (curry, bind, co, chain, repeat, always, is_a)
from jcramda.base.sequence import update_range, split_before
from string import ascii_lowercase


__all__ = (
    'capitalize', 'casefold', 'center', 'encode', 'expandtabs', 'decode', 'find',
    'format_map', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier',
    'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join',
    'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust',
    'rpartition', 'rsplit', 'rstrip', 'scount', 'sformat', 'split', 'splitlines',
    'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill',
    # custom functions
    'first_lower', 'hex_token', 'url_safe_token', 'hex_uuid', 'camelcase', 'camelcase_to',
    'rand_txt', 'repeat_txt', 'mask', 'mask_except', 'hexdigest', 'b64_encode', 'b64_decode',
    'b64_urlsafe_encode', 'b64_urlsafe_decode',
)

# string method curried ========================================


@curry
def replace(old_str, new_str, s, _count=-1):
    return s.replace(old_str, new_str, count=_count)


@curry
def sformat(tmpl: str, s, *args, **kwargs):
    return tmpl.format(s, *args, **kwargs)


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
def scount(rs, s: str, start=None, end=None):
    return s.count(rs, start, end)


def encode(s: AnyStr, errors='ignore', encoding='utf8'):
    return s.encode(encoding, errors) if is_a(str, s) else s


def decode(bs: AnyStr):
    return bs.decode() if is_a(bytes, bs) else bs


@curry
def expandtabs(tab_size, s: str):
    return s.expandtabs(tab_size)


@curry
def find(rs, s: str, start=None, end=None):
    return s.find(rs, start, end)


@curry
def rfind(rs, s: str, start=None, end=None):
    return s.rfind(rs, start, end)


@curry
def join(sep: str, seqs: Iterable):
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
def split(sep, s: str, limit=-1):
    return s.split(sep, limit)


@curry
def rsplit(sep, s: str, limit=-1):
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
def first_lower(s: str):
    return s[0:1].lower() + s[1:]


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
    """
    下划线转换驼峰
    :param s:
    :return:
    """
    return co(
        first_lower,
        join(''),
        update_range(capitalize, start=1),
        split('_')
    )(s)


@curry
def camelcase_to(sep, s: AnyStr, trans_f=lower):
    return co(
        trans_f,
        join(sep),
        chain(join('')),
        split_before(isupper)
    )(s)


def rand_txt(length, char_set=ascii_lowercase):
    return join('')(choices(char_set, k=length))


@curry
def repeat_txt(n, sub):
    return join('', repeat(n, sub))


@curry
def mask(start, stop, raw: str, char='*'):
    return co(
        join(''),
        update_range(always(char), start=start, stop=stop)
    )(raw)


@curry
def mask_except(_head: int, _tail: int, s: str, char='*'):
    return s[0:_head] + repeat_txt(len(s) - _head - _tail, char) + s[-_tail:]


@curry
def hexdigest(algorithm, raw: AnyStr, length=32):
    """
    支持以下算法
    ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b',
     'blake2s', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'shake_128', 'shake_256')
    :param algorithm:
    :param raw:
    :param length:
    :return:
    """
    spec = bind(algorithm, encode(raw))
    try:
        return spec(hashlib).hexdigest()
    except AttributeError:
        raise RuntimeError(f'not supported algorithm: {algorithm}')
    except TypeError:
        return spec(hashlib).hexdigest(length)


def b64_encode(s: AnyStr):
    import base64
    return co(
        decode,
        base64.b64encode,
        encode,
    )(s)


def b64_urlsafe_encode(s: AnyStr):
    import base64
    return co(
        decode,
        base64.urlsafe_b64encode,
        encode,
    )(s)


def b64_decode(s: AnyStr):
    import base64
    return co(
        decode,
        base64.b64decode,
    )(s)


def b64_urlsafe_decode(s: AnyStr):
    import base64
    return co(
        decode,
        base64.urlsafe_b64decode,
    )(s)


search = curry(re.search)
match = curry(re.match)
fullmatch = curry(re.fullmatch)
sub = curry(re.sub)
subn = curry(re.sub)
finditer = curry(re.finditer)
findall = curry(re.findall)
regexp = re.compile
template = re.template
escape = re.escape


# HTML ====================
import html

htmlescape = html.escape
htmlunescape = html.unescape
