
from __future__ import absolute_import
from py_noaa import coops

import pytest

def test_error_handling():
    with pytest.raises(ValueError):
        coops.get_data(
            begin_date="20150101",
            end_date="20150331",
            stationid="9442396",
            product="water_level",
            datum="navd88", # this is an invalid datum
            units="metric",
            time_zone="gmt")
