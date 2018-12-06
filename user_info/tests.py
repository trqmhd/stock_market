'''import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
from matplotlib import style


style.use('ggplot')

start = dt.datetime(2015,1,5)
end = dt.datetime(2018,9,9)

df = web.DataReader('TSLA','yahoo', start, end)

print(df.head())
'''

from faker import Faker

fakegen = Faker()
for x in range(9):
    xi = fakegen.date(pattern="%Y-%m-%d", end_datetime=None)
    print(xi)

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
tickers = ['INTL']

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2018-10-29'
end_date = '2018-10-31'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = data.DataReader(tickers, 'yahoo', start_date, end_date)

list_of_lists = [7, 2, 4, 9, 5]
for x in range(1):
    print(list_of_lists[0:3])

print(panel_data[1:2])
# export DJANGO_SETTINGS_MODULE=stock_market.settings

# from stock_info.models import StockInfo
# p1 = StockInfo.objects.create(symbol='TSLA',date='2018-10-29',high=212.343242, low=205.371837, open= 210.827927, close = 210.312838, volume= 834328, adj_close = 211.763987)


# Getting just the adjusted closing prices. This will return a Pandas DataFrame
# The index in this DataFrame is the major index of the panel_data.
close = panel_data['Close']

# Getting all weekdays between 01/01/2000 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

# How do we align the existing prices in adj_close with our new set of dates?
# All we need to do is reindex close using all_weekdays as the new index
close = close.reindex(all_weekdays)

# Reindexing will insert missing values (NaN) for the dates that were not present
# in the original set. To cope with this, we can fill the missing by replacing them
# with the latest available price for each instrument.
close = close.fillna(method='ffill')

print(all_weekdays)

# DatetimeIndex(['2010-01-01', '2010-01-04', '2010-01-05', '2010-01-06',
#               '2010-01-07', '2010-01-08', '2010-01-11', '2010-01-12',
#               '2010-01-13', '2010-01-14',
#               ...
#               '2016-12-19', '2016-12-20', '2016-12-21', '2016-12-22',
#               '2016-12-23', '2016-12-26', '2016-12-27', '2016-12-28',
#               '2016-12-29', '2016-12-30'],
#              dtype='datetime64[ns]', length=1826, freq='B')


close.head(10)

print(close.describe())





import pandas as pd
# import pandas.io.data as web# Package and modules for importing data; this code may change depending on pandas version
import datetime
from pandas_datareader import data

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2016, 1, 1)
end = datetime.date.today()

# Let's get Apple stock data; Apple's ticker symbol is AAPL
# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
apple = data.DataReader("AAPL", "yahoo", start, end)

type(apple)

apple.head()
