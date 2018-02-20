from datetime import datetime

class StockHolding:

	def __init__(self, symbol, units, purchase_date, purchase_price, current_price):
		self.symbol = symbol
		try:
			self.units = int(units)
		except ValueError:
			raise ValueError('Units must be an integer or a string that can be converted to one.')
		try:
			self.purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
		except ValueError:
			raise ValueError('Wrong date format. Please use date format YYYY-MM-DD')
		try:
			self.purchase_price = float(purchase_price)
			self.current_price = float(current_price)
		except ValueError:
			raise(ValueError('purchase_price and current_price must be numbers or string that can be turned into a float'))
	
	def set_current_price(self, price):
		try:
			self.current_price = float(price)
		except ValueError:
			raise ValueError('Can not convert {input} into a float type'.format(input=price))

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
