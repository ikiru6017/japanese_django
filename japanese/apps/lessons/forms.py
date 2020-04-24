from django import forms
from django.contrib.postgres.fields import ArrayField


class Lesson(forms.Form):
    lesson_num = forms.IntegerField('Номер урока')
    title = forms.CharField('Название урока', max_length = 50)

class Task_types(forms.Form):
    tt_name = forms.TextField('Тип задания', max_length = 50)

class TaskForm(forms.Form):
    CHOICES=[('')]

    lesson = forms.ForeignKey(Lesson, on_delete = forms.SET_NULL, null=True)
    task_num = forms.IntegerField('Номер задания')
    task_part = forms.IntegerField('Номер подзадания')
    task_title = forms.TextField('Название задания', max_length = 50)
    task_text = forms.TextField('Текст задания', max_length = 200)
    task_type = forms.ForeignKey(Task_types, on_delete = forms.SET_NULL, null=True)
    ans_option = ArrayField(
        ArrayField(
            forms.CharField(max_length=20, blank=True),
            size=8,
        ),
        size=8,
    )