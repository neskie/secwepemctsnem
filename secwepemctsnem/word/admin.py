from word.models import Word
from word.models import Linguistic
from word.models import AudioFile
from word.models import ImageFile
from django.contrib import admin

class AudioFileInline(admin.TabularInline):
    model = Word.audiofile.through
    extra = 1

class AudioFileAdmin(admin.ModelAdmin):
    list_display = ['audiofile', 'pub_date', 'recorded_by']
    inlines = [
        AudioFileInline,
    ]

class ImageFileInline(admin.TabularInline):
    model = Word.imagefile.through
    extra = 1

class ImageFileAdmin(admin.ModelAdmin):
    inlines = [
        ImageFileInline,
    ]

class WordAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('secwepemc','audiofile', 'english', 'dialect')
        }),
    )
    inlines = [
        AudioFileInline,
    ]
    search_fields = ('secwepemc', 'english')
    list_display = ('secwepemc', 'english', 'pub_date')
    related_search_fields = {
            'audiofile':('^audiofile',),
    }

admin.site.register(Word,WordAdmin)
admin.site.register(AudioFile,AudioFileAdmin)
admin.site.register(ImageFile,ImageFileAdmin)
admin.site.register(Linguistic)
