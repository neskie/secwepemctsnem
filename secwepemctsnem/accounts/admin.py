from accounts.models import *
from django.contrib import admin
from django import forms

try:
        admin.site.register(UserProfile)
except :
        pass

