from django.urls import include, path
from .views import PerfomanceListView, line_chart, line_chart_json


from . import views

app_name = 'users'
urlpatterns = [
    path('', PerfomanceListView.as_view(), name = 'index'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', views.line_chart_json, name='line_chart_json'),
]