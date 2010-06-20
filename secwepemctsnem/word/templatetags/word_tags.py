from django.template import Library, Node
from django.template.defaultfilters import stringfilter
from django.db.models import get_model
from django.utils.safestring import mark_safe

from word.models import Word
import random
     
register = Library()
     
class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
    
get_latest = register.tag(get_latest)

class RandomContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.order_by('?')[:self.num]
        return ''
 
def get_random(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_random tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_random tag must be 'as'"
    return RandomContentNode(bits[1], bits[2], bits[4])
    
get_random = register.tag(get_random)

class NoAudioNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.filter(audiofile__isnull=True)[:self.num]
        return ''
 
def get_no_audio(parser, token):
    bits = token.contents.split()
    return NoAudioNode(bits[1], bits[2], bits[4])
    
get_no_audio = register.tag(get_no_audio)

class SearchListNode(Node):
    def __init__(self, num, pagenum, varname):
        self.num, self.pagenum, self.varname = num, pagenum, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = [1,2,3,4]
        return ''
 
def get_search_list(parser, token):
    bits = token.contents.split()
    return SearchListNode(bits[1], bits[2], bits[4])
    
get_search_list = register.tag(get_search_list)
@register.filter(name='pagelist')
def pagelist(value, arg):
    output = '<ul class="pagelist">'
    pagelist = []
    if value < 6:
        if arg <=10:
            pagelist = range(1,arg+1)
        else:
            pagelist = range(1,10)
    else:
        pagelist = range(value-5,value+5)
        if arg <=10:
            pagelist = range(1,arg+1)
        if arg - 5 <= value:
            pagelist = range(arg+1-10,arg+1)

    for page in pagelist:
        if page == value:
            output += '<li>%d</li>'%(page)
        else:
            output += '<li><a href="?page=%d">%d</a></li>'%(page,page)

    output += '</ul>'
    return mark_safe(output)
pagelist.is_safe = True
