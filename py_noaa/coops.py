import math
from datetime import datetime, timedelta

import pandas as pd
import requests
from pandas.io.json import json_normalize


def build_query_url(
        begin_date, end_date, stationid, product, datum=None, bin_num=None,
        interval=None, units='metric', time_zone='gmt'):
    """
    Build an URL to be used to fetch data from the NOAA CO-OPS API
    (see https://tidesandcurrents.noaa.gov/api/)
    """
    base_url = 'http://tidesandcurrents.noaa.gov/api/datagetter?'

    # If the data product is water levels, check that a datum is specified
    if product == 'water_level':
        if datum is None:
            raise ValueError('No datum specified for water level data.See'
                             ' https://tidesandcurrents.noaa.gov/api/#datum '
                             'for list of available datums')
        else:
            # Compile parameter string for use in URL
            parameters = {'begin_date': begin_date,
                          'end_date': end_date,
                          'station': stationid,
                          'product': product,
                          'datum': datum,
                          'units': units,
                          'time_zone': time_zone,
                          'application': 'py_noaa',
                          'format': 'json'}

    elif product == 'hourly_height':
        if datum is None:
            raise ValueError('No datum specified for water level data.See'
                             ' https://tidesandcurrents.noaa.gov/api/#datum '
                             'for list of available datums')
        else:
            # Compile parameter string for use in URL
            parameters = {'begin_date': begin_date,
                          'end_date': end_date,
                          'station': stationid,
                          'product': product,
                          'datum': datum,
                          'units': units,
                          'time_zone': time_zone,
                          'application': 'py_noaa',
                          'format': 'json'}
    elif product == 'high_low':
        if datum is None:
            raise ValueError('No datum specified for water level data.See'
                             ' https://tidesandcurrents.noaa.gov/api/#datum '
                             'for list of available datums')
        else:
            # Compile parameter string for use in URL
            parameters = {'begin_date': begin_date,
                          'end_date': end_date,
                          'station': stationid,
                          'product': product,
                          'datum': datum,
                          'units': units,
                          'time_zone': time_zone,
                          'application': 'py_noaa',
                          'format': 'json'}

    elif product == 'predictions':
        # If no interval provided, return 6-min predictions data
        if interval is None:
            # Compile parameter string for use in URL
            parameters = {'begin_date': begin_date,
                          'end_date': end_date,
                          'station': stationid,
                          'product': product,
                          'datum': datum,
                          'units': units,
                          'time_zone': time_zone,
                          'application': 'py_noaa',
                          'format': 'json'}

        else:
            # Compile parameter string, including interval, for use in URL
            parameters = {'begin_date': begin_date,
                          'end_date': end_date,
                          'station': stationid,
                          'product': product,
                          'datum': datum,
                          'interval': interval,
                          'units': units,
                          'time_zone': time_zone,
                          'application': 'py_noaa',
                          'format': 'json'}

    # If the data product is currents, check that a bin number is specified
    elif product == 'currents':
        if bin_num is None:
            raise ValueError(
                'No bin specified for current data. Bin info can be '
                'found on the station info page'
                ' (e.g., https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515)')
        else:
            # Compile parameter string for use in URL
            parameters = {'begin_date': begin_date,
                          'end_date': end_date,
                          'station': stationid,
                          'product': product,
                          'bin': str(bin_num),
                          'units': units,
                          'time_zone': time_zone,
                          'application': 'py_noaa',
                          'format': 'json'}

    # For all other data types (e.g., meteoroligcal conditions)
    else:
        # If no interval provided, return 6-min met data
        if interval is None:
            # Compile parameter string for use in URL
            parameters = {'begin_date': begin_date,
                          'end_date': end_date,
                          'station': stationid,
                          'product': product,
                          'units': units,
                          'time_zone': time_zone,
                          'application': 'py_noaa',
                          'format': 'json'}
        else:
            # Compile parameter string, including interval, for use in URL
            parameters = {'begin_date': begin_date,
                          'end_date': end_date,
                          'station': stationid,
                          'product': product,
                          'interval': interval,
                          'units': units,
                          'time_zone': time_zone,
                          'application': 'py_noaa',
                          'format': 'json'}

    # Build URL with requests library
    query_url = requests.Request(
        'GET', base_url, params=parameters).prepare().url

    return query_url


def url2pandas(data_url, product):
    """
    Takes in a provided URL using the NOAA CO-OPS API conventions
    (see https://tidesandcurrents.noaa.gov/api/) and converts the corresponding
    JSON data into a pandas dataframe.
    """

    response = requests.get(data_url)  # Get JSON data from URL
    json_dict = response.json()

    if 'error' in json_dict:
        raise ValueError(
            json_dict['error'].get('message', 'Error retrieving data'))

    if product == 'predictions':
        key = 'predictions'
    else:
        key = 'data'

    df = json_normalize(json_dict[key])  # Parse JSON dict into dataframe

    return df


def parse_known_date_formats(dt_string):
    """Attempt to parse CO-OPS accepted date formats."""
    for fmt in ('%Y%m%d', '%Y%m%d %H:%M', '%m/%d/%Y', '%m/%d/%Y %H:%M'):
        try:
            return datetime.strptime(dt_string, fmt)
        except ValueError:
            pass
    raise ValueError("No valid date format found."
                     "See https://tidesandcurrents.noaa.gov/api/ "
                     "for list of accepted date formats.")


def get_data(
        begin_date, end_date, stationid, product, datum=None, bin_num=None,
        interval=None, units='metric', time_zone='gmt'):
    """
    Function to get data from NOAA CO-OPS API and convert it to a pandas
    dataframe for convenient analysis.

    Info on the NOOA CO-OPS API can be found at https://tidesandcurrents.noaa.gov/api/,
    the arguments listed below generally follow the same (or a very similar) format.

    Arguments:
    begin_date -- the starting date of request (yyyyMMdd, yyyyMMdd HH:mm, MM/dd/yyyy, or MM/dd/yyyy HH:mm), string
    end_date -- the ending date of request (yyyyMMdd, yyyyMMdd HH:mm, MM/dd/yyyy, or MM/dd/yyyy HH:mm), string
    stationid -- station at which you want data, string
    product -- the product type you would like, string
    datum -- the datum to be used for water level data, string  (default None)
    bin_num -- the bin number you would like your currents data at, int (default None)
    interval -- the interval you would like data returned, string
    units -- units to be used for data output, string (default metric)
    time_zone -- time zone to be used for data output, string (default gmt)
    """
    # Convert dates to datetime objects so deltas can be calculated
    begin_datetime = parse_known_date_formats(begin_date)
    end_datetime = parse_known_date_formats(end_date)
    delta = end_datetime - begin_datetime

    # If the length of our data request is less or equal to 31 days,
    # we can pull the data from API in one request
    if delta.days <= 31:
        data_url = build_query_url(
            begin_datetime.strftime("%Y%m%d %H:%M"),
            end_datetime.strftime("%Y%m%d %H:%M"),
            stationid, product, datum, bin_num, interval, units, time_zone)

        df = url2pandas(data_url, product)

    # If the length of the user specified data request is less than 365 days
    # AND the product is hourly_height or high_low, we can pull data directly
    # from the API in one request
    elif delta.days <= 365 and (
            product == 'hourly_height' or product == 'high_low'):
        data_url = build_query_url(
            begin_date, end_date, stationid, product, datum, bin_num, interval,
            units, time_zone)

        df = url2pandas(data_url, product)

    # If the length of the user specified data request is greater than 365 days
    # AND the product is hourly_height or high_low, we need to load data from
    # the API in365 day blocks.
    elif product == 'hourly_height' or product == 'high_low':
        # Find the number of 365 day blocks in our desired period,
        # constrain the upper limit of index in the for loop to follow
        num_365day_blocks = int(math.floor(delta.days / 365))

        df = pd.DataFrame([])  # Empty dataframe for data from API requests

        # Loop through in 365 day blocks,
        # adjust the begin_datetime and end_datetime accordingly,
        # make a request to the NOAA CO-OPS API
        for i in range(num_365day_blocks + 1):
            begin_datetime_loop = begin_datetime + timedelta(days=(i * 365))
            end_datetime_loop = begin_datetime_loop + timedelta(days=365)

            # If end_datetime_loop of the current 365 day block is greater
            # than end_datetime specified by user, use end_datetime
            if end_datetime_loop > end_datetime:
                end_datetime_loop = end_datetime

            # Build url for each API request as we proceed through the loop
            data_url = build_query_url(
                begin_datetime_loop.strftime('%Y%m%d'),
                end_datetime_loop.strftime('%Y%m%d'),
                stationid, product, datum, bin_num, interval, units, time_zone)

            df_new = url2pandas(data_url, product)  # Get dataframe for block
            df = df.append(df_new)  # Append to existing dataframe

    # If the length of the user specified data request is greater than 31 days
    # for any other products, we need to load data from the API in 31 day
    # blocks
    else:
        # Find the number of 31 day blocks in our desired period,
        # constrain the upper limit of index in the for loop to follow
        num_31day_blocks = int(math.floor(delta.days / 31))

        df = pd.DataFrame([])  # Empty dataframe for data from API requests

        # Loop through in 31 day blocks,
        # adjust the begin_datetime and end_datetime accordingly,
        # make a request to the NOAA CO-OPS API
        for i in range(num_31day_blocks + 1):
            begin_datetime_loop = begin_datetime + timedelta(days=(i * 31))
            end_datetime_loop = begin_datetime_loop + timedelta(days=31)

            # If end_datetime_loop of the current 31 day block is greater
            # than end_datetime specified by user, use end_datetime
            if end_datetime_loop > end_datetime:
                end_datetime_loop = end_datetime

            # Build URL for each API request as we proceed through the loop
            data_url = build_query_url(
                begin_datetime_loop.strftime('%Y%m%d'),
                end_datetime_loop.strftime('%Y%m%d'),
                stationid, product, datum, bin_num, interval, units, time_zone)

            df_new = url2pandas(data_url, product)  # Get dataframe for block
            df = df.append(df_new)  # Append to existing dataframe

    # Rename output dataframe columns based on requested product
    # and convert to useable data types
    if product == 'water_level':
        # Rename columns for clarity
        df.rename(columns={'f': 'flags', 'q': 'QC', 's': 'sigma',
                           't': 'date_time', 'v': 'water_level'},
                  inplace=True)

        # Convert columns to numeric values
        data_cols = df.columns.drop(['flags', 'QC', 'date_time'])
        df[data_cols] = df[data_cols].apply(
            pd.to_numeric, axis=1, errors='coerce')

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'hourly_height':
        # Rename columns for clarity
        df.rename(columns={'f': 'flags', 's': 'sigma',
                           't': 'date_time', 'v': 'water_level'},
                  inplace=True)

        # Convert columns to numeric values
        data_cols = df.columns.drop(['flags', 'date_time'])
        df[data_cols] = df[data_cols].apply(
            pd.to_numeric, axis=1, errors='coerce')

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'high_low':
        # Rename columns for clarity
        df.rename(columns={'f': 'flags', 'ty': 'high_low',
                           't': 'date_time', 'v': 'water_level'},
                  inplace=True)

        # Separate to high and low dataframes
        df_HH = df[df['high_low'] == "HH"].copy()
        df_HH.rename(columns={'date_time': 'date_time_HH',
                              'water_level': 'HH_water_level'},
                     inplace=True)

        df_H = df[df['high_low'] == "H "].copy()
        df_H.rename(columns={'date_time': 'date_time_H',
                             'water_level': 'H_water_level'},
                    inplace=True)

        df_L = df[df['high_low'].str.contains("L ")].copy()
        df_L.rename(columns={'date_time': 'date_time_L',
                             'water_level': 'L_water_level'},
                    inplace=True)

        df_LL = df[df['high_low'].str.contains("LL")].copy()
        df_LL.rename(columns={'date_time': 'date_time_LL',
                              'water_level': 'LL_water_level'},
                     inplace=True)

        # Extract dates (without time) for each entry
        dates_HH = [x.date() for x in pd.to_datetime(df_HH['date_time_HH'])]
        dates_H = [x.date() for x in pd.to_datetime(df_H['date_time_H'])]
        dates_L = [x.date() for x in pd.to_datetime(df_L['date_time_L'])]
        dates_LL = [x.date() for x in pd.to_datetime(df_LL['date_time_LL'])]

        # Set indices to datetime
        df_HH['date_time'] = dates_HH
        df_HH.index = df_HH['date_time']
        df_H['date_time'] = dates_H
        df_H.index = df_H['date_time']
        df_L['date_time'] = dates_L
        df_L.index = df_L['date_time']
        df_LL['date_time'] = dates_LL
        df_LL.index = df_LL['date_time']

        # Remove flags and combine to single dataframe
        df_HH = df_HH.drop(
            columns=['flags', 'high_low'])
        df_H = df_H.drop(columns=['flags', 'high_low',
                                  'date_time'])
        df_L = df_L.drop(columns=['flags', 'high_low',
                                  'date_time'])
        df_LL = df_LL.drop(columns=['flags', 'high_low',
                                    'date_time'])

        # Keep only one instance per date (based on max/min)
        maxes = df_HH.groupby(df_HH.index).HH_water_level.transform(max)
        df_HH = df_HH.loc[df_HH.HH_water_level == maxes]
        maxes = df_H.groupby(df_H.index).H_water_level.transform(max)
        df_H = df_H.loc[df_H.H_water_level == maxes]
        mins = df_L.groupby(df_L.index).L_water_level.transform(max)
        df_L = df_L.loc[df_L.L_water_level == mins]
        mins = df_LL.groupby(df_LL.index).LL_water_level.transform(max)
        df_LL = df_LL.loc[df_LL.LL_water_level == mins]

        df = df_HH.join(df_H, how='outer')
        df = df.join(df_L, how='outer')
        df = df.join(df_LL, how='outer')

        # Convert columns to numeric values
        data_cols = df.columns.drop(
            ['date_time', 'date_time_HH', 'date_time_H', 'date_time_L',
             'date_time_LL'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1,
                                            errors='coerce')

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df.index)
        df['date_time_HH'] = pd.to_datetime(df['date_time_HH'])
        df['date_time_H'] = pd.to_datetime(df['date_time_H'])
        df['date_time_L'] = pd.to_datetime(df['date_time_L'])
        df['date_time_LL'] = pd.to_datetime(df['date_time_LL'])

    elif product == 'predictions':
        if interval == 'h':
            # Rename columns for clarity
            df.rename(columns={'t': 'date_time', 'v': 'predicted_wl'},
                      inplace=True)

            # Convert columns to numeric values
            data_cols = df.columns.drop(['date_time'])

        elif interval == 'hilo':
            # Rename columns for clarity
            df.rename(columns={'t': 'date_time', 'v': 'predicted_wl',
                               'type': 'hi_lo'},
                      inplace=True)

            # Convert columns to numeric values
            data_cols = df.columns.drop(['date_time', 'hi_lo'])

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'currents':
        # Rename columns for clarity
        df.rename(columns={'b': 'bin', 'd': 'direction',
                           's': 'speed', 't': 'date_time'},
                  inplace=True)

        # Convert columns to numeric values
        data_cols = df.columns.drop(['date_time'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1,
                                            errors='coerce')

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'wind':
        # Rename columns for clarity
        df.rename(columns={'d': 'dir', 'dr': 'compass',
                           'f': 'flags', 'g': 'gust_spd',
                           's': 'spd', 't': 'date_time'},
                  inplace=True)

        # Convert columns to numeric values
        data_cols = df.columns.drop(['date_time', 'flags', 'compass'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1,
                                            errors='coerce')

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'air_pressure':
        # Rename columns for clarity
        df.rename(columns={'f': 'flags', 't': 'date_time', 'v': 'air_press'},
                  inplace=True)

        # Convert columns to numeric values
        data_cols = df.columns.drop(['date_time', 'flags'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1,
                                            errors='coerce')

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'air_temperature':
        # Rename columns for clarity
        df.rename(columns={'f': 'flags', 't': 'date_time', 'v': 'air_temp'},
                  inplace=True)

        # Convert columns to numeric values
        data_cols = df.columns.drop(['date_time', 'flags'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1,
                                            errors='coerce')

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'water_temperature':
        # Rename columns for clarity
        df.rename(columns={'f': 'flags', 't': 'date_time', 'v': 'water_temp'},
                  inplace=True)

        # Convert columns to numeric values
        data_cols = df.columns.drop(['date_time', 'flags'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1,
                                            errors='coerce')

        # Convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    # Set datetime to index (for use in resampling)
    df.index = df['date_time']
    df = df.drop(columns=['date_time'])

    # Handle hourly requests for water_level and currents data
    if (product == 'water_level') | (product == 'currents') & (
            interval == 'h'):
        df = df.resample('H').first()  # Only return the hourly data

    return df
