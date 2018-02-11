import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import requests
import json
import math

import time
from datetime import datetime, timedelta, date


def build_query_url(begin_date, end_date, stationid, product, datum=None, bin_num=None, units='metric', time_zone='gmt'):

    base_url = 'http://tidesandcurrents.noaa.gov/api/datagetter?'

    if product=='water_level':
        if datum==None:    # check that datum is specified
            return 'Error! No datum specified. See https://tidesandcurrents.noaa.gov/api/#datum for list of available datums'
        else:
            parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'datum='+datum, 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']

    elif product=='currents':
        if bin_num==None:
            return 'Error!: No bin specified. Bin info can be found on the station info page (e.g., https://tidesandcurrents.noaa.gov/cdata/StationInfo?id=PUG1515)'
        else:
            parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'bin='+str(bin_num), 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']
    
    else:
        parameters = ['begin_date='+begin_date, 'end_date='+end_date, 'station='+stationid, 'product='+product, 'units='+units, 'time_zone='+time_zone,'application=web_services','format=json']

    parameters_url = '&'.join(parameters)
    query_url = ''.join([base_url, parameters_url])

    return query_url


def get_data(begin_date, end_date, stationid, product, datum=None, bin_num=None, units='metric', time_zone='gmt'):

    begin_datetime = datetime.strptime(begin_date, '%Y%m%d')
    end_datetime = datetime.strptime(end_date, '%Y%m%d')

    delta = end_datetime - begin_datetime

    if delta.days <=31:
        data_url = build_query_url(begin_date, end_date, stationid, product, datum, bin_num, units, time_zone)

        print(data_url)

        response = requests.get(data_url)
        json_str = response.text
        json_dict = json.loads(json_str)
        df= json_normalize(json_dict["data"])
        return df
        
    
    else:    # if delta.days > 31
        num_31day_blocks = math.floor(delta.days/31)

        df = pd.DataFrame([])

        for i in range(num_31day_blocks + 1):
            begin_datetime += timedelta(days = (i*31) )
            end_datetime_loop = begin_datetime + timedelta(days=30)

            print("Processing block {} of {}".format((i+1), num_31day_blocks))

            if delta.days < 31: 
                end_datetime_loop = end_datetime
            
            data_url = build_query_url(begin_datetime.strftime('%Y%m%d'),end_datetime_loop.strftime('%Y%m%d'), stationid, product, datum, bin_num, units, time_zone)

            response = requests.get(data_url)
            json_str = response.text
            json_dict = json.loads(json_str)
            df_new = json_normalize(json_dict["data"])
            df = df.append(df_new)
        
            return df

# Testing code functionality
df_test = get_data("20150727", "20150909", "PUG1515", "currents", datum = None, bin_num = 1, units = "metric", time_zone = "gmt")

print(df_test.tail())
            

    