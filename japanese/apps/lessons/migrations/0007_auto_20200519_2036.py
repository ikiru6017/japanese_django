# Generated by Django 3.0.4 on 2020-05-19 13:36

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_auto_20200516_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='text',
        ),
        migrations.AddField(
            model_name='lesson',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Контент'),
        ),
    ]