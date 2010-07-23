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
#CREATE VIRTUAL TABLE word_search USING FTS3(word, body);
words = Word.objects.all()
for word in words:
    txt = " ".join([ word.strip_accents() ] + list(
        word.englishword_set.all().values_list('english',flat=True)))
    cursor.execute("INSERT INTO word_search (word_id, body) VALUES (%s, %s)", (word.id, txt))

transaction.commit_unless_managed()
