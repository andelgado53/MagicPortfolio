import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import requests
import json
import collections
from datetime import date
from StockHolding import StockHolding
from Portfolio import Portfolio
from configuration import price_api_key


scope = ['http://spreadsheets.google.com/feeds']
current_price_column_number = 6
row_offset = 1
stock_symbol_column_name = 'Stock'
current_price_column_name = 'Current Price'
purchase_date_column_name = 'Purchase Date'
purchase_price_column_name = 'Purchased Price'
purchase_units_column_name = 'Purchased Units'
today_date = date.today()

credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/delandre/Documents/MagicPortfolio/magicPortCreds.json', scope)
spread_sheet_client = gspread.authorize(credentials)

sheet = spread_sheet_client.open('Finance').worksheet('MagicPort')
# print(sheet.cell(2,6))
# print(sheet.update_cell(2,6, 10))
# print(sheet.cell(2,6))

def get_stock_latest_close_price(symbol):
	response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}'.format(symbol=symbol, key=price_api_key)).json()
	lastest_date = response['Meta Data']['3. Last Refreshed']
	latest_price_at_close = response['Time Series (Daily)'][lastest_date]['4. close']
	return float(latest_price_at_close)

stocks = sheet.get_all_records()
portfolio = []
row_num = 2
for stock in stocks:
	symbol = stock[stock_symbol_column_name]
	current_price = stock[current_price_column_name]
	purchase_date = stock[purchase_date_column_name]
	purchase_units = stock[purchase_units_column_name]
	purchase_price = stock[purchase_price_column_name][1:]
	
	if symbol and symbol not in ('cash', 'Totals'):
		new_price = get_stock_latest_close_price(symbol)
		sheet.update_cell(row_num, current_price_column_number, new_price)
		print(symbol + ': old price: ' + current_price + ', new  price: ' + str(new_price) + ', date: ' + str(today_date))
		row_num += 1
		portfolio.append(StockHolding(symbol, purchase_units, purchase_date, purchase_price, new_price))
		# pprint.pprint(stock)

Magic_portfolio = Portfolio(portfolio)
print(Magic_portfolio.get_portfolio_value())
print(Magic_portfolio.get_portfolio_initial_value())
print(Magic_portfolio.get_portfolio_profit())
# for s in portfolio:
# 	print(s.symbol + ' profit: ' + str(s.get_holding_profit()) + ' percent gain: ' + str(s.get_percent_growth()))

