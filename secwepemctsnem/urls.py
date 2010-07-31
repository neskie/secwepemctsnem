from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout, password_change
from django.contrib import databrowse
from word.models import Word
from audio.models import AudioFile
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page':'/'}),
#    (r'^accounts/register/$', 'django.views.generic.simple.redirect_to',{'url':'/accounts/register/closed/'}),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/profile/', include('profiles.urls')),
    (r'^accounts/', include('invitation.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^search/', 'word.views.search'),
    (r'^words/', include('word.urls')),
    (r'^audiofile/', include('audio.urls')),
)

#if settings.DEBUG:
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )
