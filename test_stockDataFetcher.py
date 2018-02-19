from unittest import TestCase
from unittest.mock import Mock, patch
from StockDataFetcher import StockDataFetcher
import unittest
import json

def mock_return(stock):
    return {'Meta Data': {'1. Information': 'Daily Prices (open, high, low, close) and Volumes',
            '2. Symbol': 'AMZN',
            '3. Last Refreshed': '2017-09-27',
            '4. Output Size': 'Compact',
            '5. Time Zone': 'US/Eastern'},
    'Time Series (Daily)': {'2017-09-26': {'1. open': '945.4900',
                                        '2. high': '948.6300',
                                        '3. low': '931.7500',
                                        '4. close': '938.6000',
                                        '5. volume': '3464183'},
                        '2017-09-27': {'1. open': '948.0000',
                                        '2. high': '955.3000',
                                        '3. low': '943.3000',
                                        '4. close': '950.8700',
                                        '5. volume': '3111263'}
    }}


class testStockDataFetcher(TestCase):
    
    @patch('StockDataFetcher.requests')
    def setUp(self, mock_requests):
        mock_requests.get.return_value.json.return_value = mock_return('AMZN')
        self.subject = StockDataFetcher('AMZN')
    
    @patch('StockDataFetcher.requests')
    def test_init_whith_valid_symbol(self, mock_requests):
        subject = StockDataFetcher('AAPL')
        mock_requests.get.return_value.json.assert_called()
        self.assertIsInstance(subject, StockDataFetcher)

    @patch('StockDataFetcher.requests')
    def test_init_whith_invalid_symbol(self, mock_requests):
        mock_requests.get.return_value.json.return_value = {'no valid': 'no valid'}
        subject = Mock(spec=StockDataFetcher)
        subject.side_effect = KeyError('Invalid Stock Symbol')
        self.assertRaises(KeyError, subject, 'lalalalalala')

    @patch('StockDataFetcher.requests')
    def test_get_stock_price_time_series_data(self, mock_requests):
        response = self.subject._get_stock_price_time_series_data()
        self.assertEqual(response, mock_return('AMZN'))

    def test_get_stock_price_time_series_metadata(self):
        response = self.subject._get_stock_price_time_series_metadata()
        self.assertEqual(response, mock_return('AMZN')['Meta Data'])

    def test_get_stock_latest_close_price(self):
        response = self.subject.get_stock_latest_close_price()
        self.assertEqual(response, float(mock_return('AMZN')['Time Series (Daily)']['2017-09-27']['4. close']))
    
    def test_get_stock_last_refreshed_date(self):
        response = self.subject.get_stock_last_refreshed_date()
        self.assertEqual(response, mock_return('AMZN')['Meta Data']['3. Last Refreshed'])
    
    def test_get_close_price_at(self):
        response = self.subject.get_close_price_at('2017-09-27')
        self.assertEqual(response, float(mock_return('AMZN')['Time Series (Daily)']['2017-09-27']['4. close']))
    
    def test_remove_time_stamp_when_date_has_timestamp(self):
        response = self.subject._remove_timestamp_from_date('2017-10-12 12:12:55')
        self.assertEqual(response, '2017-10-12')

    def test_remove_time_stamp_when_date_has_no_timestamp(self):
        response = self.subject._remove_timestamp_from_date('2017-10-12')
        self.assertEqual(response, '2017-10-12')


if __name__ == '__main__':
    unittest.main()




