from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('sam.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    (r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)

handler403 = 'sam.views.error.err_403'
handler404 = 'sam.views.error.err_404'
handler500 = 'sam.views.error.err_500'

if settings.DEBUG:
    urlpatterns += patterns('',
      url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
      }),
    )

urlpatterns += staticfiles_urlpatterns()
