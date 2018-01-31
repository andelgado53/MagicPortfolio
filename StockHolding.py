from datetime import datetime

class StockHolding:

	def __init__(self, symbol, units, purchase_date, purchase_price, current_price):
		self.symbol = symbol
		self.units = units
		self.purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
		self.purchase_price = float(purchase_price)
		self.sale_date = None
		self.current_price = float(current_price)
	
	def set_current_price(self, price):
		self.current_price = float(price)

	def get_current_price(self):
		return self.current_price

	def get_holding_profit(self):
		return (self.units * self.current_price) - (self.units * self.purchase_price)

	def get_holding_days(self):
		time_difference = datetime.today() - self.purchase_date
		return time_difference.days

	def get_initial_investment(self):
		return self.units * self.purchase_price

	def get_current_value(self):
		return self.units * self.get_current_price()

	def get_percent_growth(self):
		return (self.get_current_value() - self.get_initial_investment()) / self.get_initial_investment()


# ntp = StockHolding('NTP', 100, '2017-12-01', 5.0, 2.5)

# print(ntp.get_current_price())
# print(ntp.get_holding_profit())
# print(ntp.get_holding_days())
# print(ntp.get_percent_growth())