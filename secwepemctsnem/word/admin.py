from word.models import *
from audio.models import AudioFile
from django.contrib import admin

class EnglishWordInline(admin.TabularInline):
    model = EnglishWord
    extra = 3
class NotesInline(admin.TabularInline):
    model = Notes
    extra = 1

class AudioFileAdmin(admin.ModelAdmin):
    list_display = ['audiofile', 'pub_date', 'recorded_by']

class EnglishWordAdmin(admin.ModelAdmin):
    search_fields = ('english', 'secwepemc__secwepemc')

    list_display = ('secwepemc', 'english',)

class WordAdmin(admin.ModelAdmin):
    inlines = [
        EnglishWordInline, NotesInline,
    ]
    search_fields = ('secwepemc', )
    list_display = ('secwepemc', 'english', 'pub_date')

admin.site.register(Word,WordAdmin)
admin.site.register(EnglishWord,EnglishWordAdmin)
admin.site.register(AudioFile,AudioFileAdmin)
