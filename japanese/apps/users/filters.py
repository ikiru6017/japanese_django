import django_filters
from .models import Acad_perfomance

class PerfomanceFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        """Retranslate fields for template"""

        super(PerfomanceFilter, self).__init__(*args, **kwargs)
        self.filters['seito'].label = 'Ученик'
        self.filters['lesson'].label = 'Урок'

    class Meta:
        model = Acad_perfomance
        fields = ['seito', 'lesson', 'task_num']

