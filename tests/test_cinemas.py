from datetime import datetime, timedelta

import pytest
import pytz
import requests

from consts import headers
from models import cinemas_get_screenings, GetScreeningCallable


@pytest.mark.parametrize("get_screenings", cinemas_get_screenings.values(), ids=cinemas_get_screenings.keys())
def test_cinema(get_screenings: GetScreeningCallable):
    s = requests.session()
    s.headers.update(headers)
    screenings = []
    for delta in range(1, 3):  # Cinemas don't work on memorial days and Yom Kippur
        date = datetime.now(pytz.timezone('ASIA/TEL_AVIV')) + timedelta(days=delta)
        year = str(date.year)
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)
        screenings = get_screenings(year, month, day, s)
        if screenings:
            break
    assert screenings
