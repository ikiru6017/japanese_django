from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django_jinja.builtins import DEFAULT_EXTENSIONS
from django.db.models import Count, Max
from django.views.generic import View

from django.urls import reverse

from .models import Lesson, Speechpart, Word, Kanji, Task_types, Task


def index(request):
    lessons_list = Lesson.objects.order_by('id')
    return render(request, 'lessons/list.html', {'lessons_list': lessons_list})

def detail(request, lesson_id):
    try:
        a = Lesson.objects.get( id = lesson_id )
    except:
        raise Http404("Урок не найден")

    word_list = a.word_set.order_by('id')
    
    return render(request, 'lessons/detail.html', {'lesson': a, 'word_list':word_list})

def task_index(request, lesson_id):
    a = Lesson.objects.get( id = lesson_id )
    tasks_list = Task.objects.values('id', 'task_num', 'task_part').annotate(dcount=Count('task_num')).order_by('id')
    return render(request, 'lessons/t_list.html', {'lesson': a, 'tasks_list': tasks_list})


def task_detail(request, lesson_id, task_num, task_part):
    try:
        a = Lesson.objects.get( id = lesson_id )
        b = Task.objects.get(lesson_id=lesson_id, task_num=task_num, task_part=task_part)
        tasks_list = Task.objects.values('id', 'task_num', 'task_part').annotate(dcount=Count('task_num')).order_by('id')
        istest = Task.objects.values('task_type').filter(lesson_id=lesson_id, task_num=task_num, task_part=task_part)
        istest2 = next(iter(istest))
        if istest2['task_type'] == 3:
            aopt = Task.objects.values('ans_option').filter(lesson_id=lesson_id, task_num=task_num, task_part=task_part)
            ans = next(iter(aopt))
            a1 = ans['ans_option'][0]
            a2 = ans['ans_option'][1]
            
        else:
            return render(request, 'lessons/task_detail.html', {'lesson': a, 'task': b, 'tasks_list': tasks_list})
    except:
        raise Http404("Задания не найдены")
    
    return render(request, 'lessons/task_detail.html', {'lesson': a, 'task': b, 'tasks_list': tasks_list, 'a1': a1, 'a2': a2})

def next_task(request, lesson_id, task_num, task_part):
    f = 1
    d = Task.objects.values('task_part').annotate(c=Count('task_part')).values_list('task_part', flat=True).filter(lesson_id=lesson_id, task_num=task_num)
    while f < max(d):
        try:
            a = Lesson.objects.get( id = lesson_id )
            b = Task.objects.get(lesson_id=lesson_id, task_num=task_num, task_part=task_part)
            f += 1
        except:
            raise Http404("Задания не найдены")
        
        
    return HttpResponseRedirect( reverse('lessons:task_detail', args = (a.id, b.task_num, b.task_part+1,)) )

#  # эта часть не работает (переход с последнего подзадания)
#     if f >= max(d):
#         f = 1
#         b.task_part = 1
#         return HttpResponseRedirect( reverse('lessons:task_detail', args = (a.id, b.task_num+1, b.task_part,)) )

# def answer_options(request, lesson_id, task_num, task_part):
#     istest = Task.objects.values('task_type')
#     if istest == 4: