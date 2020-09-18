from typing import (
    Callable, Any, Union, TypeVar, Iterable, Sequence, Tuple,
    Optional, List, DefaultDict, overload
    )

T = TypeVar('T')
KT = TypeVar('KT')
VT = TypeVar('VT')
RT = TypeVar('RT')


# chain((1, 2, 3), [4, 5, (6, 7)]) -> (1, 2, 3, 4, 5, 6, 7)
# chain(append, first)([1, 2, 3]) -> (1, 2, 3, 1)
@overload
def chain(*funcs: Callable) -> Callable[[Iterable[VT]], Tuple[VT]]: ...

@overload
def chain(*iterable: Iterable[VT]) -> Tuple[VT]: ...

@overload
def chain(*funcs: Callable, iterable: Iterable[VT] = ...): ...


# combine(range(4), 3) --> (0,1,2), (0,1,3), (0,2,3), (1,2,3)
def combine(seqs: Iterable[Iterable], r: int = ...) -> Union[Tuple[Tuple], Callable]: ...


def count(f: Callable[[int], Any],
          end: Union[int, Callable[[int, Any], bool]],
          start: int = 0, step: int = 1): ...


def filter_(f: Callable[[], bool], iterable: Iterable): ...

def filter_not(f: Callable[[], bool], iterable: Iterable): ...

def filter_except(f: Callable[[], bool], exceptions: Iterable[Exception],
                  iterable: Iterable): ...

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
    -> Iterable[Tuple[KT, Iterable[VT]]]: ...

def ireplace(f: Callable[[], bool], sub: RT, iterable: Iterable[VT],
             _count: Optional[int] = ..., window_size: int = 1) -> Iterable[Union[VT, RT]]: ...

# functional of slice: iterable[1::2]
def islice(rng: Union[int, tuple], iterable: Iterable[VT]) -> Iterable[VT]: ...

def last(iterable: Iterable[VT]) -> VT: ...

def map_(f: Callable[[VT], RT], *iterable: Iterable[VT]) -> Iterable[RT]: ...

def mapof(f: Callable[[VT], RT], *iterable: Iterable[VT]) -> Tuple[RT]: ...

def map_except(f: Callable[[VT], RT], exceptions: Iterable[Exception],
               iterable: Iterable[VT]) -> Iterable[RT]: ...

def map_reduce(key: Callable[[VT], KT], iterable: Iterable[VT],
               emit: Optional[Callable[[VT], RT]],
               reducer: Optional[Callable[[Tuple[RT]], T]]
               ) -> DefaultDict[KT, List[Union[RT, T]]]: ...

def of(*iterable: Union[Iterable[VT], VT],
       cls=Callable[[Iterable[VT]], Sequence[VT]]): ...



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
def select(selector: Iterable[Union[bool, int]], iterable: Iterable): ...

def zip_(fill_value: VT, *iterable: Iterable) -> Iterable[Tuple]: ...
