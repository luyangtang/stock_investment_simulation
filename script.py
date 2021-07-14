
#%%
# 
from numpy import datetime_as_string
from numpy.core.numeric import roll
import pandas as pd
from datetime import datetime as dt


from strategy import Strategy
from portfolio import Portfolio
from dataFetch import StockData


#%%
start = '2000-01-01'
end = '2020-04-20'

# from API
# data = StockData('IVV', start = start, end = end, dataPath='./tests/test_stock_data').getData()

data = StockData('IVV', start = start, end = end, loadFromApi = False, dataPath='./tests/test_stock_data').getData()

#%%
index_data = data["index_data"]
market_dates = data["market_dates"]

start_date = dt.strptime(start, '%Y-%M-%d')
end_date = dt.strptime(end, '%Y-%M-%d')


#%% fixed_amount_per_period
strategy = \
    Strategy().fixed_amount_per_period(start_date_df = start_date, end_date_df = end_date)
cleaned_strategy = Strategy.clean(strategy, market_dates)

fixex_amount_portfolio = Portfolio(index_data, cleaned_strategy, portfolio_name = 'fixed_amount').plot()
# %%
