import datetime as dt
from dateutil.parser import parse
from jcramda.base import (locnow, to_datetime)


def test_locnow():
    assert locnow().tzinfo


def test_to_datetime():
    assert to_datetime('20201230') == parse('20201230')
    assert to_datetime('2021-11-3') == parse('2021-11-3')
    assert to_datetime(1609753100) == dt.datetime(2021, 1, 4, 17, 38, 20)
