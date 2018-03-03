# py_noaa
py_noaa is a Python package containing modules for fetching data from various NOAA APIs (e.g., NOAA Tides & Currents) and returning the data in convient formats (i.e., pandas datadrame) for further analysis in python. This package is under development, additional modules will be added as I encounter use cases that justify new API modules being added.

Install with `pip install py_noaa`

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

Useful station info is also typically available for different datasets at a given station (e.g., [station info](https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515) for current data at a station in Puget Sound)

You can then fetch data from the API using the `coops.get_data` function for various data products, listed [here](https://tidesandcurrents.noaa.gov/api/#products). 

Two examples are shown below:

**Observed Currents**

```python
>>> from py_noaa import coops
>>> df_currents = coops.get_data(
...     begin_date="20150727",
...     end_date="20150910",
...     stationid="PUG1515",
...     product="currents",
...     bin_num=1,
...     units="metric",
...     time_zone="gmt")
...
>>> df_currents.head()
   bin  direction  speed           date_time
0  1.0      255.0   32.1 2015-07-27 20:06:00
1  1.0      255.0   30.1 2015-07-27 20:12:00
2  1.0      261.0   29.3 2015-07-27 20:18:00
3  1.0      260.0   27.3 2015-07-27 20:24:00
4  1.0      261.0   23.0 2015-07-27 20:30:00

```

**Observed Water Levels**

```python
>>> from py_noaa import coops
>>> df_water_levels = coops.get_data(
...     begin_date="20150101",
...     end_date="20150331",
...     stationid="9442396",
...     product="water_level",
...     datum="MLLW",
...     units="metric",
...     time_zone="gmt")
...
>>> df_water_levels.head()
     flags  QC  sigma           date_time  water_level
0  0,0,0,0 NaN  0.006 2015-01-01 00:00:00       -0.045
1  0,0,0,0 NaN  0.008 2015-01-01 00:06:00       -0.028
2  0,0,0,0 NaN  0.017 2015-01-01 00:12:00       -0.021
3  0,0,0,0 NaN  0.009 2015-01-01 00:18:00        0.008
4  0,0,0,0 NaN  0.006 2015-01-01 00:24:00        0.026

```

### Exporting Data 
---
Since data is returned in a pandas dataframe, exporting the data is simple using the `.to_csv` method on the returned pandas dataframe. This requires the [pandas](https://pandas.pydata.org/) module to already be imported into your workspace.

```python
>>> df_currents = coops.get_data(
...     begin_date="20150727",
...     end_date="20150910",
...     stationid="PUG1515",
...     product="currents",
...     bin_num=1,
...     units="metric",
...     time_zone="gmt")
...
>>> df_currents.to_csv('example.csv')

```

You can set the delimeter type using the `sep=` argument in the `.to_csv` method and control the file encoding using the `encoding=` argument. Setting `index=False` will prevent the index from the pandas dataframe from being inlcuded in the exported csv file. Example:

```python
>>> df_currents.to_csv(
...     'example.csv',
...     sep='\t',
...     encoding='utf-8',
...     index=False)

```
