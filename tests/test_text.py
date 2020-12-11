from jcramda.base.text import *


def test_camelcase():
    assert camelcase_to('_', 'fooBar') == 'foo_bar'
