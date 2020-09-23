from typing import Any, Callable, Dict, Iterable, Mapping, MutableMapping, Union, Sequence, TypeVar, \
    Tuple, overload

KT = TypeVar('KT')
VT = TypeVar('VT')
_CT = TypeVar('_CT', covariant=True)
_CRT = TypeVar('_CRT', covariant=True)
CurriedF = Union[Callable[..., _CRT], _CRT]


def prop(prop_name: str, mapper: Mapping = ..., default: Any=...) -> CurriedF: ...
def loc(prop_name: str, mapper: Any = ...) -> CurriedF : ...
def obj(_keys: Union[str, Iterable[KT]], _values: Union[VT, Iterable[VT]] = ...) \
        -> CurriedF: ...
def keys(mapper: Mapping) -> Iterable: ...
def values(mapper: Mapping) -> Iterable: ...
def des(_keys: Iterable, mapper: Mapping = ...) -> CurriedF: ...
def pickall(_keys: Iterable, mapper: Mapping = ...) -> CurriedF: ...
def pick(_keys: Iterable, mapper: Mapping = ...) -> CurriedF: ...
def map_update(f: Callable, d: MutableMapping, v: Any): ...

def map_with_keys(f: Callable, _keys: Iterable, mapper: Mapping = ...) -> CurriedF: ...
def map_apply(f: Callable, seqs: Iterable = ...): ...

def remove(_keys: Iterable, mapper: MutableMapping = ...) -> Mapping: ...

def firstitem(mapper: Mapping[KT, VT]) -> Tuple[KT, VT]: ...
def firstvalue(mapper: Mapping[KT, VT]) -> VT: ...
def firstkey(mapper: Mapping[KT, VT]) -> KT: ...

def obj_zip(_keys: Iterable, _values: Iterable = ...) -> CurriedF: ...
def update_path(_path: str, upset: Any, d: MutableMapping = ...) -> CurriedF: ...
def key_map(fn: Callable, d: Mapping = ...) -> CurriedF: ...
def trans_keys(key_fn: Callable, d: Mapping = ..., deep: bool = ...) -> CurriedF: ...
def dpop(key: KT, d: MutableMapping[KT, VT] = ...) -> CurriedF: ...
def sorted_by_key(key_f: Callable, d: Mapping = ..., reverse: bool = ...) -> CurriedF: ...
def assign(*args: Mapping) -> Mapping: ...
def mstrip(f: Callable, mapper: Mapping) -> CurriedF: ...

def strip_none(mapper: Mapping) -> Mapping: ...
def strip_empty(mapper: Mapping) -> Mapping: ...

def flat_concat(*args: Union[Mapping, Iterable, ...], **kwargs) -> Union[Mapping, Sequence]: ...
def orderby(key_f: Callable, d: Mapping = ..., reverse: Any=...) -> CurriedF: ...

def ordered_key(d: Mapping) -> Mapping: ...
def ordered_value(d: Mapping) -> Mapping: ...

def invert(d: Mapping) -> Mapping: ...
def key_tree(d: Mapping, prefix: str = ...) -> CurriedF: ...
def path(paths: Union[str, Iterable], mapping: Mapping = ...) -> CurriedF: ...
def path_eq(paths: Union[KT, Iterable[KT]], pred: Callable[[VT], bool],
            mapping: Mapping[KT, VT] = ...) -> CurriedF: ...
@overload
def pluck(key: KT, mapper: Mapping[KT, VT], *args: Mapping) -> Tuple[VT]: ...
@overload
def pluck(key: KT) -> Callable[..., Tuple]: ...
def keys_eq(d1: Mapping, d2: Mapping) -> bool: ...
def where(pred: Dict[Any, Callable[[Any], bool]], mapping: Mapping) -> bool: ...
def where_eq(pred: Dict[Any, Callable[[Any], bool]], mapping: Mapping) -> bool: ...
