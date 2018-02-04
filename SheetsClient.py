import gspread 
from oauth2client.service_account import ServiceAccountCredentials

class SheetsClient:

	def __init__(self, path_to_credentials, sheet_name):
		self.scope = ['http://spreadsheets.google.com/feeds']
		self.credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_credentials, self.scope)
		self.spread_sheet_client = gspread.authorize(self.credentials)
		self.sheet = self.spread_sheet_client.open(sheet_name)

	def get_worksheet(self, worksheet_name):
		return self.sheet.worksheet(worksheet_name)
