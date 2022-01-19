from django.urls import include, path

from . import views

app_name = 'mainApp'
urlpatterns = [
    path('', views.index, name = 'index'),
]