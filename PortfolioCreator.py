from configuration import *
from SheetsClient import SheetsClient
from StockHolding import StockHolding

def create_portfolio(records):
    portfolio = []
    row_num = 2
    for stock in records:
        symbol = stock[stock_symbol_column_name]
        current_price = stock[current_price_column_name][1:]
        purchase_date = stock[purchase_date_column_name]
        purchase_units = stock[purchase_units_column_name]
        purchase_price = stock[purchase_price_column_name][1:]
        new_price = current_price      
        if symbol and symbol not in ('cash', 'Totals'):
            portfolio.append(StockHolding(symbol, purchase_units, purchase_date, purchase_price, new_price))
            row_num += 1
    return portfolio