
# %%

from datetime import datetime as dt
from collections.abc import Iterable
import warnings

class Strategy(object):

    def __init__(self):

        # plan: key-value pai
        self.plan = {}

        # # This should be an abstract class
        # raise NotImplementedError


    def getPlan(self):

        return self.plan
    
    def getDates(self):

        return list(self.plan.keys())




class AIPStrategy(Strategy):

    '''
    Automatic Investment Plan Strategy

    timetable: instance of Timetable
    
    investAmountType: callable taking date as an object with a numeric output
        this amount will be invested (allowing fraction of share invested) on the given date

    **kwargs:
        parameters to be consumed by investAmountType
    '''

    # static variables
    defaultAmount = 100

    def __init__(self, timetable, investAmountType, **kwargs):
        
        '''
        kwargs: amount
        '''

        super().__init__()

        # convert timetable to a timetable
        timetable = Timetable(timetable)

        # get amount from kwargs if any other default to 100
        amount = kwargs['amount'] if 'amount' in kwargs.keys() else self.defaultAmount

        
        # convert the timetable elements to datetime
        for date in timetable.timetable:

            try:

                # add the date - amount to self.plan
                self.plan.update(InvestAmount().FixedAmount(date = date, amount = amount))

            except Exception as err:
                print(err)
                warnings('Warning: %s is removed from the timetable due to %s' % (date, err))

        

class Timetable(object):

    def __init__(self, timetable):

        '''
        timetable: list of date as str '%Y-%m-%d' or datetime obj
        if there's no quote on one of the quote, it will be ignored with a warning
        cannot be repeated
        '''
        self.constructorType = 0

        # copy constructor
        if isinstance(timetable, Timetable):

            self.constructorType = 'copyConstructor'
            self.timetable = timetable.timetable

        
        # if timetable is given as a list
        else:
            self.constructorType = 'constructFromList'

            # take unique values only
            timetable = list(set(timetable)) if (isinstance(timetable, Iterable) and not isinstance(timetable, str)) else [timetable]
            
            self.timetable = []

            # convert the timetable elements to datetime
            for date in timetable:

                if isinstance(date, dt):
                    self.timetable += [date]

                else: 
                    try:

                        # add the date - amount to self.plan
                        self.timetable += [dt.strptime(date, '%Y-%m-%d')]

                    except Exception as err:
                        print(err)
                        warnings('Warning: %s cannot be converted due to %s' % (date, err))
                
            


    def get(self):

        return self.timetable



import numbers
from datetime import datetime as dt

class InvestAmount(object):

    def FixedAmount(self, date = None, amount = None):

        '''
        date: '%Y-%m-%d'

        positive amount: buy
        negative amount: withdraw 
        '''
        if not isinstance(date, dt):

            # convert it to a dt obj
            try:
                date = dt.strptime(date, '%Y-%m-%d')
            
            except:
                raise TypeError


        # check input type: only allow number
        if not isinstance(amount, numbers.Number):

            raise TypeError

        return {date: amount}
