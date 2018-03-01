import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import requests
import json
import math

import time
from datetime import datetime, timedelta, date
import sys


def build_query_url(begin_date, end_date, stationid, product, datum=None, bin_num=None, units='metric', time_zone='gmt'):
    """
    Builds a URL to be used to fetch data from the NOAA CO-OPS API (see https://tidesandcurrents.noaa.gov/api/)
    """

    base_url = 'http://tidesandcurrents.noaa.gov/api/datagetter?'

    # if the data product is water levels, check that a datum is specified
    if product=='water_level':
        if datum==None:
            raise ValueError('No datum specified for water level data. See https://tidesandcurrents.noaa.gov/api/#datum for list of available datums')
        else:   
            # compile parameter string for use in URL
            parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'datum='+datum, 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']

    # if the data product is currents, check that a bin number is specified
    elif product=='currents':
        if bin_num==None:
            raise ValueError('No bin specified for current data. Bin info can be found on the station info page (e.g., https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515)')
        else:    
            # compile parameter string for use in URL
            parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'bin='+str(bin_num), 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']
    
    # for all other data types (e.g., meteoroligcal conditions)
    else:    
        # compile parameter string for use in URL
        parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']

    parameters_url = '&'.join(parameters)              # join parameters to single string
    query_url = ''.join([base_url, parameters_url])    # joing parameter string with base url for use in url2pandas function

    return query_url


def url2pandas(data_url):
    """
    Takes in a provided url using the NOAA CO-OPS API conventions 
    (see https://tidesandcurrents.noaa.gov/api/), converts the corresponding 
    json data into a pandas dataframe
    """

    response = requests.get(data_url)        # get json data from url
    json_str = response.text                 # json as a string 
    json_dict = json.loads(json_str)         # convert json string to a dictionary for parsing

    if 'error' in json_dict:
        raise ValueError(
            json_dict['error'].get('message', 'Error retrieving data'))

    df = json_normalize(json_dict['data'])   # parse json dictionary for data into dataframe
    
    return df


def get_data(begin_date, end_date, stationid, product, datum=None, bin_num=None, units='metric', time_zone='gmt'):
    """
    Function to get data from NOAA CO-OPS API and convert it to a 
    pandas dataframe for convienent analysis

    Info on the NOOA CO-OPS API can be found here: https://tidesandcurrents.noaa.gov/api/

    Arguments:
    begin_date -- the starting date of request, string in yyyyMMdd format
    end_date -- the ending data of request, string in yyyyMMdd format
    stationid -- station at which you want data
    product -- the product type you would like
    datum -- the datum to be used for water level data  (default None)
    bin_num -- the bin number you would like your current data at (default None) 
    units -- units to be used for data output (default metric)
    time_zone -- time zone to be used for data output (default gmt)
    """

    # convert dates to datetime objects so deltas can be calculated
    begin_datetime = datetime.strptime(begin_date, '%Y%m%d')
    end_datetime = datetime.strptime(end_date, '%Y%m%d')
    delta = end_datetime - begin_datetime

    # If the length of our data request is less or equal to 31 days,
    # we can pull the data from API in one request
    if delta.days <=31:
        data_url = build_query_url(begin_date, end_date, stationid, product, datum, bin_num, units, time_zone)

        df = url2pandas(data_url)

        return df
        
    # If the length the user specified data request is greater than 31 days, 
    # need to pull the data from API using requests of 31 day 'blocks' since 
    # NOAA API prohibits requests larger than 31 days
    else:
        # find the number of 31 day blocks in our desired period,
        # constrain the upper limit of index in the for loop to follow
        num_31day_blocks = math.floor(delta.days/31)

        df = pd.DataFrame([])    # initialize empty dataframe to store data from API requests

        # loop through in 31 day blocks, 
        # adjust the begin_datetime and end_datetime accordingly,
        # make a request to the NOAA CO-OPS API
        for i in range(num_31day_blocks + 1):
            begin_datetime_loop = begin_datetime + timedelta(days = (i*31) )
            end_datetime_loop = begin_datetime_loop + timedelta(days=31)    # ensures we only call 31 days at a time

            # check if the end_datetime_loop of the current 31 day block is greater
            # than the end_date specified by user. If it is, use the end_date specified by user 
            if end_datetime_loop > end_datetime: 
                end_datetime_loop = end_datetime
            
            # build the url for each API request block as we proceed through the loop
            data_url = build_query_url(begin_datetime_loop.strftime('%Y%m%d'),end_datetime_loop.strftime('%Y%m%d'), stationid, product, datum, bin_num, units, time_zone)

            df_new = url2pandas(data_url)    # get data for each block as a pandas dataframe 
            df = df.append(df_new)           # append the dataframe from each request block to the existing dataframe 
        
    # rename output dataframe columns and convert to useable data types
    if product == 'water_level':
        # rename columns for clarity
        df.rename(columns = {'f': 'flags', 'q': 'QC', 's': 'sigma', 't': 'date_time', 'v': 'water_level'}, inplace=True)
        
        # convert columns to numeric values (they are strings objects before this)
        data_cols = df.columns.drop(['flags', 'date_time'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')

        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    elif product == 'currents':
        # rename columns for clarity
        df.rename(columns = {'b': 'bin', 'd': 'direction', 's': 'speed', 't': 'date_time'}, inplace=True)
        
        # convert columns to numeric values (they are strings objects before this)
        data_cols = df.columns.drop(['date_time'])
        df[data_cols] = df[data_cols].apply(pd.to_numeric, axis=1, errors='coerce')
        
        # convert date & time strings to datetime objects
        df['date_time'] = pd.to_datetime(df['date_time'])

    return df
