from django.contrib import admin

from .models import Lesson, Speechpart, Word, Kanji, Task_types, Task

admin.site.register(Lesson)
admin.site.register(Speechpart)
admin.site.register(Word)
admin.site.register(Kanji)
admin.site.register(Task_types)
admin.site.register(Task)