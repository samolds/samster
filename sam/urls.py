from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sam.views',
    url(r'^$', 'home.home'),
    url(r'^around_the_web$', 'around_the_web.around_the_web'),
    #url(r'buildings?$', 'buildings.buildings'),
    #url(r'search/$', 'search.SearchView'),
    #url(r'contact(?:/(?P<spot_id>\d+))?/$', 'contact.contact'),
    #url(r'sorry(?:/(?P<spot_id>\d+))?/$', 'contact.sorry'),
    #url(r'thankyou(?:/(?P<spot_id>\d+))?/$', 'contact.thank_you'),
    #url(r'space/(?P<spot_id>\d+)$', 'spot.SpotView'),
    #url(r'space/(?P<spot_id>\d+)/json/$', 'spot.SpotView', {'return_json': True}),
)
