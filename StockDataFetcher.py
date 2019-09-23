import requests
import pprint 


class StockDataFetcher:

    def __init__(self, symbol):
        self.symbol = symbol
        self.stock_url = 'https://api.worldtradingdata.com/api/v1/stock?symbol={symbol}&api_token=79WwFfHvhdnUyR9P1sU3HKHVfCbCoMrM4rDDOWhaFc8Q7c1rbqannIPbyLTN'
    
    def get_price(self):
        try:
            return requests.get(self.stock_url.format(symbol=self.symbol)).json()['data'][0]['price']
        except Exception as ex:
            print(ex)
            print('Could not get price data for: ' + self.symbol)


# print(requests.get('https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_3c270db17f5b460390fe6bc18874b6ab').json()['iexRealtimePrice'])
# print(requests.get('https://api.worldtradingdata.com/api/v1/stock?symbol=AAPL&api_token=79WwFfHvhdnUyR9P1sU3HKHVfCbCoMrM4rDDOWhaFc8Q7c1rbqannIPbyLTN').json()['data'][0]['price'])

# print(requests.get('https://api.worldtradingdata.com/api/v1/stock?symbol={symbol}&api_token=79WwFfHvhdnUyR9P1sU3HKHVfCbCoMrM4rDDOWhaFc8Q7c1rbqannIPbyLTN'.format(symbol='AAPL')).json())