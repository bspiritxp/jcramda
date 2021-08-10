from enum import Enum
from typing import (
    Callable, Any, Union, TypeVar, Iterable, Sequence, Tuple,
    Optional, List, DefaultDict, overload, Type,
    Hashable, Mapping, Iterator)

T = TypeVar('T')
KT = TypeVar('KT')
VT = TypeVar('VT')
RT = TypeVar('RT')

OT = Optional[T]
NumberValue = Union[int, float]
_CT = TypeVar('_CT', covariant=True)
_CRT = TypeVar('_CRT', covariant=True)
CurriedF = Union[Callable[..., _CRT], _CRT]


"""
Curry
"""
from inspect import Parameter

_ = EmptyParam = Parameter.empty


def curry(fn: Callable) -> Callable: ...
def is_curried(f: Callable) -> bool: ...
def flip(f: Callable) -> Callable: ...

def compose(*fns: Callable) -> Callable: ...
co = compose

def pipe(*funcs: Callable) -> Callable: ...

def break_if(pred: Callable[..., bool], value: Any = ...) -> CurriedF: ...


"""
IterTools
"""
# chain((1, 2, 3), [4, 5, (6, 7)]) -> (1, 2, 3, 4, 5, 6, 7)
# chain(append, first)([1, 2, 3]) -> (1, 2, 3, 1)
@overload
def chain(*iterable: Iterable) -> CurriedF: ...

@overload
def chain(f1: Callable[[VT, T], RT], f2: Callable[[T], VT]) -> Callable[[Any], RT]: ...

@overload
def chain(*funcs: Callable) -> Callable[[Iterable], RT]: ...


# combine(range(4), 3) --> (0,1,2), (0,1,3), (0,2,3), (1,2,3)
def combine(seqs: Iterable, r: int = ...) -> CurriedF[T]: ...


def count(f: Callable[[int], Any],
          end: Union[int, Callable[[int, Any], bool]],
          start: int = 0, step: int = 1): ...

@overload
def filter_(f: Callable[[], bool], iterable: Iterable) -> Iterator: ...
@overload
def filter_(f: Callable[[], bool]) -> Callable[[Iterable], Iterator]: ...

def filter_not(f: Callable[[], bool], iterable: Iterable = ...) -> CurriedF: ...

@overload
def filter_of(f: Callable[[], bool], iterable: Iterable) -> Tuple: ...
@overload
def filter_of(f: Callable[[], bool]) -> Callable[[Iterable], Tuple]: ...
@overload
def filter_group(f: Callable[[], bool], iterable: Iterable) -> Tuple[Tuple, Tuple]: ...
@overload
def filter_group(f: Callable[[], bool]) -> Callable[[Iterable], Tuple[Tuple, Tuple]]: ...

def filter_except(f: Callable[[], bool], exceptions: Iterable[Exception],
                  iterable: Iterable = ...) -> CurriedF: ...
def some(pred: Callable[..., bool], iterable: Iterable = ...) -> CurriedF[bool]: ...

def first(iterable: Iterable[VT]) -> VT: ...

def flatten(*iterable: Iterable) -> Tuple: ...

@overload
def fmap(f: Callable[[], VT], iterable: Iterable[VT]) -> Iterable[VT]: ...

@overload
def fmap(f: Callable[[], VT]) -> Callable[[Iterable[VT]], Iterable[RT]]: ...

@overload
def fmapof(f: Callable[[], VT], iterable: Iterable[VT]) -> Tuple[VT]: ...

@overload
def fmapof(f: Callable[[], VT]) -> Callable[[Iterable[VT]], Tuple[RT]]: ...

def fold(f: Callable[[RT, VT], RT], init: RT, iterable: Iterable[VT]) -> RT: ...

def foreach(f: Callable, iterable: Iterable[VT] = ...,
            chunk_size: Optional[int] = None, before: Optional[Callable] = None,
            after: Optional[Callable] = None) \
        -> Union[Iterable[VT], Callable[[Any], Iterable[VT]]]: ...

def groupby(f: Callable[[VT], KT], iterable: Iterable[VT]) \
    -> Iterator[Tuple[KT, Iterable[VT]]]: ...

def ireplace(f: Callable[[], bool], sub: RT, iterable: Iterable[VT],
             _count: Optional[int] = ..., window_size: int = 1) -> Iterator[Union[VT, RT]]: ...

# functional of slice: iterable[1::2]
def islice(rng: Union[int, tuple], iterable: Iterable[VT]) -> Iterator[VT]: ...

def last(iterable: Iterable[VT]) -> VT: ...

def map_(f: Callable[[VT], RT], iterable: Iterable[VT] = ...) -> CurriedF: ...

def mapof(f: Callable[[VT], RT], iterable: Iterable[VT] = ...) -> CurriedF: ...
@overload
def maps(func: Callable[..., RT], iterable: Iterable[Iterable[Any]]) -> Iterator[RT]: ...
@overload
def maps(func: Callable[..., RT]) \
    -> Callable[[Iterable[Iterable[Any]]], Iterator[RT]]: ...

def map_except(f: Callable[[VT], RT], exceptions: Iterable[Exception],
               iterable: Iterable[VT]) -> Iterable[RT]: ...

def map_reduce(key: Callable[[VT], KT], iterable: Iterable[VT],
               emit: Optional[Callable[[VT], RT]],
               reducer: Optional[Callable[[Tuple[RT]], T]]
               ) -> DefaultDict[KT, List[Union[RT, T]]]: ...

def of(*iterable: Union[Iterable, VT],
       cls=Callable[[Iterable[VT]], Sequence[VT]]) -> Iterable: ...

def one(iterable: Iterable[VT]) -> Union[Tuple[VT], VT]: ...
# 排列
def permute(iterable: Iterable[VT], r: int) -> Iterable[Tuple[VT]]: ...

# product((1,2), (3,4)) -> (1, 3), (1, 4), (2, 3), (2, 4)
def product(*iterable: Iterable[VT], r: int = 1) -> Iterable[Tuple[VT]]: ...

def product_map(f: Callable[[VT], RT], *iterable: Iterable[VT]) -> Iterable[RT]: ...

# repeat(3, 1) -> (1, 1, 1)
# repeat(None, 'x') -> ('x', 'x', 'x', .... ) // endless
def repeat(n: int, x: T) -> Iterable[T]: ...

def scan(f: Callable[[RT, VT], RT], init: RT,
         iterable: Iterable[VT]) -> Iterable[RT]: ...

# >>> select([1, 0, 1, 1, 0], range(1, 6)) -> iter(1, 3, 4)
@overload
def select(selector: Iterable[Union[bool, int]], iterable: Iterable[VT]) -> Iterator[VT]: ...
@overload
def select(selector: Iterable[Union[bool, int]]) -> Callable[[Iterable[VT]], Iterator[VT]]: ...

def zip_(fill_value: VT, *iterable: Iterable) -> Iterable[Tuple]: ...


"""
Operator
"""

def eq(a: OT, b: OT = ...) -> CurriedF[bool]: ...
def ne(a: OT, b: OT = ...) -> CurriedF[bool]: ...
def lt(a: T, b: T = ...) -> Union[Callable[[T], bool], bool]: ...
def le(a: T, b: T = ...) -> Union[Callable[[T], bool], bool]: ...
def ge(a: T, b: T = ...) -> Union[Callable[[T], bool], bool]: ...
def gt(a: T, b: T = ...) -> Union[Callable[[T], bool], bool]: ...
def eq_by(f: Callable[[T, T], bool], a: T = ..., b: T = ...) -> Union[Callable, bool]: ...

def cmp_range(rng: range, v: int = ...) -> Union[Callable[[int], int], int]: ...
def between(_min: T, _max: T = ..., v: T = ...) -> Union[Callable, bool]: ...
def clamp(_min: T, _max: T = ..., v: T = ...) -> Union[Callable, T]: ...
def not_(o: T) -> bool: ...
def truth(o: T) -> bool: ...
def false_(o: T) -> bool: ...
def is_(a: OT, b: OT = ...) -> Union[Callable[[OT], bool], bool]: ...
def is_not(a: OT, b: OT = ...) -> Union[Callable[[OT], bool], bool]: ...
def is_a(types: Union[Tuple[Type, ...], Type, None], o: T = ...) -> Union[Callable[[T], bool], bool]: ...
def not_a(types: Union[Tuple[Type, ...], Type, None], o: T = ...) -> CurriedF: ...
def is_none(o: OT) -> bool: ...
def not_none(o: OT) -> bool: ...
def and_(a: bool, b: bool = ...) -> CurriedF: ...
def or_(a: bool, b: bool = ...) -> CurriedF: ...

def add(a: _CT, b: _CT = ...) -> CurriedF: ...
# sub: b - a
def sub(a: _CT, b: _CT = ...) -> CurriedF: ...
# dec: a + 1
def dec(a: int) -> int: ...
# inc: a - 1
def inc(a: int) -> int: ...
# floordiv: floor(b / a)
def floordiv(a: T, b: T) -> CurriedF: ...
# div: b / a
def div(a: T, b: T = ...) -> CurriedF: ...
# inv: -a
def inv(a: T) -> T: ...
# lshift: a << b
def lshift(b: int, a: int = ...) -> CurriedF: ...
# mod(b, a) -> a % b
def mod(b: T, a: T = ...) -> CurriedF: ...
# mul(a, b) -> a * b
def mul(a: T, b: T = ...) -> CurriedF: ...
# matmul(a, b) -> a @ b
def matmul(a: T, b: T) -> T: ...
# neg(a) -> -a
def neg(a: T) -> T: ...
# pos(a) -> +a
def pos(a: T) -> T: ...
# pow(b, a) -> a ** b
def pow_(b: int, a: NumberValue = ...) -> CurriedF[NumberValue]: ...
# xor(a, b) -> a ^ b
def xor(a: T, b: T = ...) -> CurriedF[T]: ...
# concat( iter1, iter2, ..., itern) ->
def concat(a: _CT, b: _CT = ..., *args: _CT) -> CurriedF: ...
def round_down(limit: int, num: Union[int, float]) -> Union[int, float]: ...

def in_(iterable: Union[Iterable, Enum], x: Any = ...) -> CurriedF: ...
def not_in(iterable: Iterable, x: Any = ...) -> CurriedF: ...
def countof(x: Any, iterable: Iterable = ...) -> CurriedF: ...
def delitem(idx: Hashable, subable: Any = ...) -> CurriedF: ...
def getitem(idx: Hashable, subable: Any = ...) -> CurriedF: ...
def setitem(obj: Any, key: Hashable = ..., value: T = ...) -> CurriedF: ...
def attr(attr_name: str) -> Callable[[Any], RT]: ...
def props(prop_name: Hashable) -> Callable[[Mapping], RT]: ...
def bind(method_name: str, *args, **kwargs) -> Callable[[Any], RT]: ...

def index(x: T, xs: Iterable = ..., start: int = ..., end: Optional[int] = ...) -> CurriedF: ...
def indexall(x: T, xs: Iterable, start: int = ..., end: Optional[int] = ...): ...
def identity(f: Union[Callable[[Any], RT], T], *args: Any, **kw: Any) -> Union[T, RT]: ...
def when(*cases: Tuple[Callable[..., bool], Any], else_: Any =...): ...
def case(cases: dict, v: Any, default: Any=..., key: Callable = ...) -> Any: ...
def always(x: Any, _: Any = ...): ...
def if_else(pred: Callable[[T], bool], 
            success: Callable[[T], RT],
            failed: Callable[[T], RT],
            value: T = ...) -> CurriedF[RT]: ...
def try_catch(f: Callable, failed: Callable, value= ...) -> CurriedF: ...
def all_(funcs: Iterable[Callable[..., bool]], v= ...) -> CurriedF: ...
def any_(funcs: Iterable[Callable[..., bool]], v=...) -> CurriedF: ...
def all_pass(func: Callable[..., bool], iterable: Iterable) -> CurriedF[bool]: ...
def one_pass(func: Callable[..., bool], iterable: Iterable) -> CurriedF[bool]: ...
def default_to(df: Any, raw: Any = ...) -> CurriedF: ...
def import_(module_name: str, package: Optional[str] = ...): ...
def from_import_as(_name: str, from_module: str = ..., package: Optional[Any] = ...): ...
def eq_attr(attr_name: str, o1: Any = ..., o2: Any = ...) -> CurriedF: ...
def eq_prop(prop_name: Hashable, s1: Any = ..., s2: Any = ...) -> CurriedF: ...
def has_attr(attr_name: str, obj: T = ..., pred: Callable[..., bool]=...) -> CurriedF[bool]: ...
def else_to(else_f: Callable, raw: Any = ..., args: Tuple = ..., kwargs: dict = ...) -> CurriedF: ...
def chunk_map(func: Callable, size: int, it: Iterable) -> CurriedF: ...
