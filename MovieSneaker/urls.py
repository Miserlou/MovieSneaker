from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'MovieSneaker.sneaker.views.root'),
     url(r'^sneaking/(?P<hash>[^/]+)$', 'MovieSneaker.sneaker.views.sneaking'),
     url(r'^venues/(?P<zipcode>[^/]+)/(?P<date>[0-9]+)', 'MovieSneaker.sneaker.views.venues'),
     url(r'^chains/(?P<theatre>[0-9]+)', 'MovieSneaker.sneaker.views.get_chains'),
     url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'../static'}),
     #     url(r'^admin/', include(admin.site.urls)),
)
