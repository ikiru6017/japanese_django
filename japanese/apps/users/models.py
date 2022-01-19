from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from lessons.models import Lesson
from PIL import Image
from django.contrib.postgres.fields import JSONField


class Profile(models.Model):
    TEACHER = 'Teacher'
    STUDENT = 'Student'
    ADMIN = 'Administrator'
    ROLE_CHOICES = [
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
        (ADMIN, 'Administrator'),
    ]

    J201 = 'J20-1'
    J202 = 'J20-2'
    GROUP_CHOICES = [
        (J201, 'j20-1'),
        (J202, 'j20-2'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    first_name = models.CharField('Имя', max_length = 50)
    second_name = models.CharField('Фамилия', max_length = 50)
    login = models.CharField('Логин', max_length = 50)
    email = models.CharField('Почта', max_length = 50)
    m_role = models.CharField('Роль', max_length = 15, choices=ROLE_CHOICES, default=STUDENT)
    info = JSONField('Информация', max_length = 50)
    group_num = models.CharField('Номер группы', max_length = 50, choices=GROUP_CHOICES, default=J201)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Acad_perfomance(models.Model):
    seito = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name="students")
    lesson = models.ForeignKey('lessons.Lesson', on_delete = models.CASCADE, null=True, related_name="perfomances")
    task_num = models.IntegerField('Номер задания')
    rights = ArrayField(
        ArrayField(
            models.IntegerField(blank=True),
            size=8,
        ),
        size=8,
    )
    wrongs = ArrayField(
        ArrayField(
            models.IntegerField(blank=True),
            size=8,
        ),
        size=8,
    )
    datetime = models.DateTimeField()

    def user_login(self):
        return self.seito.login

    class Meta:
        verbose_name = 'Успеваемость'
        verbose_name_plural = 'Успеваемость'
