# Generated by Django 3.0.4 on 2020-04-12 15:47

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task_types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tt_name', models.CharField(max_length=20, verbose_name='Тип задания')),
            ],
            options={
                'verbose_name': 'Тип задания',
                'verbose_name_plural': 'Типы заданий',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_num', models.IntegerField(verbose_name='Номер задания')),
                ('task_part', models.IntegerField(verbose_name='Номер подзадания')),
                ('task_title', models.TextField(max_length=50, verbose_name='Название задания')),
                ('task_text', models.TextField(max_length=200, verbose_name='Текст задания')),
                ('ans_option', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), size=8), size=8)),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessons.Lesson')),
                ('task_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessons.Task_types')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
    ]
