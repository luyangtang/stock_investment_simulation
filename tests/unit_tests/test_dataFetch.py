
import unittest
import os

# DataFetch

#%% stock

target = __import__("dataFetch")
StockData = target.StockData

class TestStockDataInit(unittest.TestCase):

    def test_load_from_api(self):
        """
        Test that it can load data from api
        """
        symbol = 'IVV'
        start = '2019-01-01'
        end = '2020-01-01'
        
        stockData = StockData(
            symbol = symbol,
            start = start,
            end = end,
            loadFromApi = True,
            exportDataTo = False,
            dataPath = None
        )

        self.assertEqual(stockData.flag, 1)
        self.assertFalse(stockData.data.empty)
        # can also check if min = start, max = end


    
    def test_load_from_api_with_export(self):
        """
        Test that it can load data from api
        """
        symbol = 'IVV'
        start = '2019-01-01'
        end = '2020-01-01'
        exportDataTo = './test_data_export.csv'
        
        stockData = StockData(
            symbol = symbol,
            start = start,
            end = end,
            loadFromApi = True,
            exportDataTo = exportDataTo,
            dataPath = None
        )

        self.assertEqual(stockData.flag, 2)
        self.assertFalse(stockData.data.empty)
        self.assertTrue(os.path.isfile(exportDataTo))
        # remove the file
        os.remove(exportDataTo)
        # can also check if min = start, max = end


    
    def test_load_from_file(self):
        """
        Test that it can load data from file
        """
        symbol = 'IVV'
        start = '2019-01-01'
        end = '2020-01-01'
        dataPath = './tests/test_stock_data'

        stockData = StockData(
            symbol = symbol,
            start = start,
            end = end,
            loadFromApi = False,
            exportDataTo = None,
            dataPath = dataPath
        )

        self.assertEqual(stockData.flag, 3)
        self.assertFalse(stockData.data.empty)

    



if __name__ == '__main__':
    unittest.main()
