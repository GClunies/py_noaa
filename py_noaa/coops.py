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

    if product=='water_level':
        if datum==None:    # check that datum is specified
            sys.exit('ERROR! No datum specified for water level data. See https://tidesandcurrents.noaa.gov/api/#datum for list of available datums')
        else:
            parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'datum='+datum, 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']

    elif product=='currents':
        if bin_num==None:
            sys.exit('ERROR! No bin specified for current data. Bin info can be found on the station info page (e.g., https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515)')
        else:
            parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'bin='+str(bin_num), 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']
    
    else:
        parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']

    parameters_url = '&'.join(parameters)
    query_url = ''.join([base_url, parameters_url])

    return query_url

def url2pandas(data_url):
    """
    Takes in a provided url using the NOAA CO-OPS API conventions (see https://tidesandcurrents.noaa.gov/api/), converts the corresponding json data into a pandas dataframe
    """
    response = requests.get(data_url)
    json_str = response.text
    json_dict = json.loads(json_str)
    df = json_normalize(json_dict['data'])
    
    return df


def get_data(begin_date, end_date, stationid, product, datum=None, bin_num=None, units='metric', time_zone='gmt'):
    """
    Gets data from NOAA CO-OPS API (see https://tidesandcurrents.noaa.gov/api/) and converts it to a pandas dataframe for convienent analysis

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

    begin_datetime = datetime.strptime(begin_date, '%Y%m%d')
    end_datetime = datetime.strptime(end_date, '%Y%m%d')

    delta = end_datetime - begin_datetime

    if delta.days <=31:
        data_url = build_query_url(begin_date, end_date, stationid, product, datum, bin_num, units, time_zone)

        df = url2pandas(data_url)
        
    
    else:    # if delta.days > 31
        num_31day_blocks = math.floor(delta.days/31)

        df = pd.DataFrame([])

        for i in range(num_31day_blocks + 1):
            begin_datetime += timedelta(days = (i*31) )
            end_datetime_loop = begin_datetime + timedelta(days=30)

            if delta.days < 31: 
                end_datetime_loop = end_datetime
            
            data_url = build_query_url(begin_datetime.strftime('%Y%m%d'),end_datetime_loop.strftime('%Y%m%d'), stationid, product, datum, bin_num, units, time_zone)

            df_new = url2pandas(data_url)
            df = df.append(df_new)
        
            return df
