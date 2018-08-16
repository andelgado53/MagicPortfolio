import requests
import json
import collections
from datetime import date
from StockHolding import StockHolding
from Portfolio import Portfolio
from configuration import *
from SheetsClient import SheetsClient
from StockDataFetcher import StockDataFetcher
from PortfolioCreator import create_portfolio
import pprint
import time

today_date = date.today()

sheets_client = SheetsClient(path_to_google_sheet_credentials, stocks_sheets_name)
sheet = sheets_client.get_worksheet('Portfolio-2018')
stocks = sheet.get_all_records()

row_num = 2
for stock in stocks:
    symbol = stock['Stock']
    if symbol and symbol != 'Total':
        new_price = StockDataFetcher(symbol).get_price()
        print('Updating {symbol} to new price ${price:,.2f}'.format(symbol=symbol, price=new_price))
        sheet.update_cell(row_num, 3, new_price)   
    row_num += 1
