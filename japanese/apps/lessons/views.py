from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_jinja.builtins import DEFAULT_EXTENSIONS
from django.db.models import Count, Max
from django.views.generic import View
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField

import datetime


from django.urls import reverse

from .models import Lesson, Speechpart, Word, Kanji, Task_types, Task, Answer
from users.models import Profile, Acad_perfomance


def index(request):
    lessons_list = Lesson.objects.order_by('id')
    return render(request, 'lessons/list.html', {'lessons_list': lessons_list})

class LessonListView(ListView):
    model = Lesson
    template_name = 'lessons/list.html'
    context_object_name = 'lessons_list'
    ordering = ['lesson_num']


class LessonDetailView(DetailView):
    model = Lesson


class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    fields = ['lesson_num', 'title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.profile.m_role == 'Administrator' or self.request.user.profile.m_role == 'Teacher':
            return True
        return False


class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    fields = ['lesson_num', 'title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.profile.m_role == 'Administrator' or self.request.user.profile.m_role == 'Teacher':
            return True
        return False


class LessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lesson
    success_url = '/lessons/'

    def test_func(self):
        if self.request.user.profile.m_role == 'Administrator':
            return True
        return False


def detail(request, lesson_id):
    try:
        lesson_gotten = Lesson.objects.get( id = lesson_id )
    except:
        raise Http404("Урок не найден")

    word_list = lesson_gotten.word_set.order_by('id')
    kanji_list = lesson_gotten.kanji_set.order_by('id')
    
    return render(request, 'lessons/detail.html', {'lesson': lesson_gotten, 'word_list':word_list, 'kanji_list':kanji_list})


def task_index(request, lesson_id):
    """Display list of task nums in lessons"""

    lesson_gotten = Lesson.objects.get( id = lesson_id)
    tasks_list = Task.objects.values('task_num').filter(task_part=1, lesson_id=lesson_id)
    return render(request, 'lessons/t_list.html', {'lesson': lesson_gotten, 'tasks_list': tasks_list})


class TaskListView(ListView):
    """Task list for form"""
    
    model = Task, Lesson
    template_name = 'lessons/t_list.html'
    context_object_name = 'tasks_list'

    def get_queryset(self):
        return Task.objects.values('lesson_id', 'task_num').order_by('id').filter(task_part=1, lesson_id=self.request.resolver_match.kwargs['pk'])
    


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    fields = ['lesson', 'task_num', 'task_part', 'task_title', 'task_text', 'task_type', 'ans_option']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.profile.m_role == 'Administrator' or self.request.user.profile.m_role == 'Teacher':
            return True
        return False


cache.set('rights', 0)          #Create cache for right answers
def task_detail(request, lesson_id, task_num, task_part):
    try:
        lesson_gotten = Lesson.objects.get( id = lesson_id )
        task_gotten = Task.objects.get(lesson_id=lesson_id, task_num=task_num, task_part=task_part)
        tasks_list = Task.objects.values('task_num').filter(task_part=1, lesson_id=lesson_id)
        istest = next(iter(Task.objects.values('task_type').filter(lesson_id=lesson_id, task_num=task_num, task_part=task_part)))
        cache.get('rights')         #Initialize cache
        Task.objects.aggregate(Max('task_part'))            #Task part counter
        if istest['task_type'] == 3:            #If it`s test then initialize answer options
            ans = next(iter(Task.objects.values('ans_option').filter(lesson_id=lesson_id, task_num=task_num, task_part=task_part)))
            a1 = ans['ans_option'][0]
            a2 = ans['ans_option'][1]
            
        else:
            return render(request, 'lessons/task_detail.html', {'lesson': lesson_gotten, 'task': task_gotten, 'tasks_list': tasks_list})
    except:
        raise Http404("Задания не найдены")
    
    return render(request, 'lessons/task_detail.html', {'lesson': lesson_gotten, 'task': task_gotten, 'tasks_list': tasks_list, 'a1': a1, 'a2': a2})

#Create lists for answers
right_done_tasks = []
wrong_done_tasks = []
all_tasks = []

def next_task(request, lesson_id, task_num, task_part):
    taskcount = Task.objects.values('task_part').annotate(c=Count('task_part')).values_list('task_part', flat=True).filter(lesson_id=lesson_id, task_num=task_num)
    lesson_gotten = Lesson.objects.get( id = lesson_id )
    task_gotten = Task.objects.get(lesson_id=lesson_id, task_num=task_num, task_part=task_part)
    taskid = next(iter(Task.objects.values('id').filter(lesson_id=lesson_id, task_num=task_num, task_part=task_part)))
    right_answers = next(iter(Answer.objects.values('right_ans').filter(task_id=taskid['id'])))
    istest = next(iter(Task.objects.values('task_type').filter(lesson_id=lesson_id, task_num=task_num, task_part=task_part)))
    if istest['task_type'] == 3:
        current_answer = request.POST['answer']
    else:
        current_answer = request.POST['text']
    while task_gotten.task_part <= max(taskcount):
        if current_answer in right_answers['right_ans']:
            print("OK")
            cache.incr('rights', 1)         #Increase cache of right answers to 1
            right_done_tasks.append(task_gotten.task_part)       #Add task part num to list
            print(cache.get('rights'))
            print(current_answer)
        else:
            print("WTF")      #Just for the testing..  
            wrong_done_tasks.append(task_gotten.task_part)
        if task_gotten.task_part == max(taskcount):
            break
        return HttpResponseRedirect( reverse('lessons:task_detail', args = (lesson_gotten.id, task_gotten.task_num, task_gotten.task_part+1,)))
    current_user = Profile.objects.get(login = request.user)
    now = datetime.datetime.now()
    formatednow = now.strftime("%Y-%m-%d %H:%M:%S")
    cache.set('rights', 0)
    print (right_done_tasks)
    print (wrong_done_tasks)
    task_gotten.task_part = 1 
    Acad_perfomance.objects.create(seito=current_user, lesson=lesson_gotten, task_num=task_gotten.task_num, \
                                    rights=right_done_tasks, wrongs=wrong_done_tasks, datetime=formatednow)
    right_done_tasks.clear()
    wrong_done_tasks.clear()
      
    return HttpResponseRedirect( reverse('lessons:task_detail', args = (lesson_gotten.id, task_gotten.task_num+1, task_gotten.task_part,)) )


def Diff(alltask, rtasks):
            li_dif = [i for i in alltask + rtasks if i not in alltask or i not in rtasks]
            return li_dif


def end_task(request, lesson_id, task_num, task_part):
    taskcount = Task.objects.values('task_part').annotate(c=Count('task_part')).values_list('task_part', flat=True).filter(lesson_id=lesson_id, task_num=task_num)
    task_gotten = Task.objects.get(lesson_id=lesson_id, task_num=task_num, task_part=task_part)
    current_user = Profile.objects.get(login = request.user)
    now = datetime.datetime.now()
    formatednow = now.strftime("%Y-%m-%d %H:%M:%S")
    for i in range(1, max(taskcount)+1):        #List of task part num for comparing
        all_tasks.append(i)
    # print(all_tasks)
    allwrongs = Diff(all_tasks, right_done_tasks)           #Get remaining wrongs tasks
    cache.set('rights', 0) 
    Acad_perfomance.objects.create(seito=current_user, lesson=task_gotten.lesson, task_num=task_gotten.task_num, \
                                    rights=right_done_tasks, wrongs=allwrongs, datetime=formatednow)
    right_done_tasks.clear()
    wrong_done_tasks.clear()
    allwrongs.clear()
      
    return HttpResponseRedirect( reverse('lessons:task_index', args = (task_gotten.lesson_id,)) )