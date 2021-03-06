from django.conf.urls import patterns, include, url

urlpatterns = patterns('sam.views',
    url(r'^$', 'home.home'),
    url(r'^hub$', 'hub.hub'),
    url(r'^about$', 'about.about'),
    url(r'^contact$', 'contact.contact'),
    url(r'^me$', 'personal.personal'),
    url(r'^work$', 'professional.professional'),
    url(r'^school$', 'education.education'),
    url(r'^blog$', 'blog.blog'),
    url(r'^blog/archive$', 'blog.post_archive'),
    url(r'^blog/post(?:/(?P<post_id>\d+))?$', 'blog.post'),
    url(r'^blog/filter(?:/(?P<kind>(\w+[+]*)*))?(?:/(?P<tag>(\w+[-*+]*)*))?$', 'blog.filter'),
    url(r'^river$', 'river.river'),
    url(r'^quotes$', 'quote.quote'),
    url(r'^art$', 'art.art'),
    url(r'^art/archive$', 'art.art_archive'),
    url(r'^art/work(?:/(?P<image_id>\d+))?$', 'art.art_work'),
    url(r'^art/filter(?:/(?P<kind>(\w+[+]*)*))?(?:/(?P<tag>(\w+[-*+]*)*))?$', 'art.filter'),
    url(r'^sha1$', 'sha1.sha1'),

    url(r'^river/async/blogs$', 'river.blogs'),
    url(r'^river/async/flickrs$', 'river.flickrs'),
    url(r'^river/async/githubs$', 'river.githubs'),
    url(r'^river/async/lastfms$', 'river.lastfms'),
    url(r'^river/async/soundclouds$', 'river.soundclouds'),
    url(r'^river/async/twitters$', 'river.twitters'),
    #url(r'^river/async/$', 'river.imgurs'),
    #url(r'^river/async/$', 'river.facebooks'),
)
