from django.db import models
from django.contrib.auth.models import User,Group
from django.core.cache import cache
from django.utils import encoding
from django.template.defaultfilters import date as datefilter
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from datetime import datetime
import tagging
import unicodedata

class AudioFile(models.Model):
    audiofile = models.FileField(upload_to="files")
    description = models.CharField(max_length=400)
    def __unicode__(self):
        return str(self.audiofile)

class ImageFile(models.Model):
    imagefile = models.FileField(upload_to="files")
    description = models.CharField(max_length=400)
    def __unicode__(self):
        return self.description

class Linguistic(models.Model):
    partofspeech = models.CharField(max_length=40)
    def __unicode__(self):
        return self.partofspeech

class Word(models.Model):
    secwepemc = models.CharField(max_length=40, help_text='A word in Secwepemctsin')
    english = models.CharField(max_length=40, help_text='The English word.')
    dialect = models.CharField(max_length=40,
            help_text='One of North,East, or West',
            blank=True)
    english = models.CharField(max_length=40,
            help_text='The English word.')
    audiofile = models.ManyToManyField(AudioFile,blank=True,related_name='afiles')
    imagefile = models.ManyToManyField(ImageFile,blank=True)
    pub_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.secwepemc
    def list_audiofiles(self):
        text = 'hello'
        return text
    def strip_accents(self):
        s = self.secwepemc
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

