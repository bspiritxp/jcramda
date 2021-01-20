# JC Ramda

This is a functional programming package includes some functional methods.


## Module: `core`

### curry

|  |  |  |
|------|-----|---------|
|curry|`f -> curried_f`| 柯里化指定函数|
|is_curried|`f -> bool`| 判断函数是否被柯里化|
|flip|`f -> fliped_f`|柯里化并反转指定函数的前两个参数|
|compose|`(f1, f2, ..., fn) -> g`|组合一系列函数为一个函数，从`右`到`左`执行。|
|co|...|同compose|
|pipe|`(f1, f2, ..., fn) -> g`|组合一系列函数为一个函数，从`左`到`右`执行。|
|break_if|`(f, x) -> y -> x`|用于在pipe中判断是否中断执行|


### itertools

||||
|-|-|-|
|chain|`(a1, a2, a3, ..., an) -> tuple`|平铺传入的所有迭代器的元素|
||`(f1, f2) -> x -> f1(f2(x), x)`|连锁执行