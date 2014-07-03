from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sam.views',
    url(r'^$', 'home.home'),
    url(r'^hub$', 'around_the_web.around_the_web'),
    url(r'^about$', 'about.about'),
    url(r'^contact$', 'contact.contact'),
    url(r'^me$', 'personal.personal'),
    url(r'^work$', 'professional.professional'),
    url(r'^school$', 'education.education'),
    url(r'^blog$', 'blog.blog'),
    url(r'^blog/archive$', 'blog.post_archive'),
    url(r'^blog/post(?:/(?P<post_id>\d+))?$', 'blog.post'),
    url(r'^blog/filter(?:/(?P<kind>(\w+[+]*)*))?(?:/(?P<tag>(\w+[-*+]*)*))?$', 'blog.filter'),
    url(r'^center$', 'front_page.front_page'),
    url(r'^quotes$', 'quote.quote'),
    url(r'^art$', 'art.art'),
    url(r'^art/archive$', 'art.art_archive'),
    url(r'^art/work(?:/(?P<image_id>\d+))?$', 'art.art_work'),
    url(r'^art/filter(?:/(?P<kind>(\w+[+]*)*))?(?:/(?P<tag>(\w+[-*+]*)*))?$', 'art.filter'),
    url(r'^sha1$', 'sha1.sha1'),
)

urlpatterns += patterns('',
    (r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
