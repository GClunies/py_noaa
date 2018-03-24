import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import requests
import json
import math

import time
from datetime import datetime, timedelta, date
import sys


def build_query_url(begin_date, 
                    end_date, 
                    stationid, 
                    product, 
                    datum=None, 
                    bin_num=None, 
                    interval=None, 
                    units='metric', 
                    time_zone='gmt'):
    """
    Builds a URL to be used to fetch data from the NOAA CO-OPS API
    (see https://tidesandcurrents.noaa.gov/api/)
    """

    base_url = 'http://tidesandcurrents.noaa.gov/api/datagetter?'

    # if the data product is water levels, check that a datum is specified
    if product=='water_level':
        if datum==None:
            raise ValueError('No datum specified for water level data.See'
                        ' https://tidesandcurrents.noaa.gov/api/#datum '
                        'for list of available datums')
        else:   
            # compile parameter string for use in URL
            parameters = ['begin_date='+begin_date, 
                          'end_date='+end_date, 
                          'station='+stationid, 
                          'product='+product, 
                          'datum='+datum, 
                          'units='+units, 
                          'time_zone='+time_zone,
                          'application=py_noaa',
                          'format=json']

    elif product=='predictions':
        # if no interval provided, return 6-min predictions data
        if interval==None:
            # compile parameter string for use in URL
            parameters = ['begin_date='+begin_date, 
                          'end_date='+end_date, 
                          'station='+stationid, 
                          'product='+product, 
                          'datum='+datum, 
                          'units='+units, 
                          'time_zone='+time_zone,
                          'application=py_noaa',
                          'format=json']
        else:   
            # compile parameter string, including interval, for use in URL
            parameters = ['begin_date='+begin_date, 
                          'end_date='+end_date, 
                          'station='+stationid, 
                          'product='+product, 
                          'datum='+datum,
                          'interval='+interval, 
                          'units='+units, 
                          'time_zone='+time_zone,
                          'application=py_noaa',
                          'format=json']

    # if the data product is currents, check that a bin number is specified
    elif product=='currents':
        if bin_num==None:
            raise ValueError('No bin specified for current data. Bin info can be '
                             'found on the station info page' 
                             ' (e.g., https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515)')
        else:    
            # compile parameter string for use in URL
            parameters = ['begin_date='+begin_date, 
                          'end_date='+end_date, 
                          'station='+stationid, 
                          'product='+product, 
                          'bin='+str(bin_num), 
                          'units='+units, 
                          'time_zone='+time_zone, 
                          'application=py_noaa', 
                          'format=json']
    
    # for all other data types (e.g., meteoroligcal conditions)
    else:
        # if no interval provided, return 6-min met data
        if interval==None:    
            # compile parameter string for use in URL
            parameters = ['begin_date='+begin_date, 
                      'end_date='+end_date, 
                      'station='+stationid, 
                      'product='+product, 
                      'units='+units, 
                      'time_zone='+time_zone, 
                      'application=py_noaa', 
                      'format=json']
        else:    
            # compile parameter string, including interval, for use in URL
            parameters = ['begin_date='+begin_date, 
                      'end_date='+end_date, 
                      'station='+stationid, 
                      'product='+product,
                      'interval='+interval, 
                      'units='+units, 
                      'time_zone='+time_zone, 
                      'application=py_noaa', 
                      'format=json']

    parameters_url = '&'.join(parameters)    # join parameters to single string
    query_url = ''.join([base_url, parameters_url])    # join params & url

    return query_url


def url2pandas(data_url, product):
    """
    Takes in a provided url using the NOAA CO-OPS API conventions
    (see https://tidesandcurrents.noaa.gov/api/) and converts the corresponding
    json data into a pandas dataframe
    """

    response = requests.get(data_url)    # get json data from url
    json_str = response.text             # json as a string 
    json_dict = json.loads(json_str)     # convert json string to a dict

    if 'error' in json_dict:
        raise ValueError(
            json_dict['error'].get('message', 'Error retrieving data'))

    if product == 'predictions':
        key = 'predictions'
    else:
        key = 'data'

    df = json_normalize(json_dict[key])   # parse json dict into dataframe
    
    return df


def get_data(begin_date, 
             end_date, 
             stationid, 
             product, 
             datum=None, 
             bin_num=None,
             interval=None,  
             units='metric', 
             time_zone='gmt'):
    """
    Function to get data from NOAA CO-OPS API and convert it to a pandas 
    dataframe for convienent analysis

    Info on the NOOA CO-OPS API can be found at https://tidesandcurrents.noaa.gov/api/, 
    the arguments listed below generally follow the same (or a very similar) format.

    Arguments:
    begin_date -- the starting date of request, string in yyyyMMdd format
    end_date -- the ending data of request, string in yyyyMMdd format
    stationid -- station at which you want data, string
    product -- the product type you would like, string
    datum -- the datum to be used for water level data, string  (default None)
    bin_num -- the bin number you would like your currents data at, int (default None)
    interval -- the interval you would like data returned, string
    units -- units to be used for data output, string (default metric)
    time_zone -- time zone to be used for data output, string (default gmt)
    """

    # convert dates to datetime objects so deltas can be calculated
    begin_datetime = datetime.strptime(begin_date, '%Y%m%d')
    end_datetime = datetime.strptime(end_date, '%Y%m%d')
    delta = end_datetime - begin_datetime

    # If the length of our data request is less or equal to 31 days,
    # we can pull the data from API in one request
    if delta.days <=31:
        data_url = build_query_url(begin_date, 
                                   end_date, 
                                   stationid, 
                                   product, 
                                   datum, 
                                   bin_num,
                                   interval, 
                                   units, 
                                   time_zone)

        df = url2pandas(data_url, product)
        
    # If the length of the user specified data request is greater than 31 days, 
    # need to pull the data from API using requests of 31 day 'blocks' since 
    # NOAA API prohibits requests larger than 31 days
    else:
        # find the number of 31 day blocks in our desired period,
        # constrain the upper limit of index in the for loop to follow
        num_31day_blocks = int(math.floor(delta.days/31))

        df = pd.DataFrame([])    # empty dataframe for data from API requests

        # loop through in 31 day blocks, 
        # adjust the begin_datetime and end_datetime accordingly,
        # make a request to the NOAA CO-OPS API
        for i in range(num_31day_blocks + 1):
            begin_datetime_loop = begin_datetime + timedelta(days = (i*31) )
            end_datetime_loop = begin_datetime_loop + timedelta(days=31)

            # if end_datetime_loop of the current 31 day block is greater
            # than end_datetime specified by user, use end_datetime 
            if end_datetime_loop > end_datetime: 
                end_datetime_loop = end_datetime
            
            # build url for each API request as we proceed through the loop
            data_url = build_query_url(begin_datetime_loop.strftime('%Y%m%d'), 
                                       end_datetime_loop.strftime('%Y%m%d'), 
                                       stationid, 
                                       product, 
                                       datum, 
                                       bin_num,
                                       interval,
                                       units, 
                                       time_zone)

            df_new = url2pandas(data_url, product)    # get dataframe for block 
            df = df.append(df_new)    # append to existing dataframe 
        
    # rename output dataframe columns based on requested product
    # and convert to useable data types
    if product == 'water_level':
        # rename columns for clarity
        df.rename(columns = {'f': 'flags', 'q': 'QC', 's': 'sigma',
                             't': 'date_time', 'v': 'water_level'}, 
                             inplace=True)
        
        # convert columns to numeric values
        data_cols = df.columns.drop(['flags', 'QC', 'date_time'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')

        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'predictions':
        # rename columns for clarity
        df.rename(columns = {'t': 'date_time', 'v': 'predicted_wl'}, 
                             inplace=True)
        
        # convert columns to numeric values
        data_cols = df.columns.drop(['date_time'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')

        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'currents':
        # rename columns for clarity
        df.rename(columns = {'b': 'bin', 'd': 'direction',
                             's': 'speed', 't': 'date_time'},
                             inplace=True)
        
        # convert columns to numeric values
        data_cols = df.columns.drop(['date_time'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')
        
        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'wind':
        # rename columns for clarity
        df.rename(columns = {'d': 'dir', 'dr': 'compass',
                             'f': 'flags', 'g': 'gust_spd',
                             's': 'spd', 't': 'date_time'},
                             inplace=True)
        
        # convert columns to numeric values
        data_cols = df.columns.drop(['date_time', 'flags', 'compass'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')
        
        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'air_pressure':
        # rename columns for clarity
        df.rename(columns = {'f': 'flags', 't': 'date_time', 'v':'air_press'},
                             inplace=True)
        
        # convert columns to numeric values
        data_cols = df.columns.drop(['date_time', 'flags'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')
        
        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'air_temperature':
        # rename columns for clarity
        df.rename(columns = {'f': 'flags', 't': 'date_time', 'v':'air_temp'},
                             inplace=True)
        
        # convert columns to numeric values
        data_cols = df.columns.drop(['date_time', 'flags'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')
        
        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'water_temperature':
        # rename columns for clarity
        df.rename(columns = {'f': 'flags', 't': 'date_time', 'v':'water_temp'},
                             inplace=True)
        
        # convert columns to numeric values
        data_cols = df.columns.drop(['date_time', 'flags'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')
        
        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])


    # set datetime to index (for use in resampling)
    df.index = df['date_time']
    df = df.drop(columns=['date_time'])

    # handle hourly requests for water_level and currents data
    if (product == 'water_level') | (product == 'currents') & (interval == 'h'):
        df = df.resample('H').first()    # only return the hourly data

    return df
