from django import forms
from word.models import Word
import datetime
import os
from django.conf import settings

class AudioRecorderForm(forms.Form):
    ip = forms.IPAddressField(widget=forms.HiddenInput())
    word = forms.ModelChoiceField(Word.objects.all(),widget=forms.HiddenInput())
    wordname = forms.CharField(widget=forms.HiddenInput())
    port = forms.CharField(widget=forms.HiddenInput())
    description = forms.CharField(required=False, widget=forms.Textarea())
