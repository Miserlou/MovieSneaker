import lxml.html as html
import datetime

class ShowtimeParser:
	pass

class FlixsterParser(ShowtimeParser):
	# The date is in the format: YYYYMMDD, zipcode is: NNNNN
	BASE_URL = "http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=%(date)s&postal=%(zipcode)s&submit=Go"

	def __init__(self,zipcode=None,date=None):
		"""
		:param date: Datetime object representing our target date
		:param zipcode: The zipcode as a string

		:return:
		"""
		if zipcode:
			if not date:
				date = datetime.datetime.today()
				self._get_base(date=date.strftime("%Y%m%d"),zipcode=zipcode)
	
	def _get_base(self,**kwargs):
		self.base = html.parse(BASE_URL%kwargs).getroot())
