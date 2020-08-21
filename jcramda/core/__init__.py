from functools import partial, reduce
from ._curry import curry, _
from .compose import compose, co, pipe
from .operator import *


__all__ = (
    'curry',
    '_',
    'compose',
    'co',
    'partial',
    'reduce',
)
