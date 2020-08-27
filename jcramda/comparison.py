from .core import curry, flip, co, lt, le, gt, ge, eq


len_lt = curry(lambda n, x: len(x) < n)
len_le = curry(lambda n, x: len(x) <= n)
len_eq = curry(lambda n, x: len(x) == n)
len_gt = curry(lambda n, x: len(x) > n)
len_ge = curry(lambda n, x: len(x) >= n)


is_zero = eq(0)

