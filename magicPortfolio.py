import pprint
import requests
import json
import collections
from datetime import date
from StockHolding import StockHolding
from Portfolio import Portfolio
from configuration import price_api_key, path_to_google_sheet_credentials
from SheetsClient import SheetsClient

current_price_column_number = 6
stock_symbol_column_name = 'Stock'
current_price_column_name = 'Current Price'
purchase_date_column_name = 'Purchase Date'
purchase_price_column_name = 'Purchased Price'
purchase_units_column_name = 'Purchased Units'
statu_column_name = 'Status'
stocks_sheets_name = 'Finance'
stocks_worksheet_name = 'MagicPort'
today_date = date.today()

sheets_client = SheetsClient(path_to_google_sheet_credentials, stocks_sheets_name)
sheet = sheets_client.get_worksheet(stocks_worksheet_name)

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
	status = stock[statu_column_name]
	new_price = current_price
	
	if symbol and symbol not in ('cash', 'Totals'):
		if status != 'Sold':
			new_price = get_stock_latest_close_price(symbol)
			sheet.update_cell(row_num, current_price_column_number, new_price)
			print(symbol + ': old price: ' + current_price + ', new  price: ' + str(new_price) + ', update: ' + str(today_date))

		portfolio.append(StockHolding(symbol, purchase_units, purchase_date, purchase_price, new_price))
		row_num += 1
		
Magic_portfolio = Portfolio(portfolio)
print('Current Portfolio value: ' + str(Magic_portfolio.get_portfolio_value()))
print('Initial Investment: ' + str(Magic_portfolio.get_portfolio_initial_value()))
print('Dollar Profit: ' + str(Magic_portfolio.get_portfolio_profit()))
print('Percent Growth: ' + str(Magic_portfolio.get_portfolio_percent_growth()))
