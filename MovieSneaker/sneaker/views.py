from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from datetime import datetime
import hashlib

from sneaker.models import ZipCodeForm

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
