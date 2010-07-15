# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from word.models import *
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify, urlize
from django.core import serializers 
import csv
import mimetypes
import os
import codecs
from cStringIO import StringIO
from csvwriter import UnicodeWriter
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from django.contrib.contenttypes.models import ContentType
from tagging.models import Tag
from django.views.decorators.cache import cache_page
from django.core import serializers
from forms import *
from django.conf import settings
from django.utils.encoding import smart_unicode, smart_str, force_unicode
import subprocess

def recorder(request):
    '''This view allows the user to record audio fiels using the flash
    recorder to record a word that is already in the database.'''
    if request.method == 'POST':
        form = AudioRecorderForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            word_id = form.cleaned_data['word']
            wordname = smart_unicode(form.cleaned_data['wordname'])
            ip = form.cleaned_data['ip']
            port = form.cleaned_data['port']
            flashfile = u"%sfiles/flashfiles/%s_%s_%s.flv" % (settings.MEDIA_ROOT,
                    form.cleaned_data['ip'],
                    form.cleaned_data['port'],
                    wordname)
            #Write IP, Port, name to Log
            #Check if there are already audiofiles with that wordname.
            afiles = AudioFile.objects.filter(audiofile__contains="files/audiofiles/%s"%wordname)
            #Now convert flashfile if it exists to an mp3.
            if os.path.exists(flashfile.encode('utf-8')):
                afile = "%sfiles/audiofiles/%s_%d.mp3" %(
                        settings.MEDIA_ROOT,
                    wordname,
                    len(afiles),
                    )
                subprocess.Popen(['/usr/bin/ffmpeg', '-y', '-i',
                    flashfile.encode('utf-8'), afile.encode('utf-8')]) 
                a = AudioFile(
                        audiofile='files/audiofiles/%s_%d.mp3'%(smart_str(wordname),len(afiles)),
                        description="IP:%s"%form.cleaned_data['ip'],
                        )
                a.save()
                word_id.audiofile.add(a)

                word_id = request.GET.get('word_id')
                return HttpResponseRedirect('/words/%s'%word_id) # Redirect after
        word_id = request.GET.get('word_id')
        c = RequestContext(request,{
            'word': Word.objects.get(pk=word_id),
            'filename': wordname,
            'ip': ip,
            'port': port,
            'form': form,
            'root': flashfile,
            'title': 'Record Some Words',
        })

        t = loader.get_template('word/recorder.html')

        return HttpResponse(t.render(c))

    else:
        word_id = request.GET.get('word_id')
        ip = request.META['REMOTE_ADDR']
        port = request.META['REMOTE_PORT']
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
            'filename': word.secwepemc,
            'ip': ip,
            'port': port,
            'form': form,
            'root': flashfile,
            'title': 'Record Some Words',
        })

        t = loader.get_template('word/recorder.html')

        return HttpResponse(t.render(c))

def show_excel(request,cat_id):
    # use a StringIO buffer rather than opening a file
    output = StringIO()
    tag = Tag.objects.get(pk=cat_id)
    word_ids = Tag.objects.get(pk=cat_id).items.values('object_id')
    w = UnicodeWriter(output)
    for id in word_ids:
        word = Word.objects.get(pk=id['object_id'])
        row = [(word.secwepemc),(word.english)]
        w.writerow(row)
    # rewind the virtual file
    output.seek(0)
    response = HttpResponse(output.read(), mimetype='application/ms-excel')
    response['Content-Disposition'] = 'filename=%s.csv'%str(tag)
    return response

def audio(request):
    word_list = Word.objects.filter(audiofile__isnull=False)
    paginator = Paginator(word_list, 10) # Show 25 contacts per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        words = paginator.page(page)
    except (EmptyPage, InvalidPage):
        words = paginator.page(paginator.num_pages)

    t = loader.get_template('word/audio_table.html')
    c = RequestContext(request,{
        'words': words,
        'title': 'Audio',

    })
    return HttpResponse(t.render(c))

def jsonaudiofile(request,word_id):
    data = serializers.serialize("json",
            Word.objects.get(pk=word_id).audiofile.all())
    return HttpResponse(data, mimetype="application/javascript")

def audioplayer(request,audio_id):
    audiofile = AudioFile.objects.get(pk=audio_id)
    t = loader.get_template('word/audioplayer.html')
    c = RequestContext(request,{
        'audiofile': audiofile,
    })
    return HttpResponse(t.render(c))

def alphabet(request,letter):
    word_list = Word.objects.filter(secwepemc__startswith=letter)
    paginator = Paginator(word_list, 10) # Show 25 contacts per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        words = paginator.page(page)
    except (EmptyPage, InvalidPage):
        words = paginator.page(paginator.num_pages)
    title = 'Words Starting with %s'%(letter)
    t = loader.get_template('word/index.html')
    c = RequestContext(request,{
        'alphabet': alphabet,
        'words': words,
        'title': title,
        'count': word_list.count()

    })
    return HttpResponse(t.render(c))

def category_detail(request,cat_id):
    try:
        tag = Tag.objects.get(pk=cat_id)
        title =tag.name
        error = ''
    except Tag.DoesNotExist:
        tag = []
        title = ''
        error = "That tag doesn't exist."

    t = loader.get_template('word/category_list.html')
    c = RequestContext(request,{
        'tag': tag,
        'error': error,
        'request_detail':'category_detail',
        'title': '%s'%title,
    })
    return HttpResponse(t.render(c))


def detail(request,word_id):
    word_type = ContentType.objects.get(app_label="word", model="word")
    word = Word.objects.get(pk=word_id)
    
    flashfile = ''

    t = loader.get_template('word/word.html')
    xspf = request.GET.get('xspf')
    output = ''
    if xspf:
        t = loader.get_template('word/xspf.html')
        c = RequestContext(request,{
            'word': word,
            'word_type': word_type,
            'xspf': xspf,
        })
        return HttpResponse(t.render(c))
    else:
        c = RequestContext(request,{
            'word_obj': word,
            'flashfile': flashfile,
            'word_type': word_type,
            'xspf': xspf,
        })
        return HttpResponse(t.render(c))
def export(request):
    pass

def download_view(request, audio_id):
    audiofile = AudioFile.objects.get(pk=audio_id)
    filename = str(audiofile)
    filename = '/srv/apache/static/media/'+filename
    file = open(filename,"r")
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype: mimetype = "application/octet-stream"

    response = HttpResponse(file.read(), mimetype=mimetype)
    response["Content-Disposition"]= "attachment; filename=%s" % os.path.split(filename)[1]
    return response

def show_pdf(request,cat_id):
    tag = Tag.objects.get(pk=cat_id)
    word_ids = Tag.objects.get(pk=cat_id).items.values('object_id')
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf'%(str(tag))
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    D = '/usr/share/fonts/truetype/ttf-lg-aboriginal/'
    pdfmetrics.registerFont(TTFont('Vera', D+'AboriginalSansREGULAR9433.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', D+'AboriginalSansBOLD9433.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', D+'AboriginalSansITALIC9433.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', D+'AboriginalSansBOLDITALIC9433.ttf'))

    registerFontFamily('Vera',normal='Vera',bold='VeraBd',italic='VeraIt',boldItalic='VeraBI')

    buffer = StringIO()

    doc = SimpleDocTemplate(buffer)
    Catalog = []
    styles = getSampleStyleSheet()
    header = Paragraph("%s"%(str(tag)), styles['Heading1'])
    Catalog.append(header)
    style = ParagraphStyle(
        name='Normal',
        fontName='Vera',
        fontSize=12,
    )
    count = 0
    for id in word_ids:
        word = Word.objects.get(pk=id['object_id'])
        p = Paragraph("%s - %s" % (word.secwepemc, word.english),style)
        Catalog.append(p)
        s = Spacer(1, 0.25*inch)
        Catalog.append(s)
    doc.build(Catalog)

    # Get the value of the StringIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def random_word(request):
    data = Word.objects.order_by('?')[0]
#    data = serializers.serialize('json',(data,))
    t = loader.get_template('word/random.html')
    c = RequestContext(request,{
        'word': data,
    })
    return HttpResponse(t.render(c))

def search(request):
    from django.db import connection, transaction
    query = request.GET.get('q')
    if query:
        cursor = connection.cursor()
        cursor.execute("SELECT word_id FROM word_search WHERE body MATCH '%s'" %
                query)
        results = [ x[0] for x in  cursor.fetchall()]
        words = Word.objects.filter(id__in=results)
        del results
    else:
        words = Word.objects.none()

    c = RequestContext(request,{
        'title': 'Record Some Words',
        'words': words,
        'query': query,
    })

    t = loader.get_template('search/searchql.html')
    return HttpResponse(t.render(c))

