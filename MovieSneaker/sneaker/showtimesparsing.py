class ShowtimeParser:
	pass

class FlixsterParser(ShowtimeParser):
	# The date is in the format: YYYYMMDD, zipcode is: NNNNN
	BASE_URL = "http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=%(date)s&postal=%(zipcode)s&submit=Go"

	def __init__(self,date,zipcode):
		"""
		:param date: Datetime object representing our target date
		:param zipcode: The zipcode as a string

		:return:
		"""
		self._get_base(self,date=date.strftime("%Y%m%d"),zipcode=zipcode)

	def _get_base(self,**kwargs):
		urllib2.urlopen(BASE_URL%kwargs)