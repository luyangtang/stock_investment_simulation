
# %%
from datetime import datetime as dt, timedelta


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
