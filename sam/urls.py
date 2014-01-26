from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sam.views',
    url(r'^$', 'home.home'),
    url(r'^around_the_web$', 'around_the_web.around_the_web'), # rename 'hub' "The Hub"
    url(r'^about$', 'about.about'),
    url(r'^contact$', 'contact.contact'),
    url(r'^personal$', 'personal.personal'), # rename 'me'
    url(r'^professional$', 'professional.professional'), # rename 'work'
    url(r'^education$', 'education.education'), # rename 'school'
    url(r'^blog$', 'blog.blog'),
    url(r'^blog/archive$', 'blog.post_archive'),
    url(r'^blog/post(?:/(?P<post_id>\d+))?$', 'blog.post'),
    url(r'^blog/filter(?:/(?P<kind>(\w+[+]*)*))?(?:/(?P<tag>(\w+[-*+]*)*))?$', 'blog.filter'),
    url(r'^front_page$', 'front_page.front_page'), # rename 'center' "The Center"
    url(r'^favorite_quotes$', 'quote.quote'), # rename 'quotes'
    url(r'^art$', 'art.art'),
    url(r'^art/archive$', 'art.art_archive'),
    url(r'^art/work(?:/(?P<image_id>\d+))?$', 'art.art_work'),
    url(r'^art/filter(?:/(?P<kind>(\w+[+]*)*))?(?:/(?P<tag>(\w+[-*+]*)*))?$', 'art.filter'),
    url(r'^password$', 'password.password'),
)

urlpatterns += patterns('',
    (r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
