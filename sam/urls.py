from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sam.views',
    url(r'^$', 'home.home'),
    url(r'^around_the_web$', 'around_the_web.around_the_web'),
    url(r'^about$', 'about.about'),
    url(r'^contact$', 'contact.contact'),
    url(r'^personal$', 'personal.personal'),
    url(r'^professional$', 'professional.professional'),
    url(r'^education$', 'education.education'),
    url(r'^blog$', 'blog.blog'),
    url(r'^blog/archive$', 'blog.post_archive'),
    url(r'^blog/post(?:/(?P<post_id>\d+))?$', 'blog.post'),
    url(r'^blog/filter(?:/(?P<kind>(\w+[+]*)*))?(?:/(?P<tag>(\w+[-*+]*)*))?$', 'blog.filter'),
    url(r'^front_page$', 'front_page.front_page'),
    url(r'^favorite_quotes$', 'quote.quote'),
    url(r'^art$', 'art.art'),
    url(r'^art/archive$', 'art.art_archive'),
    url(r'^art/work(?:/(?P<image_id>\d+))?$', 'art.art_work'),
    url(r'^art/filter(?:/(?P<kind>(\w+[+]*)*))?(?:/(?P<tag>(\w+[-*+]*)*))?$', 'art.filter'),
)

urlpatterns += patterns('',
    (r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
