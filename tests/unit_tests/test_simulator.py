import unittest
import random


Simulator = __import__("simulator").Simulator
Strategy = __import__("strategy").AIPStrategy
InvestAmount = __import__("strategy").InvestAmount
Timetable = __import__("strategy").Timetable



class TestSimulator(unittest.TestCase):


    def test_simulatorInit(self):

        timetable = Timetable([
            '2020-03-12',
            '2020-03-13',
            '2020-03-14',
            '2020-03-15',
        ])

        amount = random.random()

        strategy = Strategy(
                timetable = timetable, 
                investAmountType = InvestAmount.FixedAmount,
                amount = amount
            )


        simulator = Simulator(
            stockSymbol = 'IVV',
            strategy = strategy
        )

        for i in timetable.get():
            self.assertEqual(
                amount,
                strategy.getPlan()[i]
            )