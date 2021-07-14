import pandas

import matplotlib
# assign the value to the investment dates
def map_investment_value(date, strategy):
    try:
        return strategy[date]['value']
    
    except:
        return 0


# %%
# calculate portfolio holding
class Portfolio(object):

    def __init__(self, index_data, strategy, price = 'Open', portfolio_name = 'portfolio'):
        # simulation of the portfolio
        # assumption: using open price  

        # portfolio_data = index_data[['Date', 'Date_dt']]
        portfolio_data = index_data[['Date', 'Date_dt']]
        portfolio_data['index_level'] = index_data[price]

        portfolio_data['inc_value'] = \
            portfolio_data.apply(lambda x: map_investment_value(x['Date_dt'], strategy), axis = 1)

        portfolio_data['inc_unit'] = \
            portfolio_data.apply(lambda x: x['inc_value']/x['index_level'], axis = 1)

        portfolio_data['acc_value'] = \
            portfolio_data['inc_value'].cumsum()

        portfolio_data['acc_unit'] = \
            portfolio_data['inc_unit'].cumsum()

        portfolio_data['portfolio_position'] = \
            portfolio_data['acc_unit'] * portfolio_data['index_level']


        self.portfolio_data = portfolio_data
        self.portfolio_name = portfolio_name
    
    def plot(self):


        self.portfolio_data.plot(
            x = 'Date_dt', 
            y = [
                'portfolio_position',
                'acc_value',
                'index_level',
                'inc_value',
            ],
            title = self.portfolio_name
        )
