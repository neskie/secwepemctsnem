# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from word.models import *
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
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

def recorder(request):
    word_list = Word.objects.all()

    filename = request.GET.get('filename').replace('\'','')
    ip = request.META['REMOTE_ADDR']
    port = request.META['REMOTE_PORT']
    if not filename:
        filename = "testing";

    t = loader.get_template('word/recorder.html')
    c = RequestContext(request,{
        'words': word_list,
        'filename': filename,
        'ip': ip,
        'port': port,
        'title': 'Record Some Words',
    })
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
    flashfile = "/srv/apache/django-projects/secwepemctsnem/media/files/flashfiles/snd%s.flv"% word.strip_accents()
    if os.path.isfile(flashfile):
        flashfile = 'snd%s.flv'%word.strip_accents()
    else:
        flashfile = ''
    

    t = loader.get_template('word/word.html')
    xspf = request.GET.get('xspf')
    output = ''
    if xspf:
        output = '''<?xml version="1.0" encoding="UTF-8"?>
<playlist version="1" xmlns="http://xspf.org/ns/0/">
  <trackList>
'''
        for afile in word.audiofile.all():
            output += '''    <track>
     <location>http://language.secwepemcradio.ath.cx/media/%s</location></track>
     <title>%s</title>
   </track>
            ''' % (afile.audiofile, afile.description)
        output += '''
  </trackList>
</playlist>
        ''' 
        response = HttpResponse(output, mimetype='application/xspf+xml')
        response['Content-Disposition'] = 'filename=word-%s.xml'%str(word.id).split('/')[-1]
        return response
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
