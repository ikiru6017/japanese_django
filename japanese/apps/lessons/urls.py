from django.urls import include, path
from django.contrib import admin

from . import views

app_name = 'lessons'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:lesson_id>/', views.detail, name = 'detail'),
    path('<int:lesson_id>/tasks/', views.task_index, name = 'task_index'),
    path('<int:lesson_id>/tasks/<int:task_num>.<int:task_part>/', views.task_detail, name = 'task_detail'),
    path('<int:lesson_id>/tasks/<int:task_num>.<int:task_part>/next_task/', views.next_task, name = 'next_task')
]