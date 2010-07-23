from django.conf.urls.defaults import *

urlpatterns = patterns('audio.views',
    (r'^recorder/(?P<word_id>\d+)/$', 'recorder'),
    (r'^detail/(?P<audio_id>\d+)/$', 'audiofile_detail'),
    (r'^detail/(?P<audio_id>\d+)/(?P<xspf>\w+)/$', 'audiofile_detail'),
    (r'^player/(?P<audio_id>\d+)/$', 'audioplayer'),
    (r'^player/(?P<audio_id>\d+)/download$', 'download_view'),
)
