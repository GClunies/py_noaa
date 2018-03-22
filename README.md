# py_noaa
py_noaa is a Python package containing modules to fetch data using various NOAA APIs (e.g., NOAA Tides & Currents) and returning the data in convient formats (i.e., pandas datadrame) for further analysis in python. Analysis of the data is left up to the end user.

**NOTE:**<br>
This package is under development, additional modules will be added as use cases are encountered that justify new additions.

## Installation
---
`pip install py_noaa`

You can update `py_noaa` using:

`pip install py_noaa --upgrade`

## Available Modules & Data:
---
- [NOAA CO-OPS Tides & Currents](https://tidesandcurrents.noaa.gov/)
    - Observed water levels
    - Predicted water levels (tides)
    - Observed Currents 

## NOAA CO-OPS Tides & Currents
---
NOAA records tides, currents, and other meteoroligical observations at various locations across the United States and the Great Lakes regions. Predictions are also available for [tides](https://tidesandcurrents.noaa.gov/tide_predictions.html) and [currents](https://tidesandcurrents.noaa.gov/noaacurrents/Help).

py_noaa accesses data following the [NOAA CO-OPS API](https://tidesandcurrents.noaa.gov/api/) documentation.
<br>
<br>
### **CO-OPS module basics**
---
1. Get the station ID for your station of interest, a summary of available stations, by data type, can be found through the following links:

    - [Water Level Observation Stations](https://tidesandcurrents.noaa.gov/stations.html?type=Water+Levels)
    - [Tidal Prediction Stations](https://tidesandcurrents.noaa.gov/tide_predictions.html)
    - [Current Observation Stations](https://tidesandcurrents.noaa.gov/cdata/StationList?type=Current+Data&filter=active)
    - [Meteorological Observation Stations](https://tidesandcurrents.noaa.gov/stations.html?type=Meteorological%20Observations)

2. Read the station info if available! Useful station info is typically available based on the datatype recorded at a station.  Station info for current stations are **NOT** the same for water level and tide stations (see examples below).
    - Exmaple [current station info](https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515)
    - Example [water level & tide station info](https://tidesandcurrents.noaa.gov/stationhome.html?id=9447130)

3. Fetch data using the `coops.get_data()` function for various data products, listed [here](https://tidesandcurrents.noaa.gov/api/#products). The currently supported data types are:
- Currents
- Observed water levels
- Predicted water levels (tides)
- Winds
- Air pressure
- Air temperature
- Water temperature

Compatibility with other data products listed on the [NOAA CO-OPS API](https://tidesandcurrents.noaa.gov/api/#products) may exist but is not guaranteed at this time.

### Examples data requests are shown below:

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
>>> df_currents.head() # doctest: +NORMALIZE_WHITESPACE
                     bin  direction  speed
date_time
2015-07-27 20:06:00  1.0      255.0   32.1
2015-07-27 20:12:00  1.0      255.0   30.1
2015-07-27 20:18:00  1.0      261.0   29.3
2015-07-27 20:24:00  1.0      260.0   27.3
2015-07-27 20:30:00  1.0      261.0   23.0

```

**Observed Water Levels**

```python
>>> from py_noaa import coops
>>> df_water_levels = coops.get_data(
...     begin_date="20150101",
...     end_date="20150331",
...     stationid="9447130",
...     product="water_level",
...     datum="MLLW",
...     units="metric",
...     time_zone="gmt")
...
>>> df_water_levels.head() # doctest: +NORMALIZE_WHITESPACE
                       flags QC  sigma  water_level
date_time
2015-01-01 00:00:00  0,0,0,0  v  0.023        1.799
2015-01-01 01:00:00  0,0,0,0  v  0.014        0.977
2015-01-01 02:00:00  0,0,0,0  v  0.009        0.284
2015-01-01 03:00:00  0,0,0,0  v  0.010       -0.126
2015-01-01 04:00:00  0,0,0,0  v  0.013       -0.161

```

**Predicted Water Levels (Tides)**

Note the use of the `interval` parameter to specify only hourly data be returned. The `interval` parameter works with, water level, currents, predictions, and meteorological data types.

```python
>>> from py_noaa import coops
>>> df_predictions = coops.get_data(
...     begin_date="20121115",
...     end_date="20121217",
...     stationid="9447130",
...     product="predictions",
...     datum="MLLW",
...     interval="h",
...     units="metric",
...     time_zone="gmt")
...
>>> df_predictions.head() # doctest: +NORMALIZE_WHITESPACE
                     predicted_wl
date_time
2012-11-15 00:00:00         3.660
2012-11-15 01:00:00         3.431
2012-11-15 02:00:00         2.842
2012-11-15 03:00:00         1.974
2012-11-15 04:00:00         0.953

```

**Filtering Data by date**

All data is returned as a pandas dataframe, with a DatimeIndex which allows for easy filtering of the data by dates.

```python
>>> from py_noaa import coops
>>> df_predictions = coops.get_data(
...     begin_date="20121115",
...     end_date="20121217",
...     stationid="9447130",
...     product="predictions",
...     datum="MLLW",
...     interval="h",
...     units="metric",
...     time_zone="gmt")
...
>>> df_predictions['201211150000':'201211151200'] # doctest: +NORMALIZE_WHITESPACE
                     predicted_wl
date_time
2012-11-15 00:00:00         3.660
2012-11-15 01:00:00         3.431
2012-11-15 02:00:00         2.842
2012-11-15 03:00:00         1.974
2012-11-15 04:00:00         0.953
2012-11-15 05:00:00        -0.047
2012-11-15 06:00:00        -0.787
2012-11-15 07:00:00        -1.045
2012-11-15 08:00:00        -0.740
2012-11-15 09:00:00         0.027
2012-11-15 10:00:00         1.053
2012-11-15 11:00:00         2.114
2012-11-15 12:00:00         3.006

```

### Exporting Data 
---
Since data is returned in a pandas dataframe, exporting the data is simple using the `.to_csv` method on the returned pandas dataframe. This requires the [pandas](https://pandas.pydata.org/) package, which should be taken care of if you installed `py_noaa` with `pip`.

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
>>> df_currents.to_csv(
...     'example.csv',
...     sep='\t',
...     encoding='utf-8')

```

As shown above, you can set the delimeter type using the `sep=` argument in the `.to_csv` method and control the file encoding using the `encoding=` argument.

## Requirements
---
For use:
- requests
- numpy
- pandas

Suggested for developement/contributions:
- pytest
- pytest-cov


## TODO
---
See [issues](https://github.com/GClunies/py_noaa/issues) for a list of issues and to add issues of your own.

## Contribution
---
All contributions are welcome, feel free to submit a pull request if you feel you have a valuable addition to the package or constructive feedback. 

The development of py_noaa was originally intended to help me ([@GClunies](https://github.com/GClunies)) learn python packaging, git, and GitHub while also helping to alleviate the pain of downloading NOAA Tides and Current data as part of my day job as a Coastal engineer.

As this project started as a learning exercise, please be patient and willing to teach/learn.


**Many thanks to the following contributors!**
- [@delgadom](https://github.com/delgadom)  