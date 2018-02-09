import pprint
import requests
import json
import collections
from datetime import date
from StockHolding import StockHolding
from Portfolio import Portfolio
from configuration import *
from SheetsClient import SheetsClient
from StockDataFetcher import StockDataFetcher

today_date = date.today()

sheets_client = SheetsClient(path_to_google_sheet_credentials, stocks_sheets_name)
sheet = sheets_client.get_worksheet(stocks_worksheet_name)

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
			new_price = StockDataFetcher(symbol).get_stock_latest_close_price()
			sheet.update_cell(row_num, current_price_column_number, new_price)
			print(symbol + ': old price: ' + current_price + ', new  price: ' + str(new_price) + ', update: ' + str(today_date))

		portfolio.append(StockHolding(symbol, purchase_units, purchase_date, purchase_price, new_price))
		row_num += 1
		
Magic_portfolio = Portfolio(portfolio)
print('Current Portfolio value: ' + str(Magic_portfolio.get_portfolio_value()))
print('Initial Investment: ' + str(Magic_portfolio.get_portfolio_initial_value()))
print('Dollar Profit: ' + str(Magic_portfolio.get_portfolio_profit()))
print('Percent Growth: ' + str(Magic_portfolio.get_portfolio_percent_growth()))