import requests, lxml.html
from bs4 import BeautifulSoup
import pprint
from configuration import *
from Portfolio import Portfolio
from SheetsClient import SheetsClient
from StockHolding import StockHolding
from StockDataFetcher import StockDataFetcher
from PortfolioCreator import create_portfolio

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

Magic_portfolio = Portfolio(create_portfolio(sheet.get_all_records()))

for stock in recommended_stocks:
    if not Magic_portfolio.is_stock_in_portfolio(stock):
        print(str(stock) + ' most recent closing price: ' 
        + str(StockDataFetcher(stock).get_stock_latest_close_price()))
