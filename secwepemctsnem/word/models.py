from django.db import models
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.contrib.auth.models import User,Group
from datetime import datetime
import unicodedata

class PartOfSpeech(models.Model):    
    partofspeech = models.CharField(max_length=40, unique=True, help_text='Part of Speech.')
    def __unicode__(self):
        return self.partofspeech

class Word(models.Model):
    secwepemc = models.CharField(max_length=50, unique=True, help_text='A word in Secwepemctsin')
    DIALECT_CHOICES = (
            ('A', 'All'),
            ('N', 'Northern'),
            ('W', 'Western'),
            ('E', 'Eastern'),
    )
    dialect = models.CharField(max_length=2,choices=DIALECT_CHOICES,
            blank=True,default='A', help_text='The Secwepemc Dialect that this word/spelling is from.')
    pub_date = models.DateTimeField(default=datetime.now())
    submitted_by = models.ForeignKey(User)
    part_of_speech = models.ForeignKey(PartOfSpeech)

    def __unicode__(self):
        return force_unicode(self.secwepemc)
    def strip_accents(self):
        s = self.secwepemc
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    def get_absolute_url(self):
        return "/words/%d" % self.id
    def english(self):
        if self.englishword_set.count == 0:
            return ""
        if self.englishword_set.count == 1:
            return self.englishword_set.all()[0].english
        if self.englishword_set.count > 1:
            return ", ".join(self.englishword_set.all().values_list('english', flat=True))

class EnglishWord(models.Model):    
    english = models.CharField(max_length=40, help_text='The English word.')
    secwepemc = models.ForeignKey(Word)
    class Meta:
        unique_together = ('english', 'secwepemc')

class MetaData(models.Model):    
    url = models.URLField(help_text='Original location of word on Internet.')
    source = models.CharField(max_length=200)
    secwepemc = models.ForeignKey(Word)

class Notes(models.Model):
    text = models.TextField(max_length=400, unique=True,
       help_text='Notes about a secwepemc word')
    secwepemc = models.ForeignKey(Word)
    submitted_by = models.ForeignKey(User)
