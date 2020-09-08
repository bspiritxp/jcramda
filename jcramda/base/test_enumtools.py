from enum import Enum

from jcramda.base.enumtools import *


class DA(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    f = 6


def test_members():
    assert tuple(members(DA)) == (DA.A, DA.B, DA.C, DA.D, DA.f)


def test_of():
    assert valueof(2, DA) == DA.B
    assert valueof(1)(DA) == DA.A
    assert valueof(5)(DA) is None
    assert nameof('C')(DA) == DA.C
    assert nameof('D', DA) == DA.D
    assert nameof('E')(DA) is None


def test_index_of():
    assert e_index_of(DA.C)(DA) == 2
    assert e_index_by(3)(DA) == DA.D


def test_get():
    assert enum_value(DA.A) == 1
    assert enum_name(DA.B) == 'B'
    assert enum_name('a') == 'a'
    assert enum_value(123) == 123
