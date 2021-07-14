#%%
# Import yfinance
import yfinance as yf  
import pandas as pd
import warnings
from datetime import datetime as dt
date_format = '%Y-%m-%d'

class StockData(object):

    def __init__(self, symbol, start = '2000-01-01', end = '2020-04-20', loadFromApi = True, exportDataTo = None, dataPath = None, date_format = date_format):

        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = pd.DataFrame()
        
        self.flag = 0 # for test cases


        # a load from api
        if loadFromApi:
            
            try:
            
                # Get the data for the stock symbol by specifying the stock ticker, start date, and end date
                self.data = yf.download(self.symbol, self.start, self.end)
                self.flag = 1

                
                # export the data if exportData = True
                if exportDataTo:
                    self.data.to_csv(exportDataTo)

                    self.flag = 2

            
            except Exception as err:
                print(err)
        

        # else get data from dataPath specified
        elif dataPath:

            try:

                # read data into df from the specified path
                self.data = pd.read_csv(dataPath)
                self.flag = 3

            
            except Exception as err:
                print(err)


        # raise an error if dataPath not provided
        else:
            
            raise(Exception('dataPath must be provided if not loading from api'))

        
        index_data = pd.DataFrame(self.data.to_records())
        
        try:
            index_data['Date_dt'] = index_data['Date'].apply(lambda x: dt.strptime(x, date_format))
        except:
            index_data['Date_dt'] = index_data['Date']
        market_dates = index_data['Date_dt']

        self.index_data = index_data
        self.market_dates = market_dates



        # show warning if no data created
        if self.data.empty:
            warnings.warn('No data loaded')

    
    def getData(self):

        return {
            "index_data": self.index_data,
            "market_dates": self.market_dates
        }



#%%
# data = StockData(
#     symbol = 'IVV'
# ).getData()
