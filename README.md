# py_noaa
py_noaa is a Python package with modules for fetching data from various NOAA APIs (e.g., NOAA Tides&Currents).This package is under development, additional modules will be added as I enocunter cases that justify new APIs modules being added.<br>
<br>
Install with `pip install py_noaa`.
<br>
**Currently available modules:**
- NOAA CO-OPS Tides&Currents [see documentation](https://tidesandcurrents.noaa.gov/api/)

## NOAA CO-OPS Tides&Currents API
NOAA records tides, currents, and other meteoroligical observations at various locations across the United States and the Great Lakes regions. Predictions are also available for [tides](https://tidesandcurrents.noaa.gov/tide_predictions.html) and [currents](https://tidesandcurrents.noaa.gov/noaacurrents/Help).
<br>
Data can be accessed from the NOAA CO-OPS API using the coops module.

### coops module basics

First, get the station for which you would like to get data, a summary of available stations (depending on data type) can be found through the following links:
<br>
[Water Level Observation Stations](https://tidesandcurrents.noaa.gov/stations.html?type=Water+Levels)
[Tidal Prediction Stations](https://tidesandcurrents.noaa.gov/tide_predictions.html)
[Current Observation Stations](https://tidesandcurrents.noaa.gov/cdata/StationList?type=Current+Data&filter=active)
[Meteorological Observation Stations](https://tidesandcurrents.noaa.gov/stations.html?type=Meteorological%20Observations)

You can then fetch data from the API using the `get_data` function for various data products, listed [here](https://tidesandcurrents.noaa.gov/api/#products). Two examples are shown below:

**Observed Currents**
```
>>> df_currents = get_data(begin_date="20150727", end_date="20150910", stationid="PUG1515", product="currents", bin_num=1, units="metric", time_zone="gmt")
>>> df_currents.head()
   b    d       s                 t
0  1  255  32.100  2015-07-27 20:06
1  1  255  30.100  2015-07-27 20:12
2  1  261  29.300  2015-07-27 20:18
3  1  260  27.300  2015-07-27 20:24
4  1  261  23.000  2015-07-27 20:30
```
<br>
**Observed Water Levels**
```
>>> df_water_levels = get_data(begin_date="20150101", end_date="20150331", stationid="9442396", product="water_level", datum="MLLW", units="metric", time_zone="gmt")
>>> df_water_levels.head()
         f  q      s                 t       v
0  0,0,0,0  v  0.006  2015-01-01 00:00  -0.045
1  0,0,0,0  v  0.008  2015-01-01 00:06  -0.028
2  0,0,0,0  v  0.017  2015-01-01 00:12  -0.021
3  0,0,0,0  v  0.009  2015-01-01 00:18   0.008
4  0,0,0,0  v  0.006  2015-01-01 00:24   0.026
```




