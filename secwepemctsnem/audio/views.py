from models import *
from django.views.generic.list_detail import *
import subprocess
from audio.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.template.defaultfilters import slugify, urlize
from word.models import Word
from django.utils.encoding import smart_unicode, smart_str, force_unicode

# Create your views here.
def download_view(request, audio_id):
    audiofile = AudioFile.objects.get(pk=audio_id)
    filename = str(audiofile)
    filename = settings.MEDIA_ROOT+filename
    file = open(filename,"r")
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype: mimetype = "application/octet-stream"

    response = HttpResponse(file.read(), mimetype=mimetype)
    response["Content-Disposition"]= "attachment; filename=%s" % os.path.split(filename)[1]
    return response

def audioplayer(request,audio_id):
    audiofile = AudioFile.objects.get(pk=audio_id)
    t = loader.get_template('word/audioplayer.html')
    c = RequestContext(request,{
        'audiofile': audiofile,
    })
    return HttpResponse(t.render(c))

@login_required
def recorder(request, word_id):
    '''This view allows the user to record audio fiels using the flash
    recorder to record a word that is already in the database.'''
    if request.method == 'POST':
        form = AudioRecorderForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            word = form.cleaned_data['word']
            wordname = slugify(word.strip_accents())
            ip = form.cleaned_data['ip']
            port = form.cleaned_data['port']
            description = form.cleaned_data['description']
            flashfile = u"%sfiles/flashfiles/%s_%s_%s.flv" % (settings.MEDIA_ROOT,
                    form.cleaned_data['ip'],
                    form.cleaned_data['port'],
                    wordname)
            #Write IP, Port, name to Log
            #Check if there are already audiofiles with that wordname.
            afiles = AudioFile.objects.filter(audiofile__startswith="files/audiofiles/%s"%wordname)
            #Now convert flashfile if it exists to an mp3.
            if os.path.exists(flashfile.encode('utf-8')):
                afile = "%sfiles/audiofiles/%s_%d.mp3" %(
                        settings.MEDIA_ROOT,
                    wordname,
                    len(afiles),
                    )
                subprocess.Popen(['/usr/bin/ffmpeg', '-y', '-i',
                    flashfile.encode('utf-8'), afile.encode('utf-8')]) 
                if request.user.get_full_name():
                    recorded_by = request.user.get_full_name()
                else:
                    recorded_by = request.user.username()

                a = AudioFile(
                        audiofile='files/audiofiles/%s_%d.mp3'%(smart_str(wordname),len(afiles)),
                        secwepemc=word,
                        uploaded_by=request.user,
                        slug=wordname,
                        description=description,
                        voice="%s"% recorded_by,
                        recorded_by="%s"%  recorded_by,
                        )
                a.save()

                return HttpResponseRedirect('/words/%s'%word_id) # Redirect after
        c = RequestContext(request,{
            'word': Word.objects.get(pk=word_id),
            'filename': wordname,
            'ip': ip,
            'port': port,
            'form': form,
            'title': 'Record Some Words',
        })

        t = loader.get_template('word/recorder.html')

        return HttpResponse(t.render(c))

    else:
        ip = request.META['REMOTE_ADDR']
        try:
            port = request.META['REMOTE_PORT']
        except:
            port = 0
        '''If the word doesn't exist offer to create it'''
        try:
            word= Word.objects.get(pk=word_id)
        except Word.DoesNotExist:
            return HttpResponseRedirect("/words/create/")

        #Return a bounded form, because the word needs to exist in the database.
        form = AudioRecorderForm(dict(ip=ip,word=word.id,wordname=word.secwepemc,port=port))
        flashfile = "%sfiles/flashfiles/%s_%s_%s.flv" % (settings.MEDIA_ROOT, ip,port, word.secwepemc)
        c = RequestContext(request,{
            'word': word,
            'filename': slugify(word.strip_accents()),
            'ip': ip,
            'port': port,
            'form': form,
            'root': flashfile,
            'title': 'Record Some Words',
        })

        t = loader.get_template('word/recorder.html')

        return HttpResponse(t.render(c))

def audiofile_detail(request,audio_id, xspf=False):
    import json
    audiofiles = AudioFile.objects.all()
    if xspf:
        t = loader.get_template('word/audiofile_xspf.html')
        c = RequestContext(request,{
            'audiofile':  AudioFile.objects.get(pk=audio_id),
            'xspf': xspf,
        })
        return HttpResponse(t.render(c))
    return object_detail(request,audiofiles, audio_id)
