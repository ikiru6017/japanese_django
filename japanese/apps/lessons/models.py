from django.contrib.postgres.fields import ArrayField
from django.db import models

class Lesson(models.Model):
    lesson_num = models.IntegerField('Номер урока')
    title = models.CharField('Название урока', max_length = 50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = "Уроки"

class Speechpart(models.Model):
    sp_name = models.CharField('Часть речи', max_length = 20)

    def __str__(self):
        return self.sp_name

    class Meta:
        verbose_name = 'Часть речи'
        verbose_name_plural = "Части речи"

class Word(models.Model):
    word_name = models.CharField('Номер урока', max_length = 30)
    transcription = models.CharField('Название урока', max_length = 30)
    word_translation = models.TextField('Перевод слова', max_length = 50)
    speechpart = models.ForeignKey(Speechpart, on_delete = models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete = models.SET_NULL, null=True)

    def __str__(self):
        return self.word_name

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = "Слова"

class Kanji(models.Model):
    kanji_name = models.CharField('Иероглиф', max_length = 5)
    meanings = models.CharField('Значение', max_length = 50)
    kunyomi = models.TextField('Кунное чтение', max_length = 10)
    onyomi = models.TextField('Онное чтение', max_length = 10)
    linesqty = models.IntegerField('Количество черт')
    code = models.CharField('Код', max_length = 5)
    lesson = models.ForeignKey(Lesson, on_delete = models.SET_NULL, null=True)

    def __str__(self):
        return self.kanji_name

    class Meta:
        verbose_name = 'Иероглиф'
        verbose_name_plural = "Иероглифы"

class Task_types(models.Model):
    tt_name = models.TextField('Тип задания', max_length = 50)

    def __str__(self):
        return self.tt_name

    class Meta:
        verbose_name = 'Тип задания'
        verbose_name_plural = 'Типы заданий'

class Task(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete = models.SET_NULL, null=True)
    task_num = models.IntegerField('Номер задания')
    task_part = models.IntegerField('Номер подзадания')
    task_title = models.TextField('Название задания', max_length = 50)
    task_text = models.TextField('Текст задания', max_length = 200)
    task_type = models.ForeignKey(Task_types, on_delete = models.SET_NULL, null=True)
    ans_option = ArrayField(
        ArrayField(
            models.CharField(max_length=20, blank=True),
            size=8,
        ),
        size=8,
    )

    def __str__(self):
        return self.task_title

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'