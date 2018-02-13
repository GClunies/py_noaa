# py_noaa
py_noaa is a Python package containing modules for fetching data from various NOAA APIs (e.g., NOAA Tides & Currents) and returning the data in convient formats (i.e., pandas datadrame) for further analysis in python. This package is under development, additional modules will be added as I encounter use cases that justify new API modules being added.

Install with `pip install py_noaa`.

**Currently available modules:**
- NOAA CO-OPS Tides & Currents ([see API documentation](https://tidesandcurrents.noaa.gov/api/))

## NOAA CO-OPS Tides & Currents API [website](https://tidesandcurrents.noaa.gov/)
---
NOAA records tides, currents, and other meteoroligical observations at various locations across the United States and the Great Lakes regions. Predictions are also available for [tides](https://tidesandcurrents.noaa.gov/tide_predictions.html) and [currents](https://tidesandcurrents.noaa.gov/noaacurrents/Help).

Data can be accessed from the NOAA CO-OPS API using the `coops.get_data()` function in the coops.py module.

### coops module basics
---
First, get the station for which you would like to get data, a summary of available stations (depending on data type) can be found through the following links:

- [Water Level Observation Stations](https://tidesandcurrents.noaa.gov/stations.html?type=Water+Levels)
- [Tidal Prediction Stations](https://tidesandcurrents.noaa.gov/tide_predictions.html)
- [Current Observation Stations](https://tidesandcurrents.noaa.gov/cdata/StationList?type=Current+Data&filter=active)
- [Meteorological Observation Stations](https://tidesandcurrents.noaa.gov/stations.html?type=Meteorological%20Observations)

Useful station info is also typically available for diffent datasets at a given station (e.g., [station info](https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515) for current data at a station in Puget Sound)

You can then fetch data from the API using the `coops.get_data` function for various data products, listed [here](https://tidesandcurrents.noaa.gov/api/#products). 

Two examples are shown below:

**Observed Currents**
```
>>> from py_noaa import coops
>>> df_currents = coops.get_data(begin_date="20150727", end_date="20150910", stationid="PUG1515", product="currents", bin_num=1, units="metric", time_zone="gmt")
>>> df_currents.head()
   b    d       s                 t
0  1  255  32.100  2015-07-27 20:06
1  1  255  30.100  2015-07-27 20:12
2  1  261  29.300  2015-07-27 20:18
3  1  260  27.300  2015-07-27 20:24
4  1  261  23.000  2015-07-27 20:30
```

**Observed Water Levels**

```
>>> from py_noaa import coops
>>> df_water_levels = coops.get_data(begin_date="20150101", end_date="20150331", stationid="9442396", product="water_level", datum="MLLW", units="metric", time_zone="gmt")
>>> df_water_levels.head()
         f  q      s                 t       v
0  0,0,0,0  v  0.006  2015-01-01 00:00  -0.045
1  0,0,0,0  v  0.008  2015-01-01 00:06  -0.028
2  0,0,0,0  v  0.017  2015-01-01 00:12  -0.021
3  0,0,0,0  v  0.009  2015-01-01 00:18   0.008
4  0,0,0,0  v  0.006  2015-01-01 00:24   0.026
```

### Exporting data 
---
Since data is returned in a pandas dataframe, exporting the data is simple using the `.to_csv` method on the returned pandas dataframe. 

``` 
>>> df_currents.to_csv('example.csv')
```

You can set the delimeter type using the `sep=` argument in the `.to_csv` method and control the file encoding using the `encoding=` argument. Setting `index=False` will prevent the index from the pandas dataframe from being inlcuded in the exported csv file. Example:

```
>>> df_currents(f'example.csv', encoding='utf-8', index=False)
```