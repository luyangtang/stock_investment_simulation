

from datetime import datetime as dt
import pandas as pd
import sys

StockData = __import__('dataFetch').StockData


class Simulator(object):

    def __init__(self, stockSymbol, strategy, **kwargs):

        '''
        stockSymbol: str
            e.g. IVV
        
        strategy: Strategy

        **kwargs:
            loadFromApi: bool (see dataFetch.StockData)
            dataPath: str (see dataFetch.StockData)
            priceMode: str from Open, Close, High, Low, Adj Close, Volume
        '''


        # resolve kwarg paramaters
        loadFromApi = kwargs['loadFromApi'] if 'loadFromApi' in kwargs.keys() else True
        dataPath = kwargs['dataPath'] if 'dataPath' in kwargs.keys() else None
        self.priceMode = kwargs['priceMode'] if 'priceMode' in kwargs.keys() else 'Open'

        # get data
        try:
            self.data = StockData(
                symbol = 'IVV',
                loadFromApi = loadFromApi, 
                dataPath = dataPath
            ).getData()


        except Exception as err:

            print('Data failed to load: %s') % err
            sys.exit(1)


        # raise exception if data is empty
        if self.data.empty:
            raise ValueError("No stock data loaded")

        else:

            # get strategy plan
            self.plan = strategy.getPlan()


            # simulate
            self.totalAmountInvested = 0
            self.totalQuantityInvested = 0
            portfolioValue = 0
            


            # Initialise
            self.timeseriesData = []
            pricePerShare = None



            # simulate portfolio timeseries
            for date in self.plan:

                
                # check if the planned date is a business date/exist in the data else skip it
                if date in self.data.index:

                    # get the price
                    pricePerShare = self.data[self.priceMode][date]

                    # get the investamount based on strategy
                    amount = self.plan[date]

                    # calculate quantity and cumulatives
                    quantity = amount / pricePerShare
                
                    self.totalQuantityInvested += quantity
                    self.totalAmountInvested += amount

                    # calculate portfolio value
                    portfolioValue = pricePerShare * self.totalQuantityInvested

                    # append to timeseries data
                    self.timeseriesData += [{
                        'Date': date,
                        'PricePerShare': pricePerShare,
                        'Quantity': quantity,
                        'TotalQuantityInvested': self.totalQuantityInvested,
                        'TotalAmountInvested': self.totalAmountInvested,
                        'PortfolioValue': portfolioValue,
                        'AvgBoughtPrice': self.totalAmountInvested / self.totalQuantityInvested
                    }
                    ]
                
                else:
                    pass


    def getTsData(self):

        return self.timeseriesData

    
    def getTsDf(self):

        return pd.DataFrame(self.timeseriesData)


