"""
Functions
"""
from typing import Callable, Any, Iterable, TypeVar, Union, Optional

_CT = TypeVar('_CT', covariant=True)
_CRT = TypeVar('_CRT', covariant=True)
_CF = Union[Callable[..., _CRT], _CRT]


def applyto(*args, **kwargs) -> Callable[[Callable], Any]: ...
def juxt(*funcs: Callable) -> Callable[[Any], Any]: ...
def call_until(pred: Callable[[Any], bool], funcs: Iterable[Callable],
               *args: Any, **kwargs: Any) -> _CF: ...
def f_digest(f: Callable) -> str: ...
def converge(after_f: Callable, funcs: Iterable[Callable], value: Any = ...) -> _CF: ...

def repeat_call(funcs: Iterable[Callable], times: Optional[int] = None, *args) -> _CF: ...

def pair_call(funcs: Iterable[Callable], *args) -> _CF: ...
def use_with(after_f: Callable, funcs: Iterable[Callable] = ..., *args) -> _CF: ...

