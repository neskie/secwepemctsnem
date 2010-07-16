from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout, password_change
from django.contrib import databrowse
from word.models import Word, AudioFile
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page':'/'}),
    (r'^accounts/profile/$', direct_to_template, {"template" : "accounts/profile.html"}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^search/', include('haystack.urls')),
    (r'^words/', include('word.urls')),
)

#if settings.DEBUG:
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )
