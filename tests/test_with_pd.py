import pandas as pd
import jcramda as jr


def test_loc():
    df = pd.DataFrame({'a': range(10)})
    r = jr.loc(3, df)
    assert r.a == 3
