
#%%
# 
from numpy import datetime_as_string
from numpy.core.numeric import roll
import pandas as pd

index_data = pd.read_csv('./tests/test_stock_data')
# %%

from datetime import datetime as dt
date_format = '%Y-%m-%d'
index_data['Date_dt'] = index_data['Date'].apply(lambda x: dt.strptime(x, date_format))
market_dates = index_data['Date_dt']

# the first date when an investment is made
# roll to the next business date
def roll_date(date, market_dates):
    '''
    Rolls a single date to the next business date (according to the market data)
    date format allowed: '%Y-%m-%d'
    '''

    if isinstance(date, dt):
        pass
    
    else:
        try:
            date = dt.strptime(date, date_format)
        
        except Exception as e:
            raise Exception('Incorrect date format')

    # see if the entry date is in the index_data
     # all dates present in stock data
    later_dates = [i for i in market_dates if i >= date] # dates later than entry date

    if date in later_dates:
        # no need to roll
        return date

    elif len(later_dates) > 0:
        # roll to the next date if it exists. This will be a timestamp to be converted to dt
        return min(later_dates).to_pydatetime()

    else:
        # cannot roll - throw exception
        raise Exception('invalid entry date. No further dates present in market data')


# print(roll_date('2019-01-01', market_dates))
# print(roll_date('2019-01-03', market_dates))
# print(roll_date('2021-01-01', market_dates))

# %%
def roll_date_array(dates, market_dates):
    '''
    roll an array of dates by iteratively calling roll_date
    date format allowed: '%Y-%m-%d'
    Any invalid dates will be discarded
    '''

    rolled_dates = []

    for date in dates:
        try:
            rolled_dates += [roll_date(date, market_dates)]
        
        except Exception as e:
            print(Warning('%s cannot be rolled due to "%s"' % (date, e)))

    return rolled_dates


# tests:
dates = ['2019-01-01', '2019-01-03', '2021-01-01']
rolled_dates = roll_date_array(dates, market_dates)
print(rolled_dates)
print([i in list(market_dates) for i in rolled_dates])


#%%
from strategy import Strategy

start_date = dt(2001,1,1)
end_date = dt(2020,1,1)

strategy = \
    Strategy().fixed_amount_per_period(start_date_df = start_date, end_date_df = end_date)






# %%
# clean the strategy dates
# value based strategy

# strategy = {
#     '2000-01-03': {"value": 100},
#     '2002-01-03': {"value": 200},
#     '2004-01-03': {"value": 100},
#     '2006-01-03': {"value": 300},
#     '2008-01-03': {"value": -100},
#     '2022-01-03': {"value": 100},
# }



def clean_strategy(strategy):
    # roll dates
    dates = list(strategy.keys())
    for date in dates:
        '''
        clean up strategy dates to rolled dates
        strategy = {
            '2000-01-03': {"value": 100},
            '2002-01-03': {"value": 200},
            '2004-01-03': {"value": 100},
            '2006-01-03': {"value": 300},
            '2008-01-03': {"value": -100},
            '2022-01-03': {"value": 100},
        }

        '''
        try:
            # replace the dates by rolled dates
            rolled_date = roll_date(date, market_dates)
            # replace the original key
            strategy[rolled_date] = strategy.pop(date)
        
        except Exception as e:
            # will be discarded
            strategy.pop(date)
            print('Failed to roll %s due to "%s"' % (date, e))
        
        
    return strategy


cleaned_strategy = clean_strategy(strategy)
# %%
# calculate portfolio holding
# index_data[index_data['Date_dt'] == list(cleaned_strategy.keys())[0]]
# %%
# assign the value to the investment dates
def map_investment_value(date, strategy):
    try:
        print(strategy[date])
        return strategy[date]['value']
    
    except:
        return 0

# simulation of the portfolio
# assumption: using open price
price = 'Open'
portfolio_data = index_data[['Date', 'Date_dt']]
portfolio_data['index_level'] = index_data[price]

portfolio_data['inc_value'] = \
    portfolio_data.apply(lambda x: map_investment_value(x['Date_dt'], cleaned_strategy), axis = 1)

portfolio_data['inc_unit'] = \
    portfolio_data.apply(lambda x: x['inc_value']/x['index_level'], axis = 1)

portfolio_data['acc_value'] = \
    portfolio_data['inc_value'].cumsum()

portfolio_data['acc_unit'] = \
    portfolio_data['inc_unit'].cumsum()

portfolio_data['portfolio_position'] = \
    portfolio_data['acc_unit'] * portfolio_data['index_level']


portfolio_data
# %%
import matplotlib

portfolio_data.plot(
    x = 'Date_dt', 
    y = [
        'portfolio_position',
        'acc_value',
        'index_level',
        'inc_value',
    ]
)
# %%

map_investment_value(portfolio_data[portfolio_data['Date_dt'] == dt(2019,4,29)], clean_strategy)
# %%
