import requests
from configuration import price_api_key
import pprint 

class StockDataFetcher:

    def __init__(self, symbol):
        self.api_price_response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}'.format(symbol=symbol, key=price_api_key)).json()
        self.response_metadata = self._get_stock_price_time_series_metadata()

    def _get_stock_price_time_series_data(self):
        return self.api_price_response
    
    def _get_stock_price_time_series_metadata(self):
        try:
            return self.api_price_response['Meta Data']
        except KeyError:
            raise KeyError('Invalid Stock Symbol')

    def _remove_timestamp_from_date(self, date):
        return date[0:10]

    def get_stock_latest_close_price(self):
        last_price_date = self.get_stock_last_refreshed_date()
        latest_price_at_close = self.get_close_price_at(last_price_date)
        return latest_price_at_close

    def get_stock_last_refreshed_date(self):
        return self._remove_timestamp_from_date(self.response_metadata['3. Last Refreshed'])
        
    def get_close_price_at(self, date):
        return float(self.api_price_response['Time Series (Daily)'][date]['4. close'])

