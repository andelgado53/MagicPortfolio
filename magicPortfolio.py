import requests
import json
import collections
import time
from datetime import date
from StockHolding import StockHolding
from Portfolio import Portfolio
from configuration import *
from SheetsClient import SheetsClient
from StockDataFetcher import StockDataFetcher
from PortfolioCreator import create_portfolio

today_date = date.today()

sheets_client = SheetsClient(path_to_google_sheet_credentials, stocks_sheets_name)
sheet = sheets_client.get_worksheet(stocks_worksheet_name)
stocks = sheet.get_all_records()

def update_portfolio_prices(records):
	row_num = 2
	for stock in records:
		symbol = stock[stock_symbol_column_name]
		current_price = stock[current_price_column_name]
		status = stock[statu_column_name]
		new_price = current_price

		if symbol and symbol not in ('cash', 'Totals'):
			if status != 'Sold':
				print('getting price for: ' + symbol)
				new_price = StockDataFetcher(symbol).get_price()
				sheet.update_cell(row_num, current_price_column_number, new_price)
			row_num += 1
update_portfolio_prices(stocks)

portfolio = create_portfolio(sheet.get_all_records())
		
Magic_portfolio = Portfolio(portfolio)
print('Current Portfolio value: ${value:,.2f}'.format(value=Magic_portfolio.get_portfolio_value()))
print('Initial Investment: ${value:,.2f}'.format(value=Magic_portfolio.get_portfolio_initial_value()))
print('Dollar Profit: ${value:,.2f}'.format(value=Magic_portfolio.get_portfolio_profit()))
print('Percent Growth: {growth:.2f}%'.format(growth=Magic_portfolio.get_portfolio_percent_growth() * 100))
