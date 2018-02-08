import requests, lxml.html
from bs4 import BeautifulSoup
import pprint
from configuration import magic_portfolio_site_log_email, magic_portfolio_site_log_password

magic_site_session = requests.session()

login = magic_site_session.get('https://www.magicformulainvesting.com/Account/LogOn')

login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
form['Email'] = magic_portfolio_site_log_email
form['Password'] = magic_portfolio_site_log_password
response = magic_site_session.post('https://www.magicformulainvesting.com/Account/LogOn', data=form)

form1 = {'MinimumMarketCap': 50, 'Select30': 'false'}
res = magic_site_session.post('https://www.magicformulainvesting.com/Screening/StockScreening', form1)

soup = BeautifulSoup(res.text, 'html.parser')
tables = soup.findChildren('table')
stocks_selection_table = tables[-1]
rows = stocks_selection_table.findChildren(['th', 'tr'])
stocks = set()
for row in rows:
    cells = row.findChildren('td')
    # print(cells)
    if len(cells) > 0:
        # print(cells[0].string + ' ' +  cells[1].string)
        stocks.add(cells[1].string)
    # for cell in cells:
    #     print(cell.string)

# pprint.pprint(rows[0])
print(stocks)