

from datetime import datetime as dt
import pandas as pd


class Simulator(object):

    def __init__(self, stockSymbol, strategy):

        '''
        stockSymbol: str
            e.g. IVV
        
        strategy: Strategy
        '''

        # get data
        self.data = StockData(
            symbol = 'IVV'
        ).getData()

        # get strategy plan
        self.plan = strategy.getPlan()



        self.totalAmountInvested = 0
        self.totalQuantityInvested = 0
        portfolioValue = 0
        
        
        priceMode = 'Open'


        self.timeseriesData = []

        for date in plan:

            # get the investamount based on strategy
            amount = self.plan[date]

            # get the price
            pricePerShare = self.data[priceMode][date]

            # calculate quantity and cumulatives
            quantity = amount / pricePerShare
            self.totalQuantityInvested += quantity
            self.totalAmountInvested += amount

            # calculate portfolio value
            portfolioValue = pricePerShare * self.totalQuantityInvested

            self.timeseriesData += [{
                'Date': date,
                'PricePerShare': pricePerShare,
                'Quantity': quantity,
                'TotalAmountInvested': self.totalAmountInvested,
                'PortfolioValue': portfolioValue,
                'AvgBoughtPrice': self.totalAmountInvested / self.totalQuantityInvested
            }
            ]


    def getTsData(self):

        return self.timeseriesData

    
    def getTsDf(self):

        return pd.DataFrame(self.timeseriesData)


