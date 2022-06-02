pip install polygon-api-client
pip install pandas
pip install numpy
pip install datetime

from polygon import RESTClient
import pandas as pd
import numpy as np
import DateTime as dt

# My personal link to Polygon API
key = "EDLxK3WsIehHcQhZBtyclO7DU5S6o95a"


def ts_to_datetime(ts) -> str:
    
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

#create desired date range 
date_index = pd.period_range(start='2017-06-03', end='2017-07-01', freq= 'D')

resp = []

my_list = []


#pull all daily data from Polygon in date range
for i in date_index:
    
    with RESTClient(key) as client:
        
        resp.append(client.stocks_equities_grouped_daily(locale = "us", market = "stocks", date = i, unadjusted=False))
      
        # create dataframe for each iteration, ignoring weekends
        if resp.resultsCount > 0:
            
            df = pd.DataFrame(resp.results)
            
            # add the df dataframe into the my_list
            my_list.append(df)
      


    
      
dir(resp)

print(resp.count)

print(resp.results[0:5])


df.rename(columns = {'o':'Open',
                     'h':'High',
                     'l':'Low',
                     'c':'Close',
                     'v':'Volume',
                     'vw':'VWAP',
                     'n':'Adjusted Close',
                     't':'DateTimeUnix'}, inplace=True)

df['DatetimeUTC'] = pd.to_datetime(df["DateTimeUnix"].apply(lambda x: ts_to_datetime(x)))
df['DatetimeEst'] = pd.to_datetime(df['DatetimeUTC'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('US/Eastern')

