# -*- coding: utf-8 -*-
import sys
import urllib2
from os import environ

environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from django.contrib.sessions.models import *
from django.db import connection, transaction

from word.models import *


cursor = connection.cursor()

words = Word.objects.all()
for word in words:
    hasaudio = 'has:noaudio'
    if word.audiofile.all():
        hasaudio = "has:audio"
    txt = '%s %s %s' % (word.strip_accents(), word.english, hasaudio )
    # txt should be stripped from HTML, stop words etc. to get smaller size of the database
    cursor.execute("INSERT INTO word_search (word_id, body) VALUES (%s, %s)", (word.id, txt))

transaction.commit_unless_managed()
