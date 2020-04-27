import unittest
import random
import pandas as pd
import os


Simulator = __import__("simulator").Simulator
Strategy = __import__("strategy").AIPStrategy
InvestAmount = __import__("strategy").InvestAmount
Timetable = __import__("strategy").Timetable



class TestSimulator(unittest.TestCase):

    def test_simulatorInitNoData(self):
        timetable = Timetable([
            '2020-03-12',
            '2020-03-13',
            '2020-03-14',
            '2020-03-15',
            '2020-03-16',
            '2020-03-17',
            '2020-03-18',
            '2020-03-19',
        ])

        amount = random.random() * 100

        strategy = Strategy(
                timetable = timetable, 
                investAmountType = InvestAmount.FixedAmount,
                amount = amount
            )

        kwargs = {
            'stockSymbol': 'IVV',
            'strategy': strategy,
            'loadFromApi': False,
            'dataPath': 'test_stock_data' # wrong path - will raise exception
        }
        
        self.assertRaises(
            ValueError,
            Simulator,
            **kwargs
        )

        

    def test_simulatorPriceMode(self):

        timetable = Timetable([
            '2020-03-12',
            '2020-03-13',
            '2020-03-14',
            '2020-03-15',
            '2020-03-16',
            '2020-03-17',
            '2020-03-18',
            '2020-03-19',
        ])

        amount = random.random() * 100

        strategy = Strategy(
                timetable = timetable, 
                investAmountType = InvestAmount.FixedAmount,
                amount = amount
            )


        self.assertFalse(Simulator(
            stockSymbol = 'IVV',
            strategy = strategy,
            priceMode = 'High'
        ).getTsDf().empty)




    def test_simulatorFromFile(self):

        timetable = Timetable([
            '2020-03-12',
            '2020-03-13',
            '2020-03-14',
            '2020-03-15',
            '2020-03-16',
            '2020-03-17',
            '2020-03-18',
            '2020-03-19',
        ])

        amount = random.random() * 100

        strategy = Strategy(
                timetable = timetable, 
                investAmountType = InvestAmount.FixedAmount,
                amount = amount
            )


        simulator = Simulator(
            stockSymbol = 'IVV',
            strategy = strategy,
            loadFromApi = False,
            dataPath = '%s/tests/test_stock_data' % os.path.abspath(os.getcwd())
        )

        self.assertFalse(simulator.getTsDf().empty)




    def test_simulatorInit(self):

        timetable = Timetable([
            '2020-03-12',
            '2020-03-13',
            '2020-03-14',
            '2020-03-15',
            '2020-03-16',
            '2020-03-17',
            '2020-03-18',
            '2020-03-19',
        ])

        amount = random.random() * 100

        strategy = Strategy(
                timetable = timetable, 
                investAmountType = InvestAmount.FixedAmount,
                amount = amount
            )


        simulator = Simulator(
            stockSymbol = 'IVV',
            strategy = strategy
        )

        # check if amount being invested matches the planned amount based on strategy
        for i in timetable.get():
            self.assertEqual(
                amount,
                strategy.getPlan()[i]
            )

        # Validate output timeseries data
        tsDf = simulator.getTsDf()


        self.assertTrue(all(tsDf['TotalAmountInvested'] == tsDf['AvgBoughtPrice'] * tsDf['TotalQuantityInvested']))
        # print(pd.DataFrame(simulator.timeseriesData))





if __name__ == '__main__':
    unittest.main()
