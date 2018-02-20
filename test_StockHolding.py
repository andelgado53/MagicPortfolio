from unittest import TestCase
from unittest.mock import Mock, patch
import unittest
from StockHolding import StockHolding
from datetime import datetime

class testStockDataFetcher(TestCase):
    
    def setUp(self):
        self.subject = StockHolding('AMZN', 100, '2017-12-01', '50', '65')
        self.assertIsInstance(self.subject, StockHolding)
    
    def test_init(self):
        subject = StockHolding('AMZN', '100', '2017-12-01', '50', '65')
        self.assertIsInstance(subject, StockHolding)
    
    def test_init_when_wrong_units_type(self):
        self.assertRaises(ValueError, StockHolding, 'AMZN', 'A', '2017-12-01', '50', '65')
    
    def test_init_when_wrong_date_format(self):
        self.assertRaises(ValueError, StockHolding, 'AMZN', 100, '127-12-01', '50', '65')
    
    def test_init_when_wrong_buy_price_type(self):
        self.assertRaises(ValueError, StockHolding, 'AMZN', '100', '2017-12-01', 'AAAA', '65')
    
    def test_init_when_wrong_current_price_type(self):
        self.assertRaises(ValueError, StockHolding, 'AMZN', '100', '2017-12-01', '50', 'AAA')
    
    def test_set_current_price(self):
        self.subject.set_current_price('100')
        self.assertEqual(100, self.subject.current_price)
        self.subject.set_current_price('65')
    
    def test_set_current_price_when_input_is_not_numeric(self):
        self.assertRaises(ValueError, self.subject.set_current_price, 'jdhdhdh')
   
    def test_get_current_price(self):
        response = self.subject.get_current_price()
        self.assertEqual(response, 65)
    
    def test_get_holding_profit(self):
        response = self.subject.get_holding_profit()
        entry_profit = (65.0*100) - (100*50.0)
        self.assertEqual(response, entry_profit)
    
    @patch('StockHolding.datetime')
    def test_get_holding_days(self, datetime_mock):
        datetime_mock.today.return_value = datetime.strptime('2017-12-03', '%Y-%m-%d')
        response = self.subject.get_holding_days()
        datetime_mock.today.assert_called()
        self.assertEqual(response, 2)
    
    def test_get_initial_investment(self):
        response = self.subject.get_initial_investment()
        initial_investment = 100 * 50.0
        self.assertEqual(response, initial_investment)
    
    def test_get_current_value(self):
        response = self.subject.get_current_value()
        current_value = 100 * 65.0
        self.assertEqual(response,current_value)
    
    def test_get_percent_growth(self):
        response = self.subject.get_percent_growth()
        percent_growth = 15.0/50.0
        self.assertEqual(response, percent_growth)


if __name__ == '__main__':
    unittest.main()
