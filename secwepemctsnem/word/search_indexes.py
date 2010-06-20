from haystack import indexes
from haystack.sites import site
from models import Word
import datetime

class WordIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True,use_template=True)
    secwepemc = indexes.CharField(model_attr='secwepemc')
    english = indexes.CharField(model_attr='english')
    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Word.objects.all()
site.register(Word, WordIndex)
