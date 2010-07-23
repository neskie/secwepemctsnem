from audio.models import *
from django.contrib import admin
from django import forms

class AudioFileAdmin( admin.ModelAdmin ):
    list_display = ('audiofile','description')

try:
        admin.site.register(AudioFile,AudioFileAdmin)
except :
        pass

