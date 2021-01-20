from jcramda.base.text import *


def test_camelcase():
    assert camelcase_to('_', 'fooBar') == 'foo_bar'
    assert camelcase_to('_', 'orign') == 'orign'
    assert camelcase_to('_', '') == ''
    assert camelcase_to('_', 'ABC') == 'a_b_c'
    assert camelcase('foo_bar') == 'fooBar'
    assert camelcase(sep='$')('foo$bar') == 'fooBar' 
