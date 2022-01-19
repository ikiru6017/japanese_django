from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, Acad_perfomance
from django.db.models import Count, Max
from .filters import PerfomanceFilter

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Добро пожаловать, {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            pro = Profile.objects.get(user=request.user.profile.user)
            pro.login = request.user.username
            pro.email = request.user.email
            pro.save()
            messages.success(request, f'Данные успешно обновлены!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def index(request):
    perfomance_list = Acad_perfomance.objects.order_by('id')
    perfomance_list_lesson = Acad_perfomance.objects.order_by('seito')
    perfomance_list_user = Acad_perfomance.objects.filter(seito=request.user)
    perfomance_allusers = Acad_perfomance.objects.values('seito').annotate(dcount=Count('seito')).values_list('seito', flat=True)
    return render(request, 'users/perfomance.html', {'perfomance_list': perfomance_list, 'perfomance_list_user':perfomance_list_user, 'perfomance_allusers':perfomance_allusers, 'perfomance_list_lesson':perfomance_list_lesson })

class PerfomanceListView(ListView):
    model = Acad_perfomance
    template_name = 'users/perfomance.html'
    context_object_name = 'perfomance_list'
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super(PerfomanceListView, self).get_context_data(**kwargs)
        context['perfomance_list_user'] = Acad_perfomance.objects.filter(seito=self.request.user.id)
        context['perfomance_list_lesson'] = Acad_perfomance.objects.values('lesson').annotate(dcount=Count('lesson')).values_list('lesson', flat=True)
        context['perfomance_allusers'] = Acad_perfomance.objects.values('seito__login').annotate(dcount=Count('seito')).values_list('seito__login', flat=True)
        context['perfomance_list_tasks'] = Acad_perfomance.objects.values('task_num').annotate(dcount=Count('task_num')).values_list('task_num', flat=True)
        context['filter'] = PerfomanceFilter(self.request.GET, queryset=self.get_queryset())
       
        return context


class LineChartJSONView(BaseLineChartView):
    model = Acad_perfomance
    
    # def get_providers(self):
    #     return ["Central"]

    def get_labels(self):
        """Return 2 labels for the x-axis."""
        
        return ["Правильно", "Неправильно"]
    

    def get_data(self):
        """Return datasets to plot."""
        # a = request.GET['.user_login']
        # print(id_seito.selected)
        # qs = Acad_perfomance.objects.all()
        # filter = PerfomanceFilter(self.request.GET, queryset=Acad_perfomance.objects.values('rights'))
        # query = request.GET.get('seito')
        # print (filter.filters['seito'])
        # print (format(query))
        # rightcounter = len(next(iter(Acad_perfomance.objects.values('rights').filter(seito=34, lesson_id=1, task_num=2)))['rights'])
        # wrongcounter = len(next(iter(Acad_perfomance.objects.values('wrongs').filter(seito=34, lesson_id=1, task_num=2)))['wrongs'])
        data = [[]]

        
        # return render(request, 'users/perfomance.html', {'data': data})
        return data


line_chart = TemplateView.as_view(template_name='users/perfomance.html')
line_chart_json = LineChartJSONView.as_view()

