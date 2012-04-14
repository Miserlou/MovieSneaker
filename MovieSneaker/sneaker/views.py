from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.serializers.json import DjangoJSONEncoder
import datetime
#import hashlib
import json
import showtimesparsing

from sneaker.models import ZipCodeForm, ZipCode, Movie, Venue, Showing



def root(request):

    if request.method == 'POST': # If the form has been submitted...

        zipcode= request.POST['zipcode']

        form = ZipCodeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/sneaking/' + zipcode) # Redirect after POST

    else:
        form = ZipCodeForm() # An unbound form

    return render_to_response('root.html', {'form': form}, context_instance=RequestContext(request))

def sneaking(request, hash):
    return render_to_response('processing.html', context_instance=RequestContext(request))

def _slurp_theatres(zipcode,date):
    theatres = showtimesparsing.FlixsterParser(zipcode=zipcode,date=date)
    for theatre in theatres:
        z = ZipCode.objects.get_or_create(zipcode=zipcode)
        z.save()
        v = Venue.objects.get_or_create(name=theatre["name"],address=theatre["address"],zipcode=z)
        v.save()
        for movie in theatre['movies']:
            showtimes = movie['showtimes']
            runtime = (showtimes[0]['end']-showtimes[0]['start']).seconds/60.0
            m = Movie.objects.get_or_create(name=movie["name"],runtime=runtime)
            m.save()
            for showtime in showtimes:
                s = Showing.objects.get_or_create(movie=m,venue=v,start=showtime['start'],end=showtime['end'])
                s.save()
    return theatres



def venues(request, zipcode, date=None):
    if not date:
        date = datetime.datetime.today()
    cache_key = "%s_%s"%(zipcode,date.strftime("%Y-%m-%d"))
    theatres = cache.get(cache_key)
    if not theatres:
        theatres = _slurp_theatres(zipcode,date)
        theatres_json = json.dumps(theatres, cls=DjangoJSONEncoder, indent=1)
        cache.set(cache_key,theatres_json)

    return HttpResponse(theatres)
    #if not date
    #venues =

