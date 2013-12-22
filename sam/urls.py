from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sam.views',
    url(r'^$', 'home.home'),
    url(r'^around_the_web$', 'around_the_web.around_the_web'),
    url(r'^about$', 'about.about'),
    url(r'^contact$', 'contact.contact'),
    url(r'^personal$', 'personal.personal'),
    url(r'^profesional$', 'professional.professional'),
    url(r'^education$', 'education.education'),
    url(r'^blog$', 'blog.blog'),
    url(r'^blog/all$', 'blog.all_posts'),
    url(r'^blog/post(?:/(?P<post_id>\d+))?$', 'blog.post'),
    url(r'^blog/filter(?:/(?P<tag>\w+))?$', 'blog.filter'),
    url(r'^front_page$', 'front_page.front_page'),
    url(r'^favorite_quotes$', 'quote.quote'),
    #url(r'^art$', 'art.art'),

    #url(r'buildings?$', 'buildings.buildings'),
    #url(r'search/$', 'search.SearchView'),
    #url(r'contact(?:/(?P<spot_id>\d+))?/$', 'contact.contact'),
    #url(r'sorry(?:/(?P<spot_id>\d+))?/$', 'contact.sorry'),
    #url(r'thankyou(?:/(?P<spot_id>\d+))?/$', 'contact.thank_you'),
    #url(r'space/(?P<spot_id>\d+)$', 'spot.SpotView'),
    #url(r'space/(?P<spot_id>\d+)/json/$', 'spot.SpotView', {'return_json': True}),
)

urlpatterns += patterns('',
    (r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
