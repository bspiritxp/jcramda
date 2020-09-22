from jcramda.base import (locnow, now)


def test_locnow():
    assert locnow().tzinfo
