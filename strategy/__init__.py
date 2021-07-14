
# %%
from datetime import datetime as dt, timedelta
date_format = '%Y-%m-%d'

class Strategy(object):

    '''
    Will generate an investment cashflow schedule

    e.g. strategy = {
        '2000-01-03': {"value": 100},
        '2002-01-03': {"value": 200},
        '2004-01-03': {"value": 100},
        '2006-01-03': {"value": 300},
        '2008-01-03': {"value": -100},
        '2022-01-03': {"value": 100},
    }
    '''

    def fixed_amount_per_period(self, start_date_df, end_date_df, days = 30, amount = 100):

        '''
            start_date, end_date in df
            days - period in days
        '''
        strategy = {}

        tmp = start_date_df

        while tmp < end_date_df:
            strategy[tmp] = {'value': amount}
            tmp = tmp + timedelta(days = 30)


        return strategy



# start_date = dt(2001,1,1)
# end_date = dt(2020,1,1)

# Strategy().fixed_amount_per_period(start_date_df = start_date, end_date_df = end_date)



    
# %%

    def clean(strategy, market_dates):
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

#%%
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

