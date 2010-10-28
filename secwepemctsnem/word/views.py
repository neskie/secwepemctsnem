# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from word.models import *
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify, urlize, escape
from django.core import serializers 
import csv
import mimetypes
import os
from cStringIO import StringIO
from csvwriter import UnicodeWriter
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from django.contrib.contenttypes.models import ContentType
from tagging.models import Tag, TaggedItem
from django.views.decorators.cache import cache_page
from django.core import serializers
from forms import *
from django.conf import settings
from django.utils.encoding import smart_unicode, smart_str, force_unicode
import subprocess
from django.views.generic.list_detail import *
from django.contrib.auth.decorators import login_required

def show_excel(request,cat_id):
    # use a StringIO buffer rather than opening a file
    output = StringIO()
    tag = Tag.objects.get(pk=cat_id)
    word_ids = Tag.objects.get(pk=cat_id).items.values('object_id')
    w = UnicodeWriter(output)
    for id in word_ids:
        word = Word.objects.get(pk=id['object_id'])
        row = [word.secwepemc, word.english()]
        w.writerow(row)
    # rewind the virtual file
    output.seek(0)
    response = HttpResponse(output.read(), mimetype='application/ms-excel')
    response['Content-Disposition'] = 'filename=%s.csv'%str(tag)
    return response

def audio(request):
    word_list = Word.objects.filter(audiofile__isnull=False)

    t = loader.get_template('word/audio_table.html')
    c = ({
        'title': 'Audio',

    })
    return object_list(request,word_list,extra_context=c,template_name='word/audio_table.html')

def alphabet(request,letter):
    '''Gets a wordlsit of all the words that start with a letter '''
    alphabet = u'aceghiklmnopqrstuwxyáéíóú'
    words = Word.objects.none()
    if letter != '':
        words = Word.objects.filter(secwepemc__istartswith=letter)

    title = 'Words Starting with %s'%(letter)
    t = loader.get_template('word/index.html')
    c = {
        'alphabet': alphabet,
        'letter': letter,
        'title': title,
    }
    return object_list(request, words,extra_context=c,paginate_by=10)

def dialect(request,dialect):
    '''Gets a wordlsit of all the words that start with a letter '''
    words = Word.objects.none()
    if dialect != '':
        words = Word.objects.filter(dialect=dialect[0])

    title = 'Words from the %s'%(dialect)
    t = loader.get_template('word/index.html')
    c = {
        'dialects': dict(Word.DIALECT_CHOICES)[dialect[0]],
        'title': title,
    }
    return object_list(request, words,extra_context=c,paginate_by=10)

def category_detail(request,cat_id):
    tag = Tag.objects.get(pk=cat_id)
    taggeditems = TaggedItem.objects.filter(tag=tag).values_list('object_id',flat=True)
    words = Word.objects.filter(id__in=taggeditems)
    c = {
        'title': '%s'%tag.name,
    }
    return object_list(request, words,extra_context=c,paginate_by=10)

def word_detail(request,word_id, xspf=False):
    words = Word.objects.all()
    tags = TaggedItem.objects.filter(object_id=word_id)
    if xspf:
        return object_detail(request, words,object_id=word_id,
                template_name='word/word_xspf.html',
               extra_context={'tags':tags} )
    return object_detail(request, words,object_id=word_id,
            extra_context={'tags':tags})

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
        p = Paragraph("%s - %s" % (word.secwepemc, word.english()),style)
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
    t = loader.get_template('word/random.html')
    c = RequestContext(request,{
    })
    return HttpResponse(t.render(c))

def search(request):
    from django.db import connection, transaction
    query = request.GET.get('q')
    if query:
        cursor = connection.cursor()
        cursor.execute("SELECT word_id FROM word_search WHERE body MATCH %s",
                [query])
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
