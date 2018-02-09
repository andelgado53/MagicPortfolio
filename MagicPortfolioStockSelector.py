import requests, lxml.html
from bs4 import BeautifulSoup
import pprint
from configuration import *
from Portfolio import Portfolio
from SheetsClient import SheetsClient
from StockHolding import StockHolding
from StockDataFetcher import StockDataFetcher


stocks_sheets_name = 'Finance'
stocks_worksheet_name = 'MagicPort'
magic_website_session = requests.session()

login = magic_website_session.get('https://www.magicformulainvesting.com/Account/LogOn')

login_html = lxml.html.fromstring(login.text)
loggin_hidden_inputs = login_html.xpath(r'//loggin_form//input[@type="hidden"]')
loggin_form = {x.attrib["name"]: x.attrib["value"] for x in loggin_hidden_inputs}
loggin_form['Email'] = magic_portfolio_site_log_email
loggin_form['Password'] = magic_portfolio_site_log_password
magic_website_session.post('https://www.magicformulainvesting.com/Account/LogOn', data=loggin_form)

get_stock_recommendation_form = {'MinimumMarketCap': 50, 'Select30': 'false'}
stock_selection_response = magic_website_session.post('https://www.magicformulainvesting.com/Screening/StockScreening', get_stock_recommendation_form)

soup = BeautifulSoup(stock_selection_response.text, 'html.parser')
tables = soup.findChildren('table')
stocks_selection_table = tables[-1]
rows = stocks_selection_table.findChildren(['th', 'tr'])
recommended_stocks = set()
for row in rows:
    cells = row.findChildren('td')
    if len(cells) > 0:
        recommended_stocks.add(cells[1].string)


sheets_client = SheetsClient(path_to_google_sheet_credentials, stocks_sheets_name)
sheet = sheets_client.get_worksheet(stocks_worksheet_name)

stocks_in_portfolio = sheet.get_all_records()
portfolio = []
row_num = 2
for stock in stocks_in_portfolio:
	symbol = stock[stock_symbol_column_name]
	current_price = stock[current_price_column_name][1:]
	purchase_date = stock[purchase_date_column_name]
	purchase_units = stock[purchase_units_column_name]
	purchase_price = stock[purchase_price_column_name][1:]
	status = stock[statu_column_name]
	new_price = current_price
	
	if symbol and symbol not in ('cash', 'Totals'):
		portfolio.append(StockHolding(symbol, purchase_units, purchase_date, purchase_price, new_price))
		row_num += 1
		
Magic_portfolio = Portfolio(portfolio)

for stock in recommended_stocks:
    if not Magic_portfolio.is_stock_in_portfolio(stock):
        print(str(stock) + ' most recent closing price: ' + str(StockDataFetcher(stock).get_stock_latest_close_price()))