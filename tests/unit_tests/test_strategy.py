import unittest

# %% Strategy

import random
from datetime import datetime as dt

target = __import__("strategy")
InvestAmount = target.InvestAmount


class TestInvestAmount(unittest.TestCase):

    def test_fixedAmount(self):

        amount = random.random() * 1000
        date = '2020-01-01'
        dateobj = dt.strptime(date, '%Y-%m-%d')

        # date as a string
        self.assertEqual(
            InvestAmount().FixedAmount(
                date = date, 
                amount = amount
            )[dateobj], 
            amount
        )

        # date as a datetime obj
        self.assertEqual(
            InvestAmount().FixedAmount(
                date = dateobj, 
                amount = amount
            )[dateobj], 
            amount
        )

        # wrong date format
        self.assertRaises(
            TypeError,
            InvestAmount().FixedAmount,
            'hello',
            amount
        )

        # wrong amount type
        self.assertRaises(
            TypeError,
            InvestAmount().FixedAmount,
            date,
            'amount'
        )



AIPStrategy = target.AIPStrategy

class TestAIPStrategy(unittest.TestCase):

    def test_APIStrategyInit(self):

        
        self.assertListEqual(
            AIPStrategy('2020-01-01', 1, amount = 1).getDates(), 
            [dt.strptime('2020-01-01', '%Y-%m-%d')]
        )

        self.assertListEqual(
            AIPStrategy(['2020-01-01'], 1, amount = 1).getDates(), 
            [dt.strptime('2020-01-01', '%Y-%m-%d')]
        )

        print(AIPStrategy(['2020-01-01', '2020-01-02'], 1, amount = 1).getPlan())



if __name__ == '__main__':
    unittest.main()


