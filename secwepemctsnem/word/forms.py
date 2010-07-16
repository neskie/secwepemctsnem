from django import forms
from models import Word
import datetime
import os
from django.conf import settings

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        exclude = ('audiofile', 'imagefile')


class AudioRecorderForm(forms.Form):
    ip = forms.IPAddressField(widget=forms.HiddenInput())
    word = forms.ModelChoiceField(Word.objects.all(),widget=forms.HiddenInput())
    wordname = forms.CharField(widget=forms.HiddenInput())
    port = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(required=False)
