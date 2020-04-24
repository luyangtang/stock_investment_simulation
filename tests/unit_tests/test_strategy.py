import unittest

# %% Strategy

import random
from datetime import datetime as dt

target = __import__("strategy")
InvestAmount = target.InvestAmount
Timetable = target.Timetable


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

        
        self.assertSequenceEqual(
            AIPStrategy('2020-01-01', 1, amount = 1).getDates(), 
            [dt.strptime('2020-01-01', '%Y-%m-%d')]
        )

        self.assertSequenceEqual(
            AIPStrategy(['2020-01-01'], 1, amount = 1).getDates(), 
            [dt.strptime('2020-01-01', '%Y-%m-%d')]
        )

        # construct from timetable object
        self.assertSequenceEqual(
            AIPStrategy(Timetable(['2020-01-01']), 1, amount = 1).getDates(), 
            [dt.strptime('2020-01-01', '%Y-%m-%d')]
        )

        # test amount
        amount = random.random()
        self.assertEqual(
            AIPStrategy(dt(2020,1,1), 1, amount = amount).getPlan()[dt(2020,1,1)],
            amount
        )

        self.assertEqual(
            AIPStrategy(dt(2020,1,1), 1).getPlan()[dt(2020,1,1)],
            AIPStrategy(dt(2020,1,1), 1).defaultAmount
        )

        
        



class TestTimetable(unittest.TestCase):

    def test_timetableInit(self):

        # a single date
        self.assertSequenceEqual(
            Timetable('2020-01-01').get(), 
            [dt(2020,1,1)]
        )

        # list of date strings
        self.assertSequenceEqual(
            Timetable(['2020-01-01']).get(), 
            [dt(2020,1,1)]
        )

        self.assertCountEqual(
            Timetable(['2020-01-01', '2020-01-02']).get(), 
            [dt(2020,1,1), dt(2020,1,2)]
        )

        # wrong format 
        self.assertRaises(
            Exception,
            # Timetable(['Hello']).get(),
            Timetable,
            ['hello']
        )

        # correct constructor
        self.assertEqual(
            Timetable(['2020-01-01', '2020-01-02']).constructorType,
            'constructFromList'
        )

        # wrong format 
        self.assertRaises(
            Exception,
            # Timetable(['Hello']).get(),
            Timetable,
            [1]
        )
    

    def test_timetableCopyConstructor(self):

        # copy constructor
        timetable = Timetable('2020-01-01')

        self.assertEqual(
            Timetable(timetable).constructorType,
            'copyConstructor'
        )

        self.assertSequenceEqual(
            Timetable(timetable).timetable,
            timetable.timetable
        )






if __name__ == '__main__':
    unittest.main()


