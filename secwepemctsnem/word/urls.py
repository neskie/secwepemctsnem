# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import *
from models import Word
from django.template import RequestContext
from tagging.models import Tag

words = Word.objects.all()
alphabet = ['a','á','c','e',u'é','g','h','i','k','l','m','n','q', 'r', 's', 't', 'u', 'w', 'x', 'y']
total = Word.objects.all().count()

tags = Tag.objects.all()
urlpatterns = patterns('word.views',
    (r'^$', 'index'),
    (r'^all$', object_list, { 'queryset': words, 'paginate_by':10, } ),
    (r'^browse/audio$', 'audio'),
    (r'^browse/alphabet$', direct_to_template,
            {'template': 'word/alphabet.html',
             'extra_context':{'alphabet':alphabet, 'title':'Words Starting With'}
            }),
    (r'^browse/alphabet/$', direct_to_template,
            {'template': 'word/alphabet.html',
             'extra_context':{'alphabet':alphabet}
            }),
    (r'^browse/alphabet/(?P<letter>\w+)$', 'alphabet'),
    (r'^browse/category$', object_list, { 'queryset': tags,
        'extra_context':{'total':total, 'title':'Categories'} } ),
    (r'^browse/category/(?P<cat_id>\d+)/$', 'category_detail'),
    (r'^browse/category/(?P<cat_id>\d+)/excel$', 'show_excel'),
    (r'^browse/category/(?P<cat_id>\d+)/pdf$', 'show_pdf'),
    (r'^audio/(?P<word_id>\d+)/$', 'jsonaudiofile'),
    (r'^audioplayer$', direct_to_template, {'template': 'word/audioplayer.html'}),
    (r'^audioplayer/(?P<audio_id>\d+)/$', 'audioplayer'),
    (r'^audioplayer/(?P<audio_id>\d+)/download$', 'download_view'),
    (r'^(?P<word_id>\d+)/$', 'detail'),
)

