from django.db import models
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.contrib.auth.models import User,Group
from django.core.cache import cache
from django.utils import encoding
from django.template.defaultfilters import date as datefilter
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from datetime import datetime
from word.models import Word
import tagging
import unicodedata

class AudioFile(models.Model):
    audiofile = models.FileField(upload_to="files/audio")
    secwepemc = models.ForeignKey(Word)
    uploaded_by = models.ForeignKey(User)
    slug = models.SlugField(max_length=50)
    pub_date = models.DateTimeField(default=datetime.now())
    description = models.CharField(max_length=400)
    voice = models.CharField(max_length=400)
    recorded_by = models.CharField(max_length=400)

    def __unicode__(self):
        return force_unicode(self.slug)
    def get_absolute_url(self):
        return "/audiofile/detail/%d" % self.id
