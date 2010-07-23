# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import *
from word.models import Word
from django.template import RequestContext
from tagging.models import Tag
from tagging.views import tagged_object_list
from django.views.generic.create_update import create_object
from forms import WordForm
from django.contrib.auth.decorators import login_required


words = Word.objects.all()
qs = {
          'queryset': Word.objects.all(),
          'paginate_by': 15,
          'extra_context':{'title':'All Words'},
            }

tags = Tag.objects.all()
urlpatterns = patterns('word.views',
    (r'^$', object_list, qs),
     (r'^create/?$', login_required(create_object),
           dict(form_class=WordForm) ),
    (r'^search/$', 'search'),
    (r'^random/$', 'random_word'),
    (r'^all/$', object_list, { 'queryset': words, 'paginate_by':10, } ),
    (r'^browse/audio/$', 'audio'),
    (r'^browse/alphabet/(?P<letter>\w{0,1})$', 'alphabet'),
    (r'^browse/category/$', object_list, { 'queryset': tags,
        'extra_context':{'title':'Categories'} } ),
    (r'^browse/category/(?P<cat_id>\d+)/$', 'category_detail'),
    (r'^browse/category/(?P<cat_id>\d+)/excel$', 'show_excel'),
    (r'^browse/category/(?P<cat_id>\d+)/pdf$', 'show_pdf'),
    (r'^browse/dialect/(?P<dialect>\w*)/$', 'dialect'),
    (r'^(?P<word_id>\d+)/$', 'word_detail'),
    (r'^(?P<word_id>\d+)/(?P<xspf>\w+)/$', 'word_detail'),
)

