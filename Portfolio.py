
class Portfolio:

	def __init__(self, holdings):
		self.holdings = holdings
		self.value = self._calculate_portfolio_value()
		self.initial_investment = self._calculate_portfolio_initial_value()

	def get_portfolio_value(self):
		return self.value

	def get_portfolio_initial_value(self):
		return self.initial_investment

	def _calculate_portfolio_value(self):
		value = 0 
		for holding in self.holdings:
			value += holding.get_current_value()
		return value

	def _calculate_portfolio_initial_value(self):
		value = 0 
		for holding in self.holdings:
			value += holding.get_initial_investment()
		return value

	def get_portfolio_profit(self):
		return self.value - self.initial_investment

