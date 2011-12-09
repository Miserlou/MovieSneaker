import lxml.html as html
import datetime

# TODO: Refactor this shitshow. Just use a much more straightforward interface:
# Basically, I need to define an intermediate data model, perhaps json
# and the ShowtimeParser abstract class will do validation, otherwise
# each class can just do its own custom shit

class ShowtimeParser:
	base = None
	venues = None
	movies = None
	showtimes = None
	zipcode = None
	date = None

	def get_venues(self,**kwargs):
		# if any parameters are different from the class variables, reinitialize
		if [True for k,v in [(k,self.__dict__[k]) for k in kwargs.keys() if self.__dict__.has_key(k)] if v!=d1[k]]
			self.__init__(**kwargs)
		if not self.venues:
			# extract venues
			self._extract_venues()
		return self.venues
		


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
			self.zipcode = zipcode
			self.date = date
			self._get_base(date=date.strftime("%Y%m%d"),zipcode=zipcode)
	
	def _get_base(self,**kwargs):
		self.base = html.parse(BASE_URL%kwargs).getroot())
