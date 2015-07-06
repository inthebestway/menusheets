import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import os 

class GsDownloader(object):

	def __init__(self,sheetfilename,worksheetlist=None,credentials="sheetscred.json",data_file_path=''):
		self._credentials=credentials
		self.sheetfilename=sheetfilename
		self.worksheetlist=worksheetlist
		self.gc=self.gspread_setup()
		self.data_file_path = data_file_path

		self.filename=os.path.join(self.data_file_path, self.sheetfilename + '.json') 


	def sheetdata(self, reload_data=False):
		""" 
		get data from the specified sheet. reload_data = True to reload from google spreadsheets.
		Otherwise automatically dumps to a file.. the location of the file is specified by the input: 
		data_file_path parameter
		"""
		if os.path.isfile(self.filename) is True and reload_data is False :
			outdata = json.load(open(self.filename,'r'))
		else : 
			outdata = self.download_objects()

		return outdata

	def gspread_setup(self):
		""" 
		Load gspread credentials from a file and return the object
		"""
		credentials=self._credentials
		auth=json.load(open(credentials))
		scope = ['https://spreadsheets.google.com/feeds']

		credentials = SignedJwtAssertionCredentials(auth['client_email'], auth['private_key'], scope)

		gc = gspread.Client(auth=credentials)
		gc.login()
		return gc


	def download_objects(self): #,worksheets=None):
		""" 
		gc = authenticated gspread object
		download the google spreadsheet as python dictionary 
		you can input a list of spreadsheet names if you want
		otherwise download all
		"""
		gc=self.gc
		sheetfilename=self.sheetfilename
		worksheets=self.worksheetlist

		try:
			sh = gc.open(sheetfilename)
		except gspread.SpreadsheetNotFound:
			raise Exception("Can't fine the google spreadsheet with that name")

		if worksheets is None: 	
			worksheet_list=sh.worksheets()
		else:
			worksheet_list=list()
			for k in worksheets:
				try: 
					worksheet_list.append(sh.worksheet(k))
				except gspread.exceptions.WorksheetNotFound:
					print " can't find a sheet by that name "
			if worksheet_list == list():
				raise Exception("couldn't find any of the worksheets specified: %s").format(", ".join(worksheets))
		
		dat={k.title:k.get_all_values() for k in sh.worksheets()}

		dataobj=dict()
		for key,value in dat.iteritems():
			myl=[dict(zip(value[0],l)) for l in value[1:]] 
			dataobj[key]=myl

		self.dump(dataobj)
		return dataobj

	def dump(self, data):
		json.dump(data,open(self.filename,'w'))



#sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1vr8ymnpDdcqNJkPs0EU-1rrfz7vGszPFIwXwjvvvkjE/edit?usp=sharing')


## search for all cells containing fish 
#criteria_re = re.compile(r'fish')
#cell_list = sh.sheet1.findall(criteria_re)
#cell_list

# dump of data from all worksheets