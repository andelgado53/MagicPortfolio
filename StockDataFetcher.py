import requests
import pprint 


class StockDataFetcher:

    def __init__(self, symbol):
        self.symbol = symbol
        self.stock_url = 'https://api.iextrading.com/1.0/stock/{symbol}/{api}'
    
    def get_price(self):
        try:
            return requests.get(self.stock_url.format(symbol=self.symbol, api='price')).json()
        except :
            print('Could not get price data for: ' + self.symbol)


# print(requests.get('https://api.iextrading.com/1.0/stock/{symbol}/price'.format(symbol='CJREF')).json())
