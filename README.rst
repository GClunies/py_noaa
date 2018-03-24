py\_noaa
========

py\_noaa is a Python package containing modules to fetch data using
various NOAA APIs (e.g., NOAA Tides & Currents) and returning the data
in convient formats (i.e., pandas datadrame) for further analysis in
python. Analysis of the data is left up to the end user.

**NOTE:**\  This package is under development, additional modules will
be added as use cases are encountered that justify new additions.

Installation
---------------

``pip install py_noaa``

Available Modules & Data:
----------------------------

-  `NOAA CO-OPS Tides & Currents <https://tidesandcurrents.noaa.gov/>`__

   -  Observed water levels
   -  Predicted water levels (tides)
   -  Observed Currents

NOAA CO-OPS Tides & Currents
-------------------------------

NOAA records tides, currents, and other meteoroligical observations at
various locations across the United States and the Great Lakes regions.
Predictions are also available for
`tides <https://tidesandcurrents.noaa.gov/tide_predictions.html>`__ and
`currents <https://tidesandcurrents.noaa.gov/noaacurrents/Help>`__.

py\_noaa accesses data following the `NOAA CO-OPS
API <https://tidesandcurrents.noaa.gov/api/>`__ documentation. ###
**CO-OPS module basics** --- 1. Get the station ID for the station of
interest, a summary of available stations, by data type, can be found
through the following links:

::

    - [Water Level Observation Stations](https://tidesandcurrents.noaa.gov/stations.html?type=Water+Levels)
    - [Tidal Prediction Stations](https://tidesandcurrents.noaa.gov/tide_predictions.html)
    - [Current Observation Stations](https://tidesandcurrents.noaa.gov/cdata/StationList?type=Current+Data&filter=active)
    - [Meteorological Observation Stations](https://tidesandcurrents.noaa.gov/stations.html?type=Meteorological%20Observations)

2. Read the station info if available! Useful station info is typically
   available based on the datatype recorded at a station. Station info
   for current stations are **NOT** the same for water level and tide
   stations (see examples below).

   -  Exmaple `current station
      info <https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515>`__
   -  Example `water level & tide station
      info <https://tidesandcurrents.noaa.gov/stationhome.html?id=9447130>`__

3. Fetch data using the ``coops.get_data()`` function for various data
   products, listed
   `here <https://tidesandcurrents.noaa.gov/api/#products>`__. The
   currently supported data types are:

-  Currents
-  Observed water levels
-  Predicted water levels (tides)

Examples data requests are shown below:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Observed Currents**

.. code:: python

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

**Observed Water Levels**

.. code:: python

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
         flags QC  sigma           date_time  water_level
    0  0,0,0,0  v  0.006 2015-01-01 00:00:00       -0.045
    1  0,0,0,0  v  0.008 2015-01-01 00:06:00       -0.028
    2  0,0,0,0  v  0.017 2015-01-01 00:12:00       -0.021
    3  0,0,0,0  v  0.009 2015-01-01 00:18:00        0.008
    4  0,0,0,0  v  0.006 2015-01-01 00:24:00        0.026

**Predicted Water Levels (Tides)**

.. code:: python

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
    >>> df_predictions.head()
                date_time  predicted_wl
    0 2012-11-15 00:00:00         3.660
    1 2012-11-15 01:00:00         3.431
    2 2012-11-15 02:00:00         2.842
    3 2012-11-15 03:00:00         1.974
    4 2012-11-15 04:00:00         0.953

Exporting Data
------------------

Since data is returned in a pandas dataframe, exporting the data is
simple using the ``.to_csv`` method on the returned pandas dataframe.
This requires the `pandas <https://pandas.pydata.org/>`__ package, which
should be taken care of if you installed ``py_noaa`` with ``pip``.

.. code:: python

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
    ...     encoding='utf-8',
    ...     index=False)

As shwon above, you can set the delimeter type using the ``sep=``
argument in the ``.to_csv`` method and control the file encoding using
the ``encoding=`` argument. Setting ``index=False`` will prevent the
index of the pandas dataframe from being inlcuded in the exported csv
file.

Requirements
---------------

For use: - requests - numpy - pandas

Suggested for developement/contributions: - pytest - pytest-cov

TODO
-------

See `issues <https://github.com/GClunies/py_noaa/issues>`__ for a list
of issues and to add issues of your own.

Contribution
---------------

All contributions are welcome, feel free to submit a pull request if you
feel you have a valuable addition to the package or constructive
feedback.

The development of py\_noaa was originally intended to help me
([@GClunies](https://github.com/GClunies)) learn python packaging, git,
and GitHub while also helping to alleviate the pain of downloading NOAA
Tides and Current data as part of my day job as a Coastal engineer.

As this project started as a learning exercise, please be patient and
willing to teach/learn.

**Many thanks needs to be given to the following contributors!** -
[@delgadom](https://github.com/delgadom)
