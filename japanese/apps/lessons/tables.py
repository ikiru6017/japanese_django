import django_tables2 as tables
from .models import Word
from django_jinja.builtins import DEFAULT_EXTENSIONS

class WordTable(tables.Table):
    class Meta:
        model = Word
        template_name = 'django_tables2/bootstrap.html'
        fields = ('word_name', 'transcription', 'word_translation', 'speechpart', 'lesson', )