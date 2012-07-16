import lxml.html as html
import datetime
import re

# TODO: Refactor this shitshow. Just use functions

#Here's the format we expect this to return:
#	{ 'theatres': [
#			{'name':<theater name str>, 'address':<address str>, 'movies': [
#					{'name':<movie title str>, 'showtimes': [
#							{'start':<start datetime>,'end':<end datetime>}, ...
#						]
#					}, ...
#				]
#			}, ...
#		],
#      'date' : <datetime for which these listings are>
#	}



def FlixsterParser(zipcode, date=None, BASE_URL="http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=%(date)s&postal=%(zipcode)s&submit=Go"):
    # The date is in the format: YYYYMMDD, zipcode is: NNNNN
        """
        :param zipcode: The zipcode as a string
        :param date: Datetime object representing our target date

        :return: The theatres and showtimes for a zipcode on a particular date
        """
        if zipcode:
            if not date:
                date = datetime.datetime.today()
            base = html.parse(BASE_URL%dict(date=date.strftime("%Y%m%d"),zipcode=zipcode)).getroot()

            theatres = []
            for theater in base.find_class('theater'):
                name = theater.cssselect('h2 a')[0].attrib['title']
                address = theater.cssselect('h2 span')[0].text.strip("\n\t -")
                movies = []
                for movie in theater.cssselect('.showtime'):
                    title_line = movie.cssselect('h3')[0]
                    if len(title_line.getchildren())>1:
                        title = title_line.cssselect('a')[0].attrib['title']
                        sp = title_line.cssselect('span')[0].text.strip("\n\t -").rsplit('-',1)
#                        raw_rating = sp[0]
                        if len(sp)>1:
                            raw_duration = sp[1]
                            split_duration = raw_duration.strip().split()
                            parsed_duration = 0
                            while split_duration:
                                num = split_duration.pop(0)
                                kind = split_duration.pop(0)
                                parsed_duration += 60*int(num)if 'hr' in kind.lower() else int(num)
                            duration = datetime.timedelta(minutes=parsed_duration)
                        else:
                            # if no duration specified we'll assume 3 hours
                            # probably double feature
                            duration = datetime.timedelta(minutes=180)
                    else: # we have nothing but a non-linked title
                        title = title_line.text.strip()
                        duration = datetime.timedelta(minutes=90)
                    showtimes = []
                    for raw_time in movie.cssselect('h3')[0].tail.split():
                        if not raw_time.endswith("am"):
                            raw_time += "pm"
                        # combine the hour with the date of this parse
                        start = datetime.datetime.combine(date,datetime.datetime.strptime(raw_time,"%I:%M%p").time())
                        end = start + duration
                        showtimes.append({"start":start,"end":end})
                    movies.append({'name':title,'showtimes':showtimes})
                theatres.append({'name':name,'address':address,'movies':movies})
            return { 'theatres': theatres, 'date': date }