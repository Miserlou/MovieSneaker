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
		
# TODO: fake the useragent


class FlixsterParser(ShowtimeParser):
	# The date is in the format: YYYYMMDD, zipcode is: NNNNN
	BASE_URL = "http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=%(date)s&postal=%(zipcode)s&submit=Go"
	#USERAGENT = "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"
	
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

	def _parse(self):
		theatres = []
		for theater in self.base.find_class('theater'):
			name = theater.cssselect('h2 a')[0].attrib['title']
			address = theater.cssselect('h2 span')[0].text.strip("\n\t -")
			movies = []
			for movie in theater.cssselect('.showtime'):
				title = movie.cssselect('h3 a').attrib['title']
				raw_rating,raw_duration = movie.cssselect('h3 span').text.strip("\n\t -").split('-')
				showings = []
				for raw_time in movie.cssselect('h3').tail.split()
					if raw_time.endswith(am):
						raw_time += "pm"
					# combine the hour with the date of this parse
					start = datetime.datetime.combine(self.date,datetime.datetime.strptime(raw_time,"%I:%M%p")
					end = start + duration
				movies.append({'name':title,'showtimes':showings})
			theatres.append({'name':name,'address':address,'movies':movies})
		return theatres