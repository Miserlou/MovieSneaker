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
import sneakercore

from models import ZipCodeForm, ZipCode, Movie, Venue, Showing


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
    return render_to_response('sneak.html', context_instance=RequestContext(request))

def _slurp_theatres(zipcode,date):
    theatres = showtimesparsing.FlixsterParser(zipcode=zipcode,date=date)
    for theatre in theatres["theatres"]:
        z, created = ZipCode.objects.get_or_create(zipcode=zipcode)
        if created:
            z.save()
        v, created = Venue.objects.get_or_create(name=theatre["name"],address=theatre["address"])
        if created:
            v.zipcode.add(z)
            v.save()
        theatre["id"] = v.id
        for movie in theatre['movies']:
            showtimes = movie['showtimes']
            if not showtimes:
                continue
            runtime = (showtimes[0]['end']-showtimes[0]['start']).seconds/60.0
            m, created = Movie.objects.get_or_create(name=movie["name"],runtime=runtime)
            if created:
                m.save()
            movie["id"] = m.id
            for showtime in showtimes:
                s,created = Showing.objects.get_or_create(movie=m,venue=v,start=showtime['start'],end=showtime['end'])
                if created:
                    s.save()
                showtime["id"] = s.id
    return theatres

def _parse_date(date):
    return datetime.datetime.strptime(date,"%Y%m%d") if date else datetime.datetime.today()

def venues(request, zipcode, date=None):
    """
    Returns JSON of theatres
    """
    date = _parse_date(date)

    cache_key = "%s_%s"%(zipcode,date.strftime("%Y-%m-%d"))
    theatres_json = cache.get(cache_key)
    if not theatres_json:
        theatres = _slurp_theatres(zipcode,date)
        theatres_json = json.dumps(theatres, cls=DjangoJSONEncoder, indent=1)
        cache.set(cache_key,theatres_json)

    return HttpResponse(theatres_json)
    #if not date
    #venues =

def get_chains(request,theatre, date=None):
    date = _parse_date(date)

    chain_length = int(request.GET.get('length',3))
    if chain_length > 4:
        return HttpResponse(json.dumps({"error":"No chains longer than 4 items supported"}))

    cache_key = "t%s_%s_%d"%(theatre,date.strftime("%Y-%m-%d"),chain_length)
    chains_json = cache.get(cache_key)
    if not chains_json:
        showings = Showing.objects.filter(venue__id=theatre,start__range=(date.replace(hour=0,minute=0,second=0,microsecond=0),date.replace(hour=23,minute=59,second=59,microsecond=0)))
        showtimes = []
        for showing in showings:
            showtimes.append((showing.movie.id,showing.start,showing.end))
        chains_raw = sneakercore.find_chains(showtimes,chain_length=chain_length)
        chains = {"chains":[]}
        for raw_chain in chains_raw:
            chain = []
            for movie_id,start,end in raw_chain:
                chain.append({"name":Movie.objects.get(id=movie_id).name,"id":movie_id,"start":start,"end":end})
            chains["chains"].append(chain)
        chains_json = json.dumps(chains, cls=DjangoJSONEncoder, indent=1)
        cache.set(cache_key,chains_json)
    return HttpResponse(chains_json)



