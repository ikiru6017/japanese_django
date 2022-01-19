from django.urls import include, path
from django.contrib import admin
from .views import (
    LessonListView,
    LessonDetailView,
    LessonCreateView,
    LessonUpdateView,
    LessonDeleteView,
    TaskListView,
    TaskCreateView
)

from . import views

app_name = 'lessons'
urlpatterns = [
    path('', LessonListView.as_view(), name = 'index'),
    path('<int:pk>/', LessonDetailView.as_view(), name = 'lesson-detail'),
    path('new/', LessonCreateView.as_view(), name = 'lesson-create'),
    path('<int:pk>/update/', LessonUpdateView.as_view(), name = 'lesson-update'),
    path('<int:pk>/delete/', LessonDeleteView.as_view(), name = 'lesson-delete'),
    path('<int:pk>/tasks/', TaskListView.as_view(), name = 'task_index'),
    path('tasks/new', TaskCreateView.as_view(), name = 'task-create'),
    path('<int:lesson_id>/tasks/<int:task_num>.<int:task_part>/', views.task_detail, name = 'task_detail'),
    path('<int:lesson_id>/tasks/<int:task_num>.<int:task_part>/next_task/', views.next_task, name = 'next_task'),
    path('<int:lesson_id>/tasks/<int:task_num>.<int:task_part>/end_task/', views.end_task, name = 'end_task')
]