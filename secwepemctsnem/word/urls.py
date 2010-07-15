# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import *
from models import Word
from django.template import RequestContext
from tagging.models import Tag
from django.views.generic.create_update import create_object
from forms import WordForm

words = Word.objects.all()
alphabet = ['a','á','c','e',u'é','g','h','i','k','l','m','n','q', 'r', 's', 't', 'u', 'w', 'x', 'y']
total = Word.objects.all().count()
info_dict = {
          'model': Word,
          'queryset': Word.objects.all(),
            }
qs = {
          'queryset': Word.objects.all(),
          'paginate_by': 15,
          'extra_context':{'title':'All Words'},
            }


tags = Tag.objects.all()
urlpatterns = patterns('word.views',
    (r'^$', object_list, qs),
    (r'^recorder/$', 'recorder'),
    (r'^search/$', 'search'),
    (r'^random/$', 'random_word'),
    (r'^all/$', object_list, { 'queryset': words, 'paginate_by':10, } ),
    (r'^browse/audio/$', 'audio'),
    (r'^browse/alphabet/$', direct_to_template,
            {'template': 'word/alphabet.html',
             'extra_context':{'alphabet':alphabet, 'title':'Words Starting With'}
            }),
    (r'^browse/alphabet/$', direct_to_template,
            {'template': 'word/alphabet.html',
             'extra_context':{'alphabet':alphabet}
            }),
    (r'^browse/alphabet/(?P<letter>\w+)$', 'alphabet'),
    (r'^browse/category/$', object_list, { 'queryset': tags,
        'extra_context':{'total':total, 'title':'Categories'} } ),
    (r'^browse/category/(?P<cat_id>\d+)/$', 'category_detail'),
    (r'^browse/category/(?P<cat_id>\d+)/excel$', 'show_excel'),
    (r'^browse/category/(?P<cat_id>\d+)/pdf$', 'show_pdf'),
     (r'^create/?$', create_object,
           dict(form_class=WordForm, post_save_redirect="/words/") ),
    (r'^audio/(?P<word_id>\d+)/$', 'jsonaudiofile'),
    (r'^audioplayer/(?P<audio_id>\d+)/$', 'audioplayer'),
    (r'^audioplayer/(?P<audio_id>\d+)/download$', 'download_view'),
    (r'^(?P<word_id>\d+)/$', 'detail'),
)

